#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REAL_ONLY_PKGS=(
  "src/ebot_base/turn_on_wheeltec_robot"
  "src/ebot_sensors/ydlidar_ros_driver"
  "src/ebot_navigation/rf2o_laser_odometry"
)

echo "[profile] Switching to simulation-only build profile"
for rel in "${REAL_ONLY_PKGS[@]}"; do
  pkg_dir="$ROOT_DIR/$rel"
  if [[ -d "$pkg_dir" ]]; then
    touch "$pkg_dir/CATKIN_IGNORE"
    echo "  - ignore $rel"
  fi
done

echo "[profile] Done. You can now run catkin_make without real hardware dependencies."
