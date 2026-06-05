#include <ebotController.h>

#include <algorithm>
#include <cmath>
#include <limits>

namespace ebot_controller {

ebotControllerNode::ebotControllerNode(ros::NodeHandle &n)
{
    ros::NodeHandle private_nh("~");
    private_nh.param("odom_frame", odom_frame_, std::string("odom"));
    private_nh.param("base_frame", base_frame_, std::string("base_footprint"));
    private_nh.param("global_path_topic", global_path_topic_, std::string("/move_base/GlobalPlanner/plan"));
    private_nh.param("kp", kp_, 0.85);
    private_nh.param("ki", ki_, 0.02);
    private_nh.param("kd", kd_, 0.18);
    private_nh.param("target_speed", target_speed_, 0.45);
    private_nh.param("control_period", control_period_, 0.02);
    private_nh.param("lookahead_distance", lookahead_distance_, 0.9);
    private_nh.param("min_lookahead_index", min_lookahead_index_, 4);
    private_nh.param("max_steering_theta", max_steering_theta_, 0.523599);

    lateral_pid_.setParams(kp_, ki_, kd_, -max_steering_theta_, max_steering_theta_);

    sub_final_waypoints = n.subscribe("/base_waypoints", 1, &ebotControllerNode::lane_cb, this);
    sub_global_path = n.subscribe(global_path_topic_, 1, &ebotControllerNode::path_cb, this);
    sub_pose = n.subscribe("/odom", 1, &ebotControllerNode::pose_cb_test, this);
    pub_twist_cmd = n.advertise<geometry_msgs::Twist>("/cmd_vel", 1);

    control_timer_ = n.createTimer(ros::Duration(control_period_), &ebotControllerNode::ControlCallback, this);
}

double ebotControllerNode::getdistance(const geometry_msgs::Point &a, const geometry_msgs::Point &b) const
{
    const double dx = a.x - b.x;
    const double dy = a.y - b.y;
    return std::sqrt(dx * dx + dy * dy);
}

void ebotControllerNode::pose_cb_test(const nav_msgs::Odometry msg)
{
    my_odom = msg;
}

void ebotControllerNode::lane_cb(const styx_msgs::Lane::ConstPtr &received_curve)
{
    final_waypoints.header.frame_id = received_curve->header.frame_id.empty() ? odom_frame_ : received_curve->header.frame_id;
    final_waypoints.header.stamp = ros::Time::now();
    final_waypoints.poses.resize(received_curve->waypoints.size());

    for (size_t i = 0; i < received_curve->waypoints.size(); ++i) {
        final_waypoints.poses[i].header = final_waypoints.header;
        final_waypoints.poses[i].pose = received_curve->waypoints[i].pose.pose;
    }
}

void ebotControllerNode::path_cb(const nav_msgs::Path::ConstPtr &msg)
{
    if (msg->poses.empty()) {
        return;
    }

    final_waypoints = *msg;
    if (final_waypoints.header.frame_id.empty()) {
        final_waypoints.header.frame_id = odom_frame_;
    }
}

int ebotControllerNode::nearest_point_index() const
{
    if (final_waypoints.poses.empty()) {
        return -1;
    }

    geometry_msgs::Point current_pose;
    current_pose.x = my_odom.pose.pose.position.x;
    current_pose.y = my_odom.pose.pose.position.y;

    int nearest_index = 0;
    double min_distance = std::numeric_limits<double>::max();
    for (size_t i = 0; i < final_waypoints.poses.size(); ++i) {
        const double distance = getdistance(current_pose, final_waypoints.poses[i].pose.position);
        if (distance < min_distance) {
            min_distance = distance;
            nearest_index = static_cast<int>(i);
        }
    }

    int target_index = std::min(
        nearest_index + min_lookahead_index_,
        static_cast<int>(final_waypoints.poses.size()) - 1
    );
    double accumulated = 0.0;
    for (int i = nearest_index; i + 1 < static_cast<int>(final_waypoints.poses.size()); ++i) {
        accumulated += getdistance(final_waypoints.poses[i].pose.position, final_waypoints.poses[i + 1].pose.position);
        target_index = i + 1;
        if (accumulated >= lookahead_distance_) {
            break;
        }
    }

    return target_index;
}

void ebotControllerNode::ControlCallback(const ros::TimerEvent& event)
{
    const int target_index = nearest_point_index();
    if (target_index < 0) {
        return;
    }

    geometry_msgs::PointStamped odom_point;
    odom_point.header.frame_id = final_waypoints.header.frame_id.empty() ? odom_frame_ : final_waypoints.header.frame_id;
    odom_point.header.stamp = ros::Time(0);
    odom_point.point = final_waypoints.poses[target_index].pose.position;

    geometry_msgs::PointStamped vehicle_frame_point;
    try {
        tf_listener_.transformPoint(base_frame_, odom_point, vehicle_frame_point);
    } catch (tf::TransformException& ex) {
        ROS_WARN_THROTTLE(1.0, "PID controller transform failed: %s", ex.what());
        return;
    }

    const double dt = std::max(1e-3, (event.current_real - event.last_real).toSec());
    const double lateral_error = vehicle_frame_point.point.y;
    const double steering_theta = lateral_pid_.step(lateral_error, dt);

    geometry_msgs::Twist cmd_twist;
    cmd_twist.linear.x = target_speed_;
    cmd_twist.angular.z = steering_theta;
    pub_twist_cmd.publish(cmd_twist);

    ROS_INFO_THROTTLE(
        0.5,
        "target=%d lateral_error=%.3f steering=%.3f speed=%.3f",
        target_index,
        lateral_error,
        steering_theta,
        target_speed_
    );
}

}
