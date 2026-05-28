#ifndef TF2_SENSOR_MSGS_H
#define TF2_SENSOR_MSGS_H

#include <limits>
#include <string>

#include <Eigen/Dense>
#include <geometry_msgs/TransformStamped.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/point_cloud2_iterator.h>

#include <tf2/LinearMath/Transform.h>
#include <tf2/convert.h>

namespace tf2
{

template<>
inline void doTransform(const sensor_msgs::PointCloud2& p_in,
                        sensor_msgs::PointCloud2& p_out,
                        const geometry_msgs::TransformStamped& t_in)
{
  p_out = p_in;
  p_out.header = t_in.header;

  Eigen::Transform<float, 3, Eigen::Affine> t =
      Eigen::Translation3f(t_in.transform.translation.x,
                           t_in.transform.translation.y,
                           t_in.transform.translation.z) *
      (Eigen::Quaternion<float>(t_in.transform.rotation.w,
                                t_in.transform.rotation.x,
                                t_in.transform.rotation.y,
                                t_in.transform.rotation.z));

  sensor_msgs::PointCloud2ConstIterator<float> x_in(p_in, "x");
  sensor_msgs::PointCloud2ConstIterator<float> y_in(p_in, "y");
  sensor_msgs::PointCloud2ConstIterator<float> z_in(p_in, "z");

  sensor_msgs::PointCloud2Iterator<float> x_out(p_out, "x");
  sensor_msgs::PointCloud2Iterator<float> y_out(p_out, "y");
  sensor_msgs::PointCloud2Iterator<float> z_out(p_out, "z");

  for (; x_in != x_in.end(); ++x_in, ++y_in, ++z_in, ++x_out, ++y_out, ++z_out)
  {
    Eigen::Vector3f point = t * Eigen::Vector3f(*x_in, *y_in, *z_in);
    *x_out = point.x();
    *y_out = point.y();
    *z_out = point.z();
  }

  sensor_msgs::PointCloud2ConstIterator<float> vx_in(p_in, "vp_x");
  sensor_msgs::PointCloud2ConstIterator<float> vy_in(p_in, "vp_y");
  sensor_msgs::PointCloud2ConstIterator<float> vz_in(p_in, "vp_z");
  sensor_msgs::PointCloud2Iterator<float> vx_out(p_out, "vp_x");
  sensor_msgs::PointCloud2Iterator<float> vy_out(p_out, "vp_y");
  sensor_msgs::PointCloud2Iterator<float> vz_out(p_out, "vp_z");

  if (vx_in != vx_in.end() && vy_in != vy_in.end() && vz_in != vz_in.end())
  {
    for (; vx_in != vx_in.end(); ++vx_in, ++vy_in, ++vz_in, ++vx_out, ++vy_out, ++vz_out)
    {
      Eigen::Vector3f point = t * Eigen::Vector3f(*vx_in, *vy_in, *vz_in);
      *vx_out = point.x();
      *vy_out = point.y();
      *vz_out = point.z();
    }
  }

  Eigen::Transform<float, 3, Eigen::Affine> r =
      Eigen::Translation3f(0.0, 0.0, 0.0) *
      (Eigen::Quaternion<float>(t_in.transform.rotation.w,
                                t_in.transform.rotation.x,
                                t_in.transform.rotation.y,
                                t_in.transform.rotation.z));

  sensor_msgs::PointCloud2ConstIterator<float> nx_in(p_in, "normal_x");
  sensor_msgs::PointCloud2ConstIterator<float> ny_in(p_in, "normal_y");
  sensor_msgs::PointCloud2ConstIterator<float> nz_in(p_in, "normal_z");
  sensor_msgs::PointCloud2Iterator<float> nx_out(p_out, "normal_x");
  sensor_msgs::PointCloud2Iterator<float> ny_out(p_out, "normal_y");
  sensor_msgs::PointCloud2Iterator<float> nz_out(p_out, "normal_z");

  if (nx_in != nx_in.end() && ny_in != ny_in.end() && nz_in != nz_in.end())
  {
    for (; nx_in != nx_in.end(); ++nx_in, ++ny_in, ++nz_in, ++nx_out, ++ny_out, ++nz_out)
    {
      Eigen::Vector3f point = r * Eigen::Vector3f(*nx_in, *ny_in, *nz_in);
      *nx_out = point.x();
      *ny_out = point.y();
      *nz_out = point.z();
    }
  }
}

template<>
inline const ros::Time& getTimestamp(const sensor_msgs::PointCloud2& p)
{
  return p.header.stamp;
}

template<>
inline const std::string& getFrameId(const sensor_msgs::PointCloud2& p)
{
  return p.header.frame_id;
}

template<>
inline void toMsg(const sensor_msgs::PointCloud2& in, sensor_msgs::PointCloud2& out)
{
  out = in;
}

template<>
inline void fromMsg(const sensor_msgs::PointCloud2& msg, sensor_msgs::PointCloud2& out)
{
  out = msg;
}

}  // namespace tf2

#endif
