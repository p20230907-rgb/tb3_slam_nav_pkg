#!/usr/bin/env python3
import math
import sys
import time

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node


class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('tb3_initial_pose_publisher')
        self.publisher = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)

    def publish_pose(self, x: float, y: float, yaw: float):
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        msg.pose.pose.orientation.w = math.cos(yaw / 2.0)
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.0685
        self.publisher.publish(msg)


def main():
    rclpy.init()

    if len(sys.argv) < 3:
        print('Usage: ros2 run tb3_slam_nav_pkg set_initial_pose <x> <y> [yaw_radians]')
        return

    x = float(sys.argv[1])
    y = float(sys.argv[2])
    yaw = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0

    node = InitialPosePublisher()
    for _ in range(5):
        node.publish_pose(x, y, yaw)
        rclpy.spin_once(node, timeout_sec=0.1)
        time.sleep(0.2)

    print(f'Initial pose published at x={x}, y={y}, yaw={yaw}')
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
