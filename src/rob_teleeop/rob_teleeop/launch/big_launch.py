import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFile, LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    # Get the file path to the example RViz configuration and the example URDF file
    rviz_config_file = os.path.join(get_package_share_directory('your_package_name'), 'config', 'example.rviz')
    urdf_file = os.path.join(get_package_share_directory('your_package_name'), 'urdf', 'base.urdf.xacro')

    # Configure the RViz2 node
    rviz_node = Node(
        package='rviz2',
        node_executable='rviz2',
        node_name='rviz2',
        output='both',
        arguments=['-d', rviz_config_file]
    )

    # Configure the robot_state_publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        node_executable='robot_state_publisher',
        node_name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': urdf_file}],
    )

    # Describe the launch process
    ld = LaunchDescription([
        DeclareLaunchArgument(
            'rviz_config_file',
            default_value=rviz_config_file,
            description='Full path to the RVIZ configuration file'),
        rviz_node,
        robot_state_publisher,
    ])

    return ld