import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    print(len(msg.ranges))

rospy.init_node('scan_values')
sub = rospy.Subscriber('/laser_scan_publisher', LaserScan, callback)
rospy.spin()