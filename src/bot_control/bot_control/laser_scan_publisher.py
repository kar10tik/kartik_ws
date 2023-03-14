import rclpy #rospy in ROS1
import threading
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile


rclpy.init()
laser_scan_node = rclpy.create_node('laser_scan_publisher')
qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability = QoSDurabilityPolicy.VOLATILE,
            depth=10)
scan_pub = laser_scan_node.create_publisher(LaserScan, 'scan', qos_profile = qos_profile)#, queue_size=50)

def main(args=None):
    num_readings = 100
    laser_frequency = 40

    count = 0
    thread = threading.Thread(target=rclpy.spin, args=(laser_scan_node, ), daemon=True)
    thread.start()

    r = laser_scan_node.create_rate(1.0)
    while rclpy.ok(): #rospy equivalent of is_shutdown
        current_time = laser_scan_node.get_clock().now().to_msg() #rospy equivalent of Time.now()

        scan = LaserScan()

        scan.header.stamp = current_time
        scan.header.frame_id = 'laser_frame'
        scan.angle_min = 0.0
        scan.angle_max = 1.57 #2.0944 # 120_degrees in rad
        scan.angle_increment = 3.14 / num_readings
        scan.time_increment = (1.0 / laser_frequency) / (num_readings)
        scan.range_min = 0.0
        scan.range_max = 100.0

        scan.ranges = []
        scan.intensities = []
        for i in range(0, num_readings):
            scan.ranges.append(1.0 * count)  # sample data
            scan.intensities.append(1)  # sample data

        scan_pub.publish(scan)
        count += 1
        r.sleep()

if __name__ == '__main__':
    main()