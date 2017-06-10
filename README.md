# c3po_ws
ROS Gazebo robot simulation

# Prerequisites
```
sudo apt-get install ros-kinetic-full-desktop
sudo apt-get install ros-kinetic-ros-control ros-kinetic-ros-controllers
sudo apt-get install ros-kinetic-gazebo-ros ros-kinetic-gazebo-ros-control
sudo apt-get install ros-kinetic-lms1xx	//for range scan laser
```

# Usage
- clone this project
- `catkin_init_workspace` in src dir
- `catkin_make` in root dir
- `source ~/PATH_TO_WS/devel/setup.bash` in every terminal
- `echo "source ~/PATH_TO_WS/devel/setup.bash" >> ~/.bashrc`, then `source ~/.bashrc` for current terminal
- run using `roslaunch mybot_gazebo mybot_world.launch`
### Teleoperation
Control the robot manually using the turtlesim teleop node:
 
`rosrun turtlesim turtle_teleop_key /turtle1/cmd_vel:=/mybot/cmd_vel`


# Setup from sample project

### Step 1: Install sample project
Follow [this](http://www.generationrobots.com/blog/en/2015/02/robotic-simulation-scenarios-with-gazebo-and-ros/) installation.

Download from GitHub
clone into src/

Setup:

in new console always do: `source ~/PATH_TO_WS/devel/setup.bash` or add the command to ~/.bashrc

1. in src folder --> `workspace init`
2. im workspace root folder --> `catkin_make`

### Step 2: Fixes due to Migration to ROS Kinetic
#### Explicitly add a hardware interface to the hinge's joint
1. Open ~/PATH_TO_WS/src/mybot_description/urdf/macros.xarco
2. Inside the tag:
	
    ```xml
     <transmission name="${lr}_trans">
        <type>transmission_interface/SimpleTransmission</type>
        <joint name="${lr}_wheel_hinge"/>
        <actuator name="${lr}Motor">
          <hardwareInterface>EffortJointInterface</hardwareInterface>
          <mechanicalReduction>10</mechanicalReduction>
        </actuator>
     </transmission>
    ```
	
	replace 
	```xml
	<joint name="${lr}_wheel_hinge"/>
	```
	with
	```xml
    <joint name="${lr}_wheel_hinge">
            <hardwareInterface>EffortJointInterface</hardwareInterface>
        </joint>
    ```

#### Remove the gap between the robot and the ground plane
In the sample project, there exists a gap between the robot and the ground plane. 
This is due to the configuration of the wheels inside 
`~/PATH_TO_WS/src/mybot_description/urdf/macros.xacro`. Instead of pitching and yawing the wheel 
cylinders, we need to just roll the cylinder. This avoid a calculation error due to the inaccuracy 
of pi. Inside the tag:
```xml
<macro name="wheel" params="lr tY">
```
replace all occurrences (inside `<collision>`, `<visual>` and `<inertial>`) of 
```xml
<origin xyz="0 0 0" rpy="0 ${PI/2} ${PI/2}" />
```

with 
```xml
<origin xyz="0 0 0" rpy="${PI/2} 0 0"/>
```

### Step 3: Setup environment
##### Option 1: Gas Station

Open `~/PATH_TO_WS/src/mybot_gazebo/worlds/mybot.world` and inside the `<world>`-tag add:
```xml
<include>
    <uri>model://gas_station</uri>
    <name>gas_station</name>
    <pose>-2.0 7.0 0 0 0 0</pose>
</include>
```

##### Option 2: Race track

 replace mybot.world in ~/PATH_TO_WS/src/mybot_gazebo/worlds/ with this file from 
 https://github.com/jackal/jackal_simulator/blob/indigo-devel/jackal_gazebo/worlds/jackal_race.world
 (remember renaming it to mybot.world)


		
		
# Laser Scan
This part of the tutorial is for adding a front laser and using the data we get from it to automate driving

1. add a description file for the laser mount in our case lms1xx
	- you can clone the file from https://github.com/jackal/jackal/blob/indigo-devel/jackal_description/urdf/accessories/sick_lms1xx_mount.urdf.xacro
	- remove the <visual> from the brackets link: 
	```xml
	<link name="${prefix}_laser_mount">
      <visual>
        <origin xyz="0 0 0" rpy="0 0 0" />
        <geometry>
          <mesh filename="package://jackal_description/meshes/sick-lms1xx-bracket.stl" />
        </geometry>
        <material name="dark_grey" />
      </visual>
    </link>
	```
	becomes 
	```xml
	<link name="${prefix}_laser_mount"></link>
	```
	
2. in mybot.xacro add the front laser
	- the code you need to include:
	    ```xml
        <!-- FRONT LASER -->
       	<xacro:include filename="$(find mybot_description)/urdf/sick_lms1xx_mount.urdf.xacro" />
       	<sick_lms1xx_mount prefix="front"
       			topic="mybot/front_laser/scan"/>
        
       	<joint name="front_laser_mount_joint" type="fixed">
       			<origin xyz="0 0 0"  rpy="0 0 0" />
       			<!--parent link="front_mount" />-->
           		<parent link="camera" />
           		<child link="front_laser_mount" />
       	</joint>
        ```
		
		
now the laser is ready for use. At the moment it scans a wide radius which we do not want to use so we set a filter to the laser

1. add filter to mybot_world.launch
	
	<node pkg="laser_filters" type="scan_to_scan_filter_chain"
	   name="laser_filter_front">
		<rosparam command="load" file="$(find mybot_gazebo)/launch/laserscan_filter_front.yaml" />
		<remap from="scan" to="mybot/front_laser/scan" />
		<remap from="scan_filtered" to="mybot/front_laser/scan_filtered" />
   </node>
   
2. describe the filter we need in a yaml file

	scan_filter_chain:
	- name: laser_cutoff_front
	type: laser_filters/LaserScanAngularBoundsFilter
	params:
		lower_angle: -0.78539816339
		upper_angle: 0.78539816339 
		
now when the robot is running we can subscribe to the topic mybot/front_laser/scan_filtered and we get values for the laser in front of the robot


create new package for scripts

# Autonomous Controller (control.py)
On every laser scan tick, the central and peripheral ranges are checked. If a certain threshold is crossed, the corresponding angular velocity to counteract is added to the current msg, else the robot just goes straight forward.
--> to be optimized for all situations, to be merged with Miron's approach (autonom.py)
