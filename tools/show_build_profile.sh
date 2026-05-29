#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REAL_PKGS=(
  "src/ebot_base/turn_on_wheeltec_robot"
  "src/ebot_sensors/ydlidar_ros_driver"
  "src/ebot_navigation/rf2o_laser_odometry"
)
SIM_PKGS=(
  "src/robot_sim"
  "src/vehicle_sim"
)

echo "Build profile status (real-robot-only):"
for rel in "${REAL_PKGS[@]}"; do
  if [[ -f "$ROOT_DIR/$rel/CATKIN_IGNORE" ]]; then
    echo "  [DISABLED] $rel is ignored (unexpected for real profile)"
  else
    echo "  [REAL]     $rel is enabled"
  fi
done

for rel in "${SIM_PKGS[@]}"; do
  if [[ -f "$ROOT_DIR/$rel/CATKIN_IGNORE" ]]; then
    echo "  [SIM_OFF]  $rel is ignored"
  else
    echo "  [WARNING]  $rel is enabled (expected ignored in real-only workspace)"
  fi
done
