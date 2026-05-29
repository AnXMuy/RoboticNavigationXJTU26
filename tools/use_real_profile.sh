#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REAL_ONLY_PKGS=(
  "src/ebot_base/turn_on_wheeltec_robot"
  "src/ebot_sensors/ydlidar_ros_driver"
  "src/ebot_navigation/rf2o_laser_odometry"
)
SIM_PKGS=(
  "src/robot_sim"
  "src/vehicle_sim"
)

echo "[profile] Enforcing real-robot-only build profile"
for rel in "${REAL_ONLY_PKGS[@]}"; do
  pkg_dir="$ROOT_DIR/$rel"
  if [[ -f "$pkg_dir/CATKIN_IGNORE" ]]; then
    rm -f "$pkg_dir/CATKIN_IGNORE"
    echo "  - enable $rel"
  else
    echo "  - already enabled $rel"
  fi
done

for rel in "${SIM_PKGS[@]}"; do
  pkg_dir="$ROOT_DIR/$rel"
  if [[ -d "$pkg_dir" ]]; then
    touch "$pkg_dir/CATKIN_IGNORE"
    echo "  - ignore $rel (simulation disabled)"
  fi
done

echo "[profile] Done. catkin_make will compile only real-robot workflow packages."
