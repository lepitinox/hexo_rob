#!/usr/bin/env python3
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node 
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory

from pathlib import Path


def generate_launch_description():


    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=[
            "-d",
            "/home/ubuntu/hexo_rob/src/rob_teleeop/rob_teleeop/config/big.rviz",
        ],
    )

    path = "/home/ubuntu/hexo_rob/src/rob_teleeop/rob_teleeop/urdf/base.urdf.xacro"
    #path = "/home/ubuntu/hexo_rob/src/rob_teleeop/rob_teleeop/urdf/test.urdf"


    model_arg = DeclareLaunchArgument(name='model', default_value=str(path),
                                      description='Absolute path to robot urdf file')
    
    
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration('model')]),
                                       value_type=str)

    usb_cam_dir = get_package_share_directory('usb_cam')
    params_path = os.path.join(
        usb_cam_dir,
        'config',
        'params.yaml'
    )

    # Configure the robot_state_publisher node
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    custom_state_publisher = Node(
        package="rob_teleeop",
        executable="state",
        name="state",
        output="screen",
    )
    usb_cam = Node(
        package='usb_cam', executable='usb_cam_node_exe', output='screen',
        name="my_usb_cam",
        parameters=[params_path]
        )
    
    hand_inf = Node(
        package='rob_teleeop', executable='hand_inf.py', output='screen',
        name="hand_inf",
        )

    # Describe the launch process
    ld = LaunchDescription(
        [
            model_arg,
            robot_state_publisher,
            rviz_node,
            custom_state_publisher,
            usb_cam,
            hand_inf
        ]
    )

    return ld
