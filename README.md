# tb3_slam_nav_pkg

A ready-to-use ROS 2 Humble package for TurtleBot3 that wraps:
- **SLAM mapping** with `slam_toolbox`
- **Alternative mapping** with `turtlebot3_cartographer`
- **Autonomous navigation** with `Nav2`
- **Goal sending** and **initial pose publishing** from Python

This package is designed for **TurtleBot3 Burger / Waffle / Waffle Pi** and works in:
- **Gazebo simulation**, or
- **a real TurtleBot3** after you bring up the robot on the SBC.

---

## 1) Install dependencies

On Ubuntu 22.04 + ROS 2 Humble:

```bash
sudo apt update
sudo apt install -y \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-slam-toolbox \
  ros-humble-nav2-map-server \
  ros-humble-nav2-simple-commander \
  ros-humble-turtlebot3 \
  ros-humble-turtlebot3-msgs \
  ros-humble-turtlebot3-bringup \
  ros-humble-turtlebot3-gazebo \
  ros-humble-turtlebot3-navigation2 \
  ros-humble-turtlebot3-cartographer
```

Add your TurtleBot3 model to the shell if you want:

```bash
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```

---

## 2) Build the package

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
cp -r /path/to/tb3_slam_nav_pkg .
cd ~/ros2_ws
colcon build --symlink-install --packages-select tb3_slam_nav_pkg
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

---

## 3) Create a map in Gazebo with SLAM Toolbox

Launch the simulator + SLAM:

```bash
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 launch tb3_slam_nav_pkg mapping_slam_toolbox_sim.launch.py
```

Drive the robot manually in another terminal:

```bash
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Save the map when enough area has been explored:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/my_map
```

This creates:
- `~/maps/my_map.yaml`
- `~/maps/my_map.pgm`

---

## 4) Create a map in Gazebo with Cartographer

If you prefer the TurtleBot3 Cartographer pipeline:

```bash
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 launch tb3_slam_nav_pkg mapping_cartographer_sim.launch.py
```

Then drive with teleop and save the map using:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/my_map
```

---

## 5) Navigate on a saved map in Gazebo

Once the map is saved, start localization + Nav2:

```bash
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 launch tb3_slam_nav_pkg navigation_saved_map_sim.launch.py map:=$HOME/maps/my_map.yaml
```

### Set the initial pose

Use RViz **2D Pose Estimate**, or publish it from the terminal:

```bash
ros2 run tb3_slam_nav_pkg set_initial_pose 0.0 0.0 0.0
```

### Send one autonomous goal

```bash
ros2 run tb3_slam_nav_pkg send_goal 1.0 0.5 0.0
```

### Run a simple waypoint patrol

```bash
ros2 run tb3_slam_nav_pkg patrol_waypoints
```

---

## 6) Navigation while mapping

This mode launches Nav2 and SLAM Toolbox together, so the robot can plan while the map is still being built:

```bash
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 launch tb3_slam_nav_pkg nav_while_mapping_sim.launch.py
```

You can then send a goal:

```bash
ros2 run tb3_slam_nav_pkg send_goal 1.0 0.0 0.0
```

---

## 7) Use with a real TurtleBot3 robot

### Terminal A: on the TurtleBot3 SBC

SSH into the robot and launch bringup:

```bash
ssh ubuntu@<ROBOT_IP>
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_bringup robot.launch.py
```

### Terminal B: on the remote PC, create a map

You can use the standard TurtleBot3 Cartographer launch:

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

Or the Nav2-style SLAM Toolbox flow:

```bash
ros2 launch slam_toolbox online_async_launch.py
```

Drive the robot and save the map:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/real_lab_map
```

### Terminal C: run localization + navigation on the saved map

```bash
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 launch tb3_slam_nav_pkg navigation_real_robot.launch.py map:=$HOME/maps/real_lab_map.yaml
```

Set the initial pose in RViz or from terminal, then send goals using:

```bash
ros2 run tb3_slam_nav_pkg send_goal 1.0 0.5 0.0
```

---

## 8) What each launch file does

### `mapping_slam_toolbox_sim.launch.py`
- Starts Gazebo with TurtleBot3
- Starts `slam_toolbox` in online async mapping mode
- Best for **2D LiDAR occupancy-grid mapping** with Nav2

### `mapping_cartographer_sim.launch.py`
- Starts Gazebo with TurtleBot3
- Starts TurtleBot3 Cartographer SLAM
- Good if you want to follow the standard TurtleBot3 Cartographer flow

### `navigation_saved_map_sim.launch.py`
- Starts Gazebo
- Starts TurtleBot3 Navigation2 on a **saved map**
- Use this for localization, path planning, and autonomous navigation

### `nav_while_mapping_sim.launch.py`
- Starts Gazebo
- Starts Nav2 without AMCL/map server
- Starts `slam_toolbox` to provide `/map` and `map -> odom`
- Use this when you want **planning while the map is still being built**

### `navigation_real_robot.launch.py`
- Starts the TurtleBot3 Navigation2 stack on a real robot using a saved map

---

## 9) Python nodes in this package

### `send_goal`
Sends a single `NavigateToPose` goal through the Nav2 Simple Commander API.

```bash
ros2 run tb3_slam_nav_pkg send_goal <x> <y> [yaw_radians]
```

### `set_initial_pose`
Publishes the AMCL initial pose.

```bash
ros2 run tb3_slam_nav_pkg set_initial_pose <x> <y> [yaw_radians]
```

### `patrol_waypoints`
Sends a hard-coded waypoint sequence using `followWaypoints()`.

```bash
ros2 run tb3_slam_nav_pkg patrol_waypoints
```

Edit the `WAYPOINTS` list in:

```bash
tb3_slam_nav_pkg/patrol_waypoints.py
```

---

## 10) Sensor requirements

### For LiDAR-based 2D mapping/navigation
You need:
- `/scan` (`sensor_msgs/LaserScan`)
- wheel odometry / TF (`odom -> base_footprint`)
- robot frames (`base_link`, `base_footprint`, sensors)

This is the standard TurtleBot3 flow.

### For camera-only or RGB-D mapping
This package does **not** include an RTAB-Map launch.

If you want **camera / RGB-D SLAM**:
- keep Nav2 for path planning and control,
- replace the SLAM backend with **RTAB-Map**,
- provide camera topics, depth topics, camera info, and odometry,
- publish `/map` and the `map -> odom` transform for Nav2.

---

## 11) Typical workflow summary

### A. Build a map
1. Start simulation or bring up the real robot.
2. Start `slam_toolbox` or `cartographer`.
3. Move the robot so LiDAR scans cover the environment.
4. Save the map using `map_saver_cli`.

### B. Autonomous navigation
1. Launch Nav2 with the saved map.
2. Set the initial pose.
3. Send a goal or waypoint list.
4. Nav2 localizes, plans a path, avoids obstacles, and drives the robot.

---

## 12) Notes

- If RViz shows time warnings in simulation, make sure `use_sim_time:=true` is set.
- If navigation does not start, verify the initial pose is set.
- If mapping looks distorted, verify TF and `/scan` are correct.
- For real robots, run TurtleBot3 bringup on the SBC and Nav2/SLAM on the remote PC.

