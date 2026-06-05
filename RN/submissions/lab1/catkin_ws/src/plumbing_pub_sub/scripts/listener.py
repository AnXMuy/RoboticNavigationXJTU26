#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def callback(msg):
    rospy.loginfo("我听见: %s", msg.data)


if __name__ == "__main__":
    rospy.init_node("listener_py")
    rospy.Subscriber("chatter", String, callback, queue_size=10)
    rospy.spin()
