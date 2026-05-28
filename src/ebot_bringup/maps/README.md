Put generated map files here.

Default map file names expected by launch files:
- `nav.pgm`
- `nav.yaml`

Example save command after mapping:

```bash
cd ~/test_demo/catkin_ebot/src/ebot_bringup/maps
rosrun map_server map_saver -f nav
```

If you use another map name, override in launch:

```bash
roslaunch ebot_bringup test_amcl.launch map:=your_map.yaml
roslaunch ebot_bringup test_nav.launch map:=your_map.yaml
```
