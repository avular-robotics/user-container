# Copyright 2025 Avular Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from origin_msgs.msg import ControlMode
from origin_msgs.srv import SetControlMode
from origin_msgs.srv import ReturnControlMode

import numpy as np

N_PI = 3.14159265

class SetVelocity(Node):

    def __init__(self):
        super().__init__('velocity_commander')
        self.mission_executing_callback_group = rclpy.callback_groups.MutuallyExclusiveCallbackGroup()
        self.main_callback_group = rclpy.callback_groups.ReentrantCallbackGroup()
        # create the velocity publisher
        self.velocity_publisher = self.create_publisher(Twist, 'robot/cmd_vel_user', 10)
        self.velocity_msg = Twist()
        self.velocity_msg.linear.x = 1.0 	# meters per second
        self.velocity_msg.angular.z = 0.0   # radians per second
        # create a service for acquiring and releasing control of the robot
        self.request_control = self.create_client(
            srv_type=SetControlMode,
            srv_name='/robot/cmd_vel_controller/set_control_mode',
            callback_group=self.main_callback_group,
        )
        self.release_control = self.create_client(
            srv_type=ReturnControlMode,
            srv_name='/robot/cmd_vel_controller/reset_control_mode',
            callback_group=self.main_callback_group,
        )
        self.obtained_control = False       

        # create a timer for publishing the velocity at 10 Hz
        self.timer_period = 0.1     # seconds
        self.counter = 0            # counter for the number of times the velocity command is sent, after which the test will change the velocity command to a different value
        self.timer = self.create_timer(self.timer_period, self.timer_callback, callback_group = self.mission_executing_callback_group)     
        
    async def get_control(self):
        request_msg = SetControlMode.Request()
        request_msg.mode.mode = ControlMode.USER
        if not self.request_control.service_is_ready():
            print("[WARNING]: behavior service not available, aborting...")
            return False
        else:
            response = await self.request_control.call_async(request_msg)
            return response.success

    async def timer_callback(self):
        if not self.obtained_control:
            self.obtained_control = await self.get_control()
            if self.obtained_control:
                self.get_logger().info('Successfully obtained control of the robot, starting to send velocity commands')
            else:
                self.get_logger().error('Failed to obtain control of the robot, aborting...')
                rclpy.shutdown()
                return
        # sent velocity commands
        if self.counter == 20:
            self.velocity_msg.linear.x = 1.0 	    # meters per second
            self.velocity_msg.angular.z = 0.0	    # radians per second
            self.counter = 0
        elif self.counter == 10:
            self.velocity_msg.linear.x = 0.0 	    # meters per second
            self.velocity_msg.angular.z = N_PI/3/10	# radians per second
            self.counter += 1
        else:
            self.counter += 1

        self.velocity_publisher.publish(self.velocity_msg)
        self.get_logger().info('Setting a reference velocity of %.2f [m/s] going forward and %.2f [deg/s] turning ' % (self.velocity_msg.linear.x, self.velocity_msg.angular.z*180/N_PI))


def main(args=None):
    rclpy.init(args=args)

    set_velocity = SetVelocity()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(set_velocity)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        set_velocity.destroy_node()
        rclpy.shutdown()
          
    
if __name__ == '__main__':
    main()
