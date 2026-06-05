#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose


def callback(msg):
    rospy.loginfo(
        "位姿: x=%.3f y=%.3f theta=%.3f linear=%.3f angular=%.3f",
        msg.x, msg.y, msg.theta, msg.linear_velocity, msg.angular_velocity,
    )


if __name__ == "__main__":
    rospy.init_node("pose_sub")
    rospy.Subscriber("/turtle1/pose", Pose, callback, queue_size=10)
    rospy.spin()
