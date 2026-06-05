#include <ros/ros.h>
#include <std_msgs/String.h>

#include <sstream>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "demo01_pub_node");
  ros::NodeHandle nh;

  ros::Publisher pub = nh.advertise<std_msgs::String>("chatter", 10);
  ros::Rate rate(10);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    ss << "hello ROS topic " << count++;
    msg.data = ss.str();

    ROS_INFO("%s", msg.data.c_str());
    pub.publish(msg);

    ros::spinOnce();
    rate.sleep();
  }

  return 0;
}
