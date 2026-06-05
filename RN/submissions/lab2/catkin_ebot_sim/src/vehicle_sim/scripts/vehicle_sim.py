#!/usr/bin/env python3
import math

import rospy
import tf2_ros
from geometry_msgs.msg import Quaternion, TransformStamped, Twist
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler


class VehicleSimulator:
    def __init__(self):
        self.odom_frame = rospy.get_param("~odom_frame", "odom")
        self.base_frame = rospy.get_param("~base_frame", "base_footprint")
        self.publish_rate = rospy.get_param("~publish_rate", 30.0)

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.linear_x = 0.0
        self.angular_z = 0.0
        self.last_time = rospy.Time.now()

        self.odom_pub = rospy.Publisher("/odom", Odometry, queue_size=20)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        self.cmd_sub = rospy.Subscriber("/cmd_vel", Twist, self.cmd_callback, queue_size=10)

    def cmd_callback(self, msg):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z

    def step(self):
        now = rospy.Time.now()
        dt = (now - self.last_time).to_sec()
        self.last_time = now
        if dt <= 0.0:
            return

        delta_x = self.linear_x * math.cos(self.yaw) * dt
        delta_y = self.linear_x * math.sin(self.yaw) * dt
        delta_yaw = self.angular_z * dt

        self.x += delta_x
        self.y += delta_y
        self.yaw = math.atan2(math.sin(self.yaw + delta_yaw), math.cos(self.yaw + delta_yaw))

        quat_values = quaternion_from_euler(0.0, 0.0, self.yaw)
        quat = Quaternion(*quat_values)

        transform = TransformStamped()
        transform.header.stamp = now
        transform.header.frame_id = self.odom_frame
        transform.child_frame_id = self.base_frame
        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.translation.z = 0.0
        transform.transform.rotation = quat
        self.tf_broadcaster.sendTransform(transform)

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = self.odom_frame
        odom.child_frame_id = self.base_frame
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = quat
        odom.twist.twist.linear.x = self.linear_x
        odom.twist.twist.angular.z = self.angular_z
        odom.pose.covariance[0] = 0.01
        odom.pose.covariance[7] = 0.01
        odom.pose.covariance[35] = 0.02
        odom.twist.covariance[0] = 0.01
        odom.twist.covariance[35] = 0.02
        self.odom_pub.publish(odom)

    def spin(self):
        rate = rospy.Rate(self.publish_rate)
        while not rospy.is_shutdown():
            self.step()
            rate.sleep()


if __name__ == "__main__":
    rospy.init_node("vehicle_sim_node")
    VehicleSimulator().spin()
