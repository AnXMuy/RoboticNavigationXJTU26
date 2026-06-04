#ifndef EBOT_CONTROLLER_H
#define EBOT_CONTROLLER_H

#include "PidControl.h"

#include <geometry_msgs/Point.h>
#include <geometry_msgs/PointStamped.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <nav_msgs/Path.h>
#include <ros/ros.h>
#include <string>
#include <styx_msgs/Lane.h>
#include <tf/transform_listener.h>

namespace ebot_controller {

class ebotControllerNode {
public:
    explicit ebotControllerNode(ros::NodeHandle &n);

private:
    void ControlCallback(const ros::TimerEvent& event);
    void lane_cb(const styx_msgs::Lane::ConstPtr &msg);
    void path_cb(const nav_msgs::Path::ConstPtr &msg);
    void pose_cb_test(const nav_msgs::Odometry msg);
    int nearest_point_index() const;
    double getdistance(const geometry_msgs::Point &a, const geometry_msgs::Point &b) const;

    ros::Publisher pub_twist_cmd;
    ros::Subscriber sub_final_waypoints;
    ros::Subscriber sub_global_path;
    ros::Subscriber sub_pose;
    ros::Timer control_timer_;

    tf::TransformListener tf_listener_;
    PidControl lateral_pid_;

    nav_msgs::Path final_waypoints;
    nav_msgs::Odometry my_odom;

    std::string odom_frame_;
    std::string base_frame_;
    std::string global_path_topic_;

    double kp_;
    double ki_;
    double kd_;
    double target_speed_;
    double control_period_;
    double lookahead_distance_;
    double max_steering_theta_;
    int min_lookahead_index_;
};

}

#endif
