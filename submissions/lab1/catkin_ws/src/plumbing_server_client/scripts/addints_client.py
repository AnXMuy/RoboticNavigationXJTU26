#!/usr/bin/env python3
import sys
import rospy
from plumbing_server_client.srv import AddInts

if __name__ == "__main__":
    if len(sys.argv) != 3:
        rospy.logerr("请提交两个整数")
        sys.exit(1)

    rospy.init_node("addints_client_py")
    rospy.wait_for_service("AddInts_py")
    client = rospy.ServiceProxy("AddInts_py", AddInts)

    resp = client(int(sys.argv[1]), int(sys.argv[2]))
    rospy.loginfo("响应结果: %d", resp.sum)
