#!/usr/bin/env python3
import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


WAYPOINTS = [
    (0.5, 0.0, 0.0),
    (1.5, 0.0, 0.0),
    (1.5, 1.0, math.pi / 2.0),
    (0.5, 1.0, math.pi),
]


def quaternion_from_yaw(yaw: float):
    return 0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)


def make_pose(navigator: BasicNavigator, x: float, y: float, yaw: float) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0
    qx, qy, qz, qw = quaternion_from_yaw(yaw)
    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    pose.pose.orientation.w = qw
    return pose


def main():
    rclpy.init()
    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()

    poses = [make_pose(navigator, *wp) for wp in WAYPOINTS]
    navigator.followWaypoints(poses)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            print(f'Current waypoint index: {feedback.current_waypoint}')

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Waypoint patrol completed.')
    elif result == TaskResult.CANCELED:
        print('Waypoint patrol canceled.')
    elif result == TaskResult.FAILED:
        print('Waypoint patrol failed.')
    else:
        print('Unknown patrol result.')

    navigator.destroyNode()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
