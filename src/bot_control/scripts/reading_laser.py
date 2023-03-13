from rosidl_runtime_py import get_interface_path # For ROS2 compatibility with rosmsg (unavailable in ROS2)
from rosidl_adapter.parser import parse_message_file
m = parse_message_file('std_msgs', get_interface_path('std_msgs/msg/Bool'))
import rospy
import math, numpy as np
from sensor_msgs.msg import LaserScan

def callback(data):
    frame = np.zeros((500, 500, 3), np.uint8)
    angle = data.angle_min
    for r in data.ranges:
        #change infinite values to 0
        if math.isinf(r) == True:
            r = 0
        x = math.trunc((r * 30.0)*math.cos(angle + (-90.0*3.1416/180.0)))
        y = math.trunc((r * 30.0)*math.sin(angle + (-90.0*3.1416/180.0)))

        #set the borders (all values outside the defined area should be 0)
        if y > 0 or y < -35 or x<-40 or x>40:
            x=0
            y=0