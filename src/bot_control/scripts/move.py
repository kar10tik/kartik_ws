import rclpy #rospy in ROS1
import threading
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from tf2.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile

waypoint_coordinates = [[0,0,0] [5,0,45] [5,5,90] [0,5,0] [0,0,135]]

class RobotControl(Node):

    def __init__(self):
        super().__init__('controller_node')
        self.qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            durability = QoSDurabilityPolicy.VOLATILE,
            depth=10)
        self.vel_publisher = self.create_publisher(Twist, 'diff_drive_pub', qos_profile = self.qos_profile)
        self.cmd = Twist()
        self.ctrl_c = False
        thread = threading.Thread(target=rclpy.spin, args=(self, ), daemon=True)
        thread.start()
        self.rate = self.create_rate(10)
        rclpy.on_shutdown(self.shutdownhook)


    def publish_once_in_cmd_vel(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuous publishing systems, this is no big deal, but in systems that publish only
        once, it IS very important.
        """
        while not self.ctrl_c:
            connections = self.vel_publisher.get_num_connections()
            if connections > 0:
                self.vel_publisher.publish(self.cmd)
                break
            else:
                self.rate.sleep()


    def shutdownhook(self):
        self.stop_robot()
        self.ctrl_c = True


    def stop_robot(self):
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0
        self.publish_once_in_cmd_vel()


    def get_inputs_rotate(self):
        self.angular_speed_d = int(
            input('Enter desired angular speed (degrees): '))
        self.angle_d = int(input('Enter desired angle (degrees): '))
        clockwise_yn = input('Do you want to rotate clockwise? (y/n): ')
        if clockwise_yn == "y":
            self.clockwise = True
        if clockwise_yn == "n":
            self.clockwise = False

        return [self.angular_speed_d, self.angle_d]


    def convert_degree_to_rad(self, speed_deg, angle_deg):

        self.angular_speed_r = speed_deg * 3.14 / 180
        self.angle_r = angle_deg * 3.14 / 180
        return [self.angular_speed_r, self.angle_r]


    def rotate(self):

        # Initilize velocities
        self.cmd.linear.x = 0
        self.cmd.linear.y = 0
        self.cmd.linear.z = 0
        self.cmd.angular.x = 0
        self.cmd.angular.y = 0

        # Convert speed and angle to radians
        speed_d, angle_d = self.get_inputs_rotate()
        self.convert_degree_to_rad(speed_d, angle_d)

        # Check the direction of the rotation
        if self.clockwise:
            self.cmd.angular.z = -abs(self.angular_speed_r)
        else:
            self.cmd.angular.z = abs(self.angular_speed_r)

        # t0 is the current time
        t0 = rclpy.get_clock().now().secs

        current_angle = 0

        # loop to publish the velocity estimate, current_distance = velocity * (t1 - t0)
        while (current_angle < self.angle_r):

            # Publish the velocity
            self.vel_publisher.publish(self.cmd)
            # t1 is the current time
            t1 = rclpy.get_clock().now().secs
            # Calculate current angle
            current_angle = self.angular_speed_r * (t1 - t0)
            self.rate.sleep()

        # set velocity to zero to stop the robot
        #self.stop_robot()



def main(args=None):
    robotcontrol_object = RobotControl()
    try:
        res = robotcontrol_object.rotate()
    except rclpy.ROSInterruptException:
        pass
    count = 0
    while rclpy.ok(): #rospy equivalent of is_shutdown
        current_time = laser_scan_node.get_clock().now().to_msg() #rospy equivalent of Time.now()
        scan_pub.publish(scan)
        count += 1
        r.sleep()

if __name__ == '__main__':
    main()