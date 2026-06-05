#include <cstdlib>

#include <ros/ros.h>

#include "plumbing_server_client/AddInts.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "demo02_client_node");

  if (argc != 3)
  {
    ROS_ERROR("usage: rosrun plumbing_server_client demo02_client_node num1 num2");
    return 1;
  }

  ros::NodeHandle nh;
  ros::ServiceClient client = nh.serviceClient<plumbing_server_client::AddInts>("add_ints");

  plumbing_server_client::AddInts srv;
  srv.request.num1 = std::atoi(argv[1]);
  srv.request.num2 = std::atoi(argv[2]);

  if (client.call(srv))
  {
    ROS_INFO("sum: %d", srv.response.sum);
    return 0;
  }

  ROS_ERROR("failed to call add_ints service");
  return 1;
}
