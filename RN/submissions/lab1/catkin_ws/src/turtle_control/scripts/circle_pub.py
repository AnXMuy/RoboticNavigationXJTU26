#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

if __name__ == "__main__":
    rospy.init_node("circle_pub")
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(10)

    cmd = Twist()
    cmd.linear.x = 1.0
    cmd.angular.z = 0.5

    while not rospy.is_shutdown():
        pub.publish(cmd)
        rate.sleep()
