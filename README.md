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


create new package for scripts
