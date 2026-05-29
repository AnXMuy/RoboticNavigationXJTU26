#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

if __name__ == "__main__":
    rospy.init_node("talker_py")
    pub = rospy.Publisher("chatter", String, queue_size=10)
    rate = rospy.Rate(10)
    count = 0

    while not rospy.is_shutdown():
        msg = f"Hello ROS Python {count}"
        pub.publish(msg)
        rospy.loginfo("发送的消息: %s", msg)
        count += 1
        rate.sleep()
