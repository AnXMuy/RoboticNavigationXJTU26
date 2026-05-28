#!/usr/bin/env python3

import copy
import math

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler


class VehicleSim:
    def __init__(self):
        rospy.init_node("vehicle_sim_node", anonymous=False)

        self.odom_frame = rospy.get_param("~odom_frame", "odom")
        self.base_frame = rospy.get_param("~base_frame", "base_footprint")
        self.cmd_vel_timeout = rospy.get_param("~cmd_vel_timeout", 1.0)

        self.goal_linear_velocity = 0.0
        self.goal_angular_velocity = 0.0

        self.odom_pose = [0.0, 0.0, 0.0]
        self.odom_vel = [0.0, 0.0, 0.0]

        self.last_cmd_vel_time = rospy.Time.now()
        self.prev_update_time = rospy.Time.now()

        self.pose_covariance = [
            0.1, 0, 0, 0, 0, 0,
            0, 0.1, 0, 0, 0, 0,
            0, 0, 1e6, 0, 0, 0,
            0, 0, 0, 1e6, 0, 0,
            0, 0, 0, 0, 1e6, 0,
            0, 0, 0, 0, 0, 0.2,
        ]
        self.twist_covariance = copy.deepcopy(self.pose_covariance)

        self.odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
        self.cmd_vel_sub = rospy.Subscriber(
            "cmd_vel", Twist, self.command_velocity_callback, queue_size=50
        )

        self.tf_broadcaster = tf2_ros.TransformBroadcaster()

    def command_velocity_callback(self, msg):
        self.last_cmd_vel_time = rospy.Time.now()
        self.goal_linear_velocity = msg.linear.x
        self.goal_angular_velocity = msg.angular.z

    def update_odometry(self, diff_time_sec):
        v = self.goal_linear_velocity
        w = self.goal_angular_velocity

        if math.isnan(v):
            v = 0.0
        if math.isnan(w):
            w = 0.0

        delta_s = v * diff_time_sec
        delta_theta = w * diff_time_sec

        current_theta = self.odom_pose[2]
        new_theta = current_theta + delta_theta

        while new_theta > math.pi:
            new_theta -= 2.0 * math.pi
        while new_theta < -math.pi:
            new_theta += 2.0 * math.pi

        if abs(w) < 1e-6:
            delta_x = delta_s * math.cos(current_theta)
            delta_y = delta_s * math.sin(current_theta)
        else:
            radius = v / w
            delta_x = radius * (math.sin(new_theta) - math.sin(current_theta))
            delta_y = radius * (-math.cos(new_theta) + math.cos(current_theta))

        if math.isnan(delta_x):
            delta_x = 0.0
        if math.isnan(delta_y):
            delta_y = 0.0

        self.odom_pose[0] += delta_x
        self.odom_pose[1] += delta_y
        self.odom_pose[2] = new_theta

        if diff_time_sec > 0:
            self.odom_vel[0] = v
            self.odom_vel[2] = w
        else:
            self.odom_vel[0] = 0.0
            self.odom_vel[2] = 0.0

    def publish_odom_and_tf(self, time_now):
        odom_msg = Odometry()
        odom_msg.header.stamp = time_now
        odom_msg.header.frame_id = self.odom_frame
        odom_msg.child_frame_id = self.base_frame

        odom_msg.pose.pose.position.x = self.odom_pose[0]
        odom_msg.pose.pose.position.y = self.odom_pose[1]
        odom_msg.pose.pose.position.z = 0.0

        quat = quaternion_from_euler(0.0, 0.0, self.odom_pose[2])
        odom_msg.pose.pose.orientation.x = quat[0]
        odom_msg.pose.pose.orientation.y = quat[1]
        odom_msg.pose.pose.orientation.z = quat[2]
        odom_msg.pose.pose.orientation.w = quat[3]

        odom_msg.pose.covariance = self.pose_covariance
        odom_msg.twist.twist.linear.x = self.odom_vel[0]
        odom_msg.twist.twist.angular.z = self.odom_vel[2]
        odom_msg.twist.covariance = self.twist_covariance
        self.odom_pub.publish(odom_msg)

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

    def update(self):
        time_now = rospy.Time.now()
        diff_time = time_now - self.prev_update_time
        self.prev_update_time = time_now

        if (time_now - self.last_cmd_vel_time).to_sec() > self.cmd_vel_timeout:
            self.goal_linear_velocity = 0.0
            self.goal_angular_velocity = 0.0

        diff_sec = diff_time.to_sec()
        if diff_sec > 0:
            self.update_odometry(diff_sec)

        self.publish_odom_and_tf(time_now)

    def run(self):
        rate = rospy.Rate(50)
        while not rospy.is_shutdown():
            self.update()
            rate.sleep()


if __name__ == "__main__":
    try:
        VehicleSim().run()
    except rospy.ROSInterruptException:
        pass
