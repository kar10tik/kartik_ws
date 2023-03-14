import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile

class ReadingLaser(Node):

    def __init__(self):
        super().__init__('reading_laser')
        self.qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability = QoSDurabilityPolicy.VOLATILE,
            depth=10)
        self.subscription = self.create_subscription(
            LaserScan, 'scan', self.listener_callback,
            qos_profile = self.qos_profile)
       
        self.filtered_laser_scan_node = rclpy.create_node('filtered_laser_scan_publisher')
        self.publisher = self.create_publisher(LaserScan, 'filtered_scan', self.qos_profile)
        self.filtered_scan = LaserScan()

    def listener_callback(self, msg):
        print("Range: ", len(msg.ranges))
        current_angle = msg.angle_min
        count = 0
        for i in range(0, len(msg.ranges)):
            self.filtered_scan.ranges.append(msg.ranges[i])
            #self.filtered_scan.ranges[count] = msg.ranges[i]
            if (len(msg.intensities) > i):
                #self.filtered_scan.intensities[count] = msg.intensities[i]
                self.filtered_scan.intensities.append(msg.intensities[i])
                count += 1
                if (current_angle + msg.angle_increment > 2.0944):
                    break
                current_angle += msg.angle_increment
        self.publisher.publish(msg)


def main(args = None):
    rclpy.init()
    reading_laser = ReadingLaser()
    rclpy.spin(reading_laser)
    reading_laser.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()