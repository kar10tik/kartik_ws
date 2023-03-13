import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

def callback(data):
    frame = np.zeros((500, 500,3), np.uint8)
    angle = data.angle_min
    for r in data.ranges:
        #change infinite values to 0
        if math.isinf(r) == True:
            r = 0
        #convert angle and radius to cartesian coordinates
        x = math.trunc((r * 30.0)*math.cos(angle + (-90.0*3.1416/180.0)))
        y = math.trunc((r * 30.0)*math.sin(angle + (-90.0*3.1416/180.0)))

        #set the borders (all values outside the defined area should be 0)
        if y > 0 or y < -35 or x<-40 or x>40:
            x=0
            y=0

        cv2.line(frame,(250, 250),(x+250,y+250),(255,0,0),2)
        angle= angle + data.angle_increment 
        cv2.circle(frame, (250, 250), 2, (255, 255, 0))
        cv2.imshow('frame',frame)
        cv2.waitKey(1)