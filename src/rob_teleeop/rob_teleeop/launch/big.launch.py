import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from pathlib import Path

def generate_launch_description():

    
    # Configure the RViz2 node
    rviz_node = Node(
        package='rviz2',
        node_executable='rviz2',
        node_name='rviz2',
        output='both',
    )

    # Configure the robot_state_publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        node_executable='robot_state_publisher',
        node_name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': "/home/ubuntu/rob/src/rob_teleeop/rob_teleeop/urdf/robot.urdf"}],
    )

    # Describe the launch process
    ld = LaunchDescription([
        rviz_node,
        robot_state_publisher,
    ])

    return ld