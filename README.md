# c3po_ws
ROS Gazebo robot simulation

# Prerequisites
- sudo apt-get install ros-kinetic-full-desktop
- sudo apt-get install ros-kinetic-ros-control ros-kinetic-ros-controllers
- sudo apt-get install ros-kinetic-gazebo-ros ros-kinetic-gazebo-ros-control
- sudo apt-get install ros-kinetic-lms1xx	//for range scan laser

# Usage
- clone this project
- 'catkin_init_workspace' in src dir
- 'catkin_make' in root dir
- 'source ~/<YourWorkspace>/devel/setup.bash' in every terminal
- 'echo "source ~/<YourWorkspace>/devel/setup.bash" >> ~/.bashrc', then 'source ~/.bashrc' for current terminal
- run using 'roslaunch mybot_gazebo mybot_world.launch'


# Setup from sample project
Follow the isntallation from http://www.generationrobots.com/blog/en/2015/02/robotic-simulation-scenarios-with-gazebo-and-ros/

Download from GitHub
clone into src/

Setup:

in new console always do: source ~/<YourWorkspace>/devel/setup.bash OR add the command to ~/.bashrc

1. in src -->workspace init
2. im workspace --> catkin_make
3. sudo apt-get install ros-kinetic-ros-control ros-kinetic-ros-controllers
4. sudo apt-get install ros-kinetic-gazebo-ros ros-kinetic-gazebo-ros-control

go to mybot_description/urdf/macros.xarco

	in:
	<transmission name="${lr}_trans">
        <type>transmission_interface/SimpleTransmission</type>
        <joint name="${lr}_wheel_hinge"/>
        <actuator name="${lr}Motor">
          <hardwareInterface>EffortJointInterface</hardwareInterface>
          <mechanicalReduction>10</mechanicalReduction>
        </actuator>
      </transmission>

	replace <joint name="${lr}_wheel_hinge"/>
	with
	<joint name="${lr}_wheel_hinge">
        <hardwareInterface>EffortJointInterface</hardwareInterface>
    </joint>

    --> this adds a hardware interface to the hinge joint

    in: 
	<macro name="wheel" params="lr tY">
		replace all occurances (inside collision, visual and inertial) of 
			<origin xyz="0 0 0" rpy="0 ${PI/2} ${PI/2}" /> 
		with 
			<origin xyz="0 0 0" rpy="${PI/2} 0 0"/>

	--> this removes the gap between the robot and ground plane

	add a gas station:
	mybot.world add:
		<include>
      		<uri>model://gas_station</uri>
      		<name>gas_station</name>
      		<pose>-2.0 7.0 0 0 0 0</pose>
    	</include>
		
		
# Laser Scan
This part of the tutorial is for adding a front laser and using the data we get from it to automate driving

1. add a description file for the laser mount in our case lms1xx
	- you can clone the file from https://github.com/jackal/jackal/blob/indigo-devel/jackal_description/urdf/accessories/sick_lms1xx_mount.urdf.xacro
	- add <xacro:property name="cameraSize" value="0.05"/>
		  <xacro:property name="cameraMass" value="0.1"/>
	- remove the <visual> brackets
	
2. in mybot.xacro add the front laser
	- the code you need to include:
	
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
