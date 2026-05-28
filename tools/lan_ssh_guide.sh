#!/usr/bin/env bash

set -euo pipefail

current_user="$(id -un)"
host_name="$(hostname)"
ip_list="$(hostname -I 2>/dev/null | xargs || true)"
default_iface="$(ip route 2>/dev/null | awk '/default/ {print $5; exit}')"
ssh_service_name=""
ssh_service_state="unknown"

if systemctl list-unit-files 2>/dev/null | grep -q '^ssh\.service'; then
  ssh_service_name="ssh"
elif systemctl list-unit-files 2>/dev/null | grep -q '^sshd\.service'; then
  ssh_service_name="sshd"
fi

if [ -n "${ssh_service_name}" ]; then
  ssh_service_state="$(systemctl is-active "${ssh_service_name}" 2>/dev/null || true)"
fi

print_title() {
  printf '\n==== %s ====\n' "$1"
}

print_title "group12 LAN SSH Guide"
printf 'user      : %s\n' "${current_user}"
printf 'hostname  : %s\n' "${host_name}"
printf 'ip        : %s\n' "${ip_list:-not detected}"
printf 'interface : %s\n' "${default_iface:-not detected}"
printf 'ssh svc   : %s\n' "${ssh_service_name:-not detected}"
printf 'ssh state : %s\n' "${ssh_service_state}"

print_title "Step 1: Make Sure The Board And Your Computer Are In The Same LAN"
cat <<EOF
- Put the board and your laptop on the same router, hotspot, or switch.
- On this board, the detected IP is:
  ${ip_list:-IP not detected}
- If the IP is empty, check network first with:
  ip addr
  ping 8.8.8.8
EOF

print_title "Step 2: Ensure SSH Server Exists And Is Running On The Board"
if [ "${ssh_service_state}" = "active" ]; then
  cat <<EOF
SSH server already looks active on this board.
You can go directly to Step 3.
EOF
else
  cat <<EOF
If SSH is not installed or not started, run these commands on the board:

sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh --no-pager

If your system uses sshd instead of ssh, replace the service name accordingly.
EOF
fi

print_title "Step 3: Connect From Your Computer"
cat <<EOF
Run this on your laptop terminal:

ssh ${current_user}@${ip_list%% *}

If you want to specify the hostname instead of the IP, try:

ssh ${current_user}@${host_name}.local

On first connection, answer:
  yes
when asked whether to trust the host key.
EOF

print_title "Step 4: Common Helpful Commands"
cat <<EOF
Copy a file from laptop to board:
scp local_file ${current_user}@${ip_list%% *}:/home/${current_user}/

Copy a file from board to laptop:
scp ${current_user}@${ip_list%% *}:/home/${current_user}/remote_file .

Open an interactive remote shell:
ssh ${current_user}@${ip_list%% *}
EOF

print_title "If Connection Fails"
cat <<EOF
1. On your laptop:
   ping ${ip_list%% *}

2. On the board:
   sudo systemctl status ${ssh_service_name:-ssh} --no-pager
   ss -tlnp | grep ':22'

3. If firewall is enabled on the board:
   sudo ufw allow ssh

4. If the IP changed after reboot, rerun this script on the board.
EOF

print_title "Recommended Workflow For This Project"
cat <<EOF
- Use SSH for terminal control on the board.
- Run RViz on your own computer if the board's GUI resources are limited.
- Keep one SSH tab for bringup, one for lidar/navigation, one for logs.
EOF

print_title "Done"
echo "This script only prints guidance and detected connection info."
