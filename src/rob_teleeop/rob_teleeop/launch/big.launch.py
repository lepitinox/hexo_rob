#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable,PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from pathlib import Path

def generate_launch_description():

    
    # Configure the RViz2 node
   #rviz_node = Node(
   #    package='rviz2',
   #    executable='rviz2',
   #    name='rviz2',
   #    arguments=['-d', '/home/ubuntu/rob/src/rob_teleeop/rob_teleeop/config/big.rviz'],
   #
    robot_description_content = Command([PathJoinSubstitution([FindPackageShare("rob_teleeop"),"base.urdf.xacro"])])
    path = "/home/ubuntu/hexo_rob/src/rob_teleeop/rob_teleeop/urdf/base.urdf.xacro"
    robot_description_content = Command([path])

    robot_description = {"robot_description": robot_description_content}

    # Configure the robot_state_publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': path}],
    )

    # Describe the launch process
    ld = LaunchDescription([
   #     rviz_node,
        robot_state_publisher,
    ])

    return ld