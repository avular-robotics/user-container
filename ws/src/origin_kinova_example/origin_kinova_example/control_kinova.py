import time
import sys
import os
import threading

from kortex_api.TCPTransport import TCPTransport
from kortex_api.RouterClient import RouterClient
from kortex_api.SessionManager import SessionManager
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.messages import Session_pb2, Base_pb2

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, QoSPresetProfiles
from sensor_msgs.msg import Joy
#from .resource.utilities import TextUtils


class ControlKinova(Node):
    def __init__(self) -> None:
        super().__init__('kinova_commander')
        self.get_logger().info('Hello from the ROS Kinova node')
        
        qos_default = QoSPresetProfiles.get_from_short_key('system_default')
        qos_latching = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        
        # define subscriptions (origin joystick input)
        self.subscription = self.create_subscription(
            msg_type = Joy, 
            topic = '/robot/joy', 
            qos_profile = qos_default,
            callback = self.handle_joystick,
        )
        

    def handle_text_sentence(self, msg: Joy) -> None:
        '''
            function to readout the joystick commands and send then to the robot arm
        '''
        self.get_logger().info(f"received joystick command: {msg.axes}")
        self.get_logger().info(f"received joystick command: {msg.buttons}")

        # check of buttong L2 is being pressed
        if msg.axes[3] < 0.0:
            vx = msg.axes[0] + msg.axes[1]
            vy = msg.axes[2] + msg.axes[3]
            vz = 0.0
        else:
            vx = 0.0
            vy = -.0
            vz = msg.axes[0] + msg.axes[1]
        
        self.get_logger().info(f"speed commands would be: {vx}, {vy}, {vz}")
        

def main(args=None) -> None:
    rclpy.init(args=args)
    control_kinova = ControlKinova()
    rclpy.spin(control_kinova)
    control_kinova.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
