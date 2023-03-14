from launch import LaunchDescription
from launch_ros.actions import Node
 
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bot_control',
            namespace='ns1',
            executable='laser_scan_publisher',
            name='laser_scan_node'
        ),
        Node(
            package='bot_control',
            namespace='ns1',
            executable='reading_laser',
            name='reading_laser'
        ),
        Node(
            package='bot_control',
            namespace='ns1',
            executable='reading_laser',
            name='filtered_laser_scan_node'
        )
    ])