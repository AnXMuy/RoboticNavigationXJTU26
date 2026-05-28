#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REAL_ONLY_PKGS=(
  "src/ebot_base/turn_on_wheeltec_robot"
  "src/ebot_sensors/ydlidar_ros_driver"
  "src/ebot_navigation/rf2o_laser_odometry"
)

echo "[profile] Switching to full real-robot build profile"
for rel in "${REAL_ONLY_PKGS[@]}"; do
  pkg_dir="$ROOT_DIR/$rel"
  if [[ -f "$pkg_dir/CATKIN_IGNORE" ]]; then
    rm -f "$pkg_dir/CATKIN_IGNORE"
    echo "  - enable $rel"
  else
    echo "  - already enabled $rel"
  fi
done

echo "[profile] Done. catkin_make will include real robot driver packages."
