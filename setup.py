import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tb3_slam_nav_pkg'

setup(
    name=package_name,
    version='0.1.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Kabita Choudhary',
    maintainer_email='user@example.com',
    description='TurtleBot3 ROS 2 package for SLAM mapping and Nav2 navigation in simulation or on a robot.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'send_goal = tb3_slam_nav_pkg.send_goal:main',
            'set_initial_pose = tb3_slam_nav_pkg.set_initial_pose:main',
            'patrol_waypoints = tb3_slam_nav_pkg.patrol_waypoints:main',
        ],
    },
)
