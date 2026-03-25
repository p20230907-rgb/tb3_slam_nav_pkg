#!/usr/bin/env python3
import math
import sys

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def quaternion_from_yaw(yaw: float):
    return 0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0)


def main():
    rclpy.init()

    if len(sys.argv) < 3:
        print('Usage: ros2 run tb3_slam_nav_pkg send_goal <x> <y> [yaw_radians]')
        return

    x = float(sys.argv[1])
    y = float(sys.argv[2])
    yaw = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0

    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()

    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = 0.0
    qx, qy, qz, qw = quaternion_from_yaw(yaw)
    goal_pose.pose.orientation.x = qx
    goal_pose.pose.orientation.y = qy
    goal_pose.pose.orientation.z = qz
    goal_pose.pose.orientation.w = qw

    navigator.goToPose(goal_pose)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            print(f'Estimated time remaining: {feedback.estimated_time_remaining.sec} sec')

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled.')
    elif result == TaskResult.FAILED:
        print('Goal failed.')
    else:
        print('Goal has an unknown result.')

    navigator.destroyNode()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
