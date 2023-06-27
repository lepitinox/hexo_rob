#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch_ros.parameter_descriptions import ParameterValue

from pathlib import Path


def generate_launch_description():
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            "/home/ubuntu/rob/src/rob_teleeop/rob_teleeop/config/big.rviz",
        ],
    )

    path = "/home/ubuntu/hexo_rob/src/rob_teleeop/rob_teleeop/urdf/base.urdf.xacro"
    path = "/home/ubuntu/hexo_rob/src/rob_teleeop/rob_teleeop/urdf/test.urdf"


    model_arg = DeclareLaunchArgument(name='model', default_value=str(path),
                                      description='Absolute path to robot urdf file')
    
    
    robot_description = ParameterValue(Command([LaunchConfiguration('model')]),
                                       value_type=str)


    with open(path, "r") as file:
        data = file.read()

    cpm = Command("whoami")
    # Configure the robot_state_publisher node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    # Describe the launch process
    ld = LaunchDescription(
        [cpm,
            model_arg,
            robot_state_publisher,
            rviz_node,
        ]
    )

    return ld
