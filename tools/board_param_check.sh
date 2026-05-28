#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

BRINGUP_LAUNCH="${REPO_ROOT}/src/ebot_bringup/launch/bringup.launch"
STATIC_TF_LAUNCH="${REPO_ROOT}/src/ebot_bringup/launch/static_tf.launch"
LIDAR_YAML="${REPO_ROOT}/src/ebot_bringup/config/lidar/ydlidar_real.yaml"
AMCL_YAML="${REPO_ROOT}/src/ebot_bringup/config/localization/amcl_real.yaml"
RF2O_YAML="${REPO_ROOT}/src/ebot_bringup/config/localization/rf2o.yaml"
HECTOR_YAML="${REPO_ROOT}/src/ebot_bringup/config/slam/hector_mapping.yaml"
MAP_YAML="${REPO_ROOT}/src/ebot_bringup/maps/nav.yaml"

print_title() {
  printf '\n==== %s ====\n' "$1"
}

read_launch_default() {
  local file="$1"
  local arg_name="$2"
  awk -v key="${arg_name}" '
    $0 ~ "<arg name=\"" key "\" " {
      if (match($0, /default="[^"]+"/)) {
        value = substr($0, RSTART + 9, RLENGTH - 10)
        print value
        exit
      }
    }
  ' "${file}"
}

read_yaml_value() {
  local file="$1"
  local key="$2"
  awk -F':' -v search_key="${key}" '
    $1 ~ "^[[:space:]]*" search_key "[[:space:]]*$" {
      value = $2
      sub(/^[[:space:]]+/, "", value)
      sub(/[[:space:]]+$/, "", value)
      print value
      exit
    }
  ' "${file}"
}

show_file_value() {
  local label="$1"
  local value="$2"
  local file="$3"
  printf '%-22s %s\n' "${label}:" "${value}"
  printf '  file: %s\n' "${file}"
}

print_title "group12 Real-Robot Parameter Checker"
printf 'repo root: %s\n' "${REPO_ROOT}"

print_title "Current Config In This Repository"
show_file_value "base_port" "$(read_launch_default "${BRINGUP_LAUNCH}" "base_port")" "${BRINGUP_LAUNCH}"
show_file_value "base_baudrate" "$(read_launch_default "${BRINGUP_LAUNCH}" "base_baudrate")" "${BRINGUP_LAUNCH}"
show_file_value "wheel_odom_frame_id" "$(read_launch_default "${BRINGUP_LAUNCH}" "wheel_odom_frame_id")" "${BRINGUP_LAUNCH}"
show_file_value "wheel_robot_frame_id" "$(read_launch_default "${BRINGUP_LAUNCH}" "wheel_robot_frame_id")" "${BRINGUP_LAUNCH}"
show_file_value "wheel_odom_topic" "$(read_launch_default "${BRINGUP_LAUNCH}" "wheel_odom_topic")" "${BRINGUP_LAUNCH}"

show_file_value "laser port" "$(read_yaml_value "${LIDAR_YAML}" "port")" "${LIDAR_YAML}"
show_file_value "laser frame_id" "$(read_yaml_value "${LIDAR_YAML}" "frame_id")" "${LIDAR_YAML}"
show_file_value "laser baudrate" "$(read_yaml_value "${LIDAR_YAML}" "baudrate")" "${LIDAR_YAML}"
show_file_value "laser sample_rate" "$(read_yaml_value "${LIDAR_YAML}" "sample_rate")" "${LIDAR_YAML}"
show_file_value "laser reversion" "$(read_yaml_value "${LIDAR_YAML}" "reversion")" "${LIDAR_YAML}"
show_file_value "laser inverted" "$(read_yaml_value "${LIDAR_YAML}" "inverted")" "${LIDAR_YAML}"
show_file_value "laser range_max" "$(read_yaml_value "${LIDAR_YAML}" "range_max")" "${LIDAR_YAML}"
show_file_value "laser frequency" "$(read_yaml_value "${LIDAR_YAML}" "frequency")" "${LIDAR_YAML}"

show_file_value "laser_x" "$(read_launch_default "${STATIC_TF_LAUNCH}" "laser_x")" "${STATIC_TF_LAUNCH}"
show_file_value "laser_y" "$(read_launch_default "${STATIC_TF_LAUNCH}" "laser_y")" "${STATIC_TF_LAUNCH}"
show_file_value "laser_z" "$(read_launch_default "${STATIC_TF_LAUNCH}" "laser_z")" "${STATIC_TF_LAUNCH}"
show_file_value "laser_yaw" "$(read_launch_default "${STATIC_TF_LAUNCH}" "laser_yaw")" "${STATIC_TF_LAUNCH}"
show_file_value "laser_pitch" "$(read_launch_default "${STATIC_TF_LAUNCH}" "laser_pitch")" "${STATIC_TF_LAUNCH}"
show_file_value "laser_roll" "$(read_launch_default "${STATIC_TF_LAUNCH}" "laser_roll")" "${STATIC_TF_LAUNCH}"

print_title "Detected Serial Devices On This Board"
if [ -d /dev/serial/by-path ]; then
  ls -l /dev/serial/by-path
else
  echo "/dev/serial/by-path does not exist on this system."
fi

print_title "What You Must Check Before Real-Robot Test"
cat <<EOF
1. Base serial port
   file: ${BRINGUP_LAUNCH}
   key : base_port
   action:
     Compare the configured path with the real chassis serial path listed above.
     If the chassis cable is plugged into a different USB port, this path must be updated.

2. Lidar serial port
   file: ${LIDAR_YAML}
   key : port
   action:
     Compare it with the real lidar serial path listed above.
     If the lidar path is wrong, /scan will not come out.

3. Lidar electrical parameters
   file: ${LIDAR_YAML}
   keys: baudrate, sample_rate, isSingleChannel, support_motor_dtr
   action:
     These must match your lidar model's spec sheet.
     If your lidar is not the same model as the lab handout, check these first.

4. Lidar scan direction
   file: ${LIDAR_YAML}
   keys: reversion, inverted
   action:
     If RViz shows the scan mirrored or reversed, change these two booleans.

5. Static TF between base and lidar
   file: ${STATIC_TF_LAUNCH}
   keys: laser_x, laser_y, laser_z, laser_yaw, laser_pitch, laser_roll
   action:
     If your lidar mounting position or facing direction differs from the current robot,
     these values must be updated.
     A wrong TF will directly damage mapping and localization quality.

6. Map file for localization
   file: ${MAP_YAML}
   action:
     Experiment 4 needs nav.yaml and nav.pgm under src/ebot_bringup/maps/.
     If you have not saved the map yet, run mapping first.

7. Optional localization tuning later
   files:
     ${AMCL_YAML}
     ${RF2O_YAML}
     ${HECTOR_YAML}
   action:
     These usually do not need immediate edits before the first run.
     Change them only when you start tuning AMCL, RF2O, or Hector behavior.
EOF

print_title "Recommended Edit Commands"
cat <<EOF
nano "${BRINGUP_LAUNCH}"
nano "${STATIC_TF_LAUNCH}"
nano "${LIDAR_YAML}"
EOF

print_title "Quick Real-Robot Bringup Order"
cat <<EOF
1. roslaunch ebot_bringup bringup.launch
2. roslaunch ebot_bringup my_lidar.launch
3. Experiment 3 mapping:
   roslaunch ebot_bringup slam_hector.launch
4. Experiment 4 localization:
   roslaunch ebot_bringup test_amcl.launch
EOF

print_title "Done"
echo "This script only checks and explains. It does not modify any file."
