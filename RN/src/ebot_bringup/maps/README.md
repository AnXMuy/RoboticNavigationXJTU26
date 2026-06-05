# maps

Use experiment 3 to build a real map and save it as `nav.yaml` + `nav.pgm`:

```bash
cd ~/test_demo/catkin_ebot/src/ebot_bringup/maps
rosrun map_server map_saver -f nav
```

The checked-in map is only a placeholder so that localization and navigation
launch files have a stable default path before the real robot map is generated.
