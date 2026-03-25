from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = LaunchConfiguration('world')
    tb3_model = LaunchConfiguration('tb3_model')
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_params = LaunchConfiguration('slam_params_file')

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                world,
            ])
        )
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'),
                'launch',
                'navigation_launch.py',
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items(),
    )

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('slam_toolbox'),
                'launch',
                'online_async_launch.py',
            ])
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': slam_params,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('tb3_model', default_value='burger'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('world', default_value='turtlebot3_world.launch.py'),
        DeclareLaunchArgument(
            'slam_params_file',
            default_value=PathJoinSubstitution([
                FindPackageShare('tb3_slam_nav_pkg'),
                'config',
                'slam_toolbox.yaml',
            ]),
        ),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', tb3_model),
        gazebo_launch,
        nav2_launch,
        slam_launch,
    ])
