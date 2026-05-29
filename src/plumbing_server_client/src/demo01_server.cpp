#include <ros/ros.h>

#include "plumbing_server_client/AddInts.h"

bool add(plumbing_server_client::AddInts::Request &req,
         plumbing_server_client::AddInts::Response &res)
{
  res.sum = req.num1 + req.num2;
  ROS_INFO("request: num1=%d, num2=%d, sum=%d", req.num1, req.num2, res.sum);
  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "demo01_server_node");
  ros::NodeHandle nh;

  ros::ServiceServer server = nh.advertiseService("add_ints", add);
  ROS_INFO("add_ints service is ready");
  ros::spin();

  return 0;
}
