#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKGS=(
  "src/ebot_base/turn_on_wheeltec_robot"
  "src/ebot_sensors/ydlidar_ros_driver"
  "src/ebot_navigation/rf2o_laser_odometry"
)

echo "Build profile status:"
for rel in "${PKGS[@]}"; do
  if [[ -f "$ROOT_DIR/$rel/CATKIN_IGNORE" ]]; then
    echo "  [SIM_ONLY] $rel is ignored"
  else
    echo "  [REAL]     $rel is enabled"
  fi
done
