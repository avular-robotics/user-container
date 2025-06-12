
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    kinova_node = Node(
        package="origin_kinova_example",
        executable="kinova_node",
    )
    ld.add_action(kinova_node)
    return ld