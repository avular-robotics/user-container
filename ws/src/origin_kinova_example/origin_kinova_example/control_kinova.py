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
from .resource import utilities


class KinovaArgs():
    ip = "192.168.100.200"
    username = "admin"
    password = "admin"

class ControlKinova(Node):
    def __init__(self, kinova_client) -> None:
        super().__init__('kinova_commander')
        self.get_logger().info('Hello from the ROS Kinova node')

        # store local variables
        self._kinova_client = kinova_client
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        
        qos_default = QoSPresetProfiles.get_from_short_key('system_default')
        qos_latching = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        
        # define subscriptions (origin joystick input)
        self.subscription = self.create_subscription(
            msg_type = Joy, 
            topic = '/robot/joy', 
            qos_profile = qos_default,
            callback = self.handle_joystick,
        )

        # sent commands to robot arm periodically
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.sent_twist_command)
        

    def handle_joystick(self, msg: Joy) -> None:
        '''
            function to readout the joystick commands and send then to the robot arm
        '''
        self.get_logger().info(f"received joystick command: {msg.axes}")

        # check of buttong L2 is being pressed
        if msg.axes[2] < 0.0:
            self.vx = msg.axes[7]
            self.vy = msg.axes[6]
            self.vz = 0.0
        else:
            self.vx = 0.0
            self.vy = -0.0
            self.vz = msg.axes[7]
        
        self.get_logger().info(f"speed commands would be: {self.vx}, {self.vy}, {self.vz}")
    
    def sent_twist_command(self):

        command = Base_pb2.TwistCommand()

        #command.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_BASE
        command.reference_frame = Base_pb2.CARTESIAN_REFERENCE_FRAME_TOOL
        command.duration = 0

        twist = command.twist
        twist.linear_x = self.vx
        twist.linear_y = self.vy
        twist.linear_z = self.vz
        twist.angular_x = 0
        twist.angular_y = 0
        twist.angular_z = 0

        self._kinova_client.SendTwistCommand(command)
        

def main(args=None) -> None:
    rclpy.init(args=args)

    args_kinova = KinovaArgs()

    # Create connection to the device and get the router
    with utilities.DeviceConnection.createTcpConnection(args_kinova) as router:
        # Create required services
        kinova_client = BaseClient(router)
        # spin the node
        control_kinova = ControlKinova(kinova_client)
        rclpy.spin(control_kinova)
    
        kinova_client.stop()

    control_kinova.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
