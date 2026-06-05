#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
import tf2_ros
import copy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TransformStamped, Point, Quaternion
from tf.transformations import quaternion_from_euler

class VehicleSim:
    def __init__(self):
        # 初始化节点
        rospy.init_node('vehicle_sim_node', anonymous=True)
        
        # --- 参数配置 ---
        # 从参数服务器读取帧ID，默认值同C++代码
        self.odom_frame = rospy.get_param('~odom_frame', 'odom')
        self.base_frame = rospy.get_param('~base_frame', 'base_footprint')        
        
        # 超时时间 (秒)
        self.cmd_vel_timeout = rospy.get_param('~cmd_vel_timeout', 1.0)
        
        # 车辆运动状态变量
        self.goal_linear_velocity = 0.0
        self.goal_steering_angle = 0.0
        self.goal_yaw_rate = 0.0
        self.wheel_base = rospy.get_param('~wheel_base', 0.313)
        self.max_steering_angle = rospy.get_param('~max_steering_angle', 0.523599)
        self.cmd_angular_is_steering = rospy.get_param('~cmd_angular_is_steering', True)
        
        # 里程计状态 [x, y, theta]
        self.odom_pose = [0.0, 0.0, 0.0]
        # 里程计速度 [vx, vy, w]
        self.odom_vel = [0.0, 0.0, 0.0]
        
        self.last_cmd_vel_time = rospy.Time.now()
        self.prev_update_time = rospy.Time.now()
        
        # --- 协方差矩阵(x, y, z, roll, pitch, yaw) ---
        self.pose_covariance = [
            0.1, 0,   0,   0,   0,   0,
            0,   0.1, 0,   0,   0,   0,
            0,   0,   1e6, 0,   0,   0,
            0,   0,   0,   1e6, 0,   0,
            0,   0,   0,   0,   1e6, 0,
            0,   0,   0,   0,   0,   0.2
        ]
        # 速度协方差通常与位置类似，这里直接复用
        self.twist_covariance = copy.deepcopy(self.pose_covariance)
        
        # 发布者和订阅者
        self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=100)
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.command_velocity_callback, queue_size=100)
        
        # TF 广播器
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()

    # ------------ 回调函数：处理订阅的 cmd_vel 消息 -------------
    def command_velocity_callback(self, msg):
        
        self.last_cmd_vel_time = rospy.Time.now()
        
        self.goal_linear_velocity = msg.linear.x
        if self.cmd_angular_is_steering:
            self.goal_steering_angle = max(
                -self.max_steering_angle,
                min(self.max_steering_angle, msg.angular.z)
            )
        else:
            self.goal_yaw_rate = msg.angular.z
         

    # ------------ 计算里程计(odom_pose、odom_vel) -------------
    def update_odometry(self, diff_time_sec):
 
        v = self.goal_linear_velocity
        if self.cmd_angular_is_steering:
            w = v * math.tan(self.goal_steering_angle) / self.wheel_base
        else:
            w = self.goal_yaw_rate
        
        # 处理 NaN
        if math.isnan(v):
            v = 0.0
        if math.isnan(w):
            w = 0.0
                    
        # 位移和角度变化
        delta_s = v * diff_time_sec
        delta_theta = w * diff_time_sec
        
        #更新theta     
        current_theta = self.odom_pose[2]
        new_theta = current_theta + delta_theta
        
        # 将角度归一化到[-pi,pi]
        while new_theta > math.pi:
              new_theta -= 2.0*math.pi
        while new_theta < -math.pi:
              new_theta += 2.0*math.pi
              
        # x, y变化量
        if abs(w) < 1e-6:
           # 直线运动模型（避免除以零）
           delta_x = delta_s*math.cos(current_theta)
           delta_y = delta_s*math.sin(current_theta)
        else:
           # 圆弧运动模型
           radius = v/w      
           delta_x = radius * (math.sin(new_theta) - math.sin(current_theta))
           delta_y = radius * (-math.cos(new_theta) + math.cos(current_theta))                

        if math.isnan(delta_x):
            delta_x = 0.0
        if math.isnan(delta_y):
            delta_y = 0.0
            
        self.odom_pose[0] += delta_x
        self.odom_pose[1] += delta_y    
        self.odom_pose[2] = new_theta 
   
        # 更新瞬时速度
        if diff_time_sec > 0:
            self.odom_vel[0] = v
            self.odom_vel[2] = w
        else:
            self.odom_vel[0] = 0.0
            self.odom_vel[2] = 0.0
            
        return True


    # ------------ 发布里程计消息和 TF 变换 -------------
    def publish_odom_and_tf(self, time_now):
        # ----- 1. 构建 Odometry 消息并发布 -----
        # 头消息(header)
        odom_msg = Odometry()
        odom_msg.header.stamp = time_now
        odom_msg.header.frame_id = self.odom_frame
        odom_msg.child_frame_id = self.base_frame
        
        # 位置
        odom_msg.pose.pose.position.x = self.odom_pose[0]
        odom_msg.pose.pose.position.y = self.odom_pose[1]
        odom_msg.pose.pose.position.z = 0.0
        
        # 姿态 (Yaw -> Quaternion)
        quat = quaternion_from_euler(0, 0, self.odom_pose[2])
        odom_msg.pose.pose.orientation.x = quat[0]
        odom_msg.pose.pose.orientation.y = quat[1]
        odom_msg.pose.pose.orientation.z = quat[2]
        odom_msg.pose.pose.orientation.w = quat[3]
        
        # 协方差
        odom_msg.pose.covariance = self.pose_covariance
        
        # 速度
        odom_msg.twist.twist.linear.x = self.odom_vel[0]
        odom_msg.twist.twist.angular.z = self.odom_vel[2]
        odom_msg.twist.covariance = self.twist_covariance
        
        # 发布
        self.odom_pub.publish(odom_msg)
        
        # -----  2. 广播 TF -----
        # transformStamped 需要单独构建
        odom_tf = TransformStamped()
        odom_tf.header.stamp = time_now
        odom_tf.header.frame_id = self.odom_frame
        odom_tf.child_frame_id = self.base_frame
        odom_tf.transform.translation.x = self.odom_pose[0]
        odom_tf.transform.translation.y = self.odom_pose[1]
        odom_tf.transform.translation.z = 0.0
        odom_tf.transform.rotation.x = quat[0]
        odom_tf.transform.rotation.y = quat[1]
        odom_tf.transform.rotation.z = quat[2]
        odom_tf.transform.rotation.w = quat[3]

        self.tf_broadcaster.sendTransform(odom_tf)

    
    # ------------ 主更新循环 -------------
    def update(self):
    
        time_now = rospy.Time.now()
        diff_time = time_now - self.prev_update_time
        self.prev_update_time = time_now
        
        diff_sec = diff_time.to_sec()
        
        # --- 超时保护 ---
        if (time_now - self.last_cmd_vel_time).to_sec() > self.cmd_vel_timeout:
            self.goal_linear_velocity = 0.0
            self.goal_steering_angle = 0.0
            self.goal_yaw_rate = 0.0
            
        # 更新里程计
        if diff_sec > 0:
            self.update_odometry(diff_sec)
            
        # 发布数据
        self.publish_odom_and_tf(time_now)


    # ------------ 运行主循环 -------------
    def run(self):
            
        rate = rospy.Rate(50) # 50 Hz
        
        while not rospy.is_shutdown():
            self.update()
            rate.sleep()
            

if __name__ == '__main__':

    try:
        sim = VehicleSim()
        sim.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        rospy.loginfo("VehicleSim node terminated.")
