#!/usr/bin/env python3
import rospy
from plumbing_server_client.srv import AddInts, AddIntsResponse


def handle(req):
    rospy.loginfo("服务器收到请求: num1 = %d, num2 = %d", req.num1, req.num2)
    if req.num1 < 0 or req.num2 < 0:
        rospy.logerr("提交的数据异常: 数据不可以为负数")
        return AddIntsResponse()
    return AddIntsResponse(req.num1 + req.num2)


if __name__ == "__main__":
    rospy.init_node("addints_server_py")
    server = rospy.Service("AddInts_py", AddInts, handle)
    rospy.loginfo("Python 服务已经启动...")
    rospy.spin()
