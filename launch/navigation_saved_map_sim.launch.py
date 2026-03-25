from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = LaunchConfiguration('world')
    tb3_model = LaunchConfiguration('tb3_model')
    map_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                world,
            ])
        )
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_navigation2'),
                'launch',
                'navigation2.launch.py',
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': map_file,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('tb3_model', default_value='burger'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('world', default_value='turtlebot3_world.launch.py'),
        DeclareLaunchArgument('map', default_value='/tmp/my_map.yaml'),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', tb3_model),
        gazebo_launch,
        navigation_launch,
    ])
