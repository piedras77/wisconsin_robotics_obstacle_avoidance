import rospy	
import time
from obst.finder import get_navigation_angle
from sensor_msgs.msg import PointCloud2, LaserScan

HIST_TRESH = 3.3
SECTOR_COUNT = 120
SECTOR_ANGLE = 360 / SECTOR_COUNT
VISION_ANGLE = 180

def callback(data):
	if data.ranges[0] >= data.range_min:
		# print(data.range_max)
		# print('increment: ' + str(data.angle_increment))
		# print(len(data.ranges))
		# TODO: get actual target by subscribing to node
		#for now suppose target angle is 81, i.e. sector 
		result = get_navigation_angle(27, SECTOR_COUNT, SECTOR_ANGLE, HIST_TRESH, VISION_ANGLE, data)
		print(result)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('scan', LaserScan, callback)
	rospy.spin()


listener()