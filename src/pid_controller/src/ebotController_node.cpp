#include <ebotController.h>
#include <ros/ros.h>

ebot_controller::ebotControllerNode* node;

int main(int argc, char** argv)
{
  ros::init(argc, argv, "ebot_controller");
  ros::NodeHandle n;

  node = new ebot_controller::ebotControllerNode(n);
  ros::spin();
}