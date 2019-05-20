import rospy	
import time
from obst.finder import get_navigation_angle
from sensor_msgs.msg import PointCloud2, LaserScan

HIST_TRESH = 11.7
SECTOR_COUNT = 120
SECTOR_ANGLE = 360 / SECTOR_COUNT
VISION_ANGLE = 180
target_sector = 30

def update_target_sector():
	# get angle 0-360 counterclockwise, starting from right hand
	angle = 90
	# map angle to sector
	target_sector = angle / SECTOR_ANGLE



def callback(data):
	if data.ranges[0] >= data.range_min:
		# print(data.range_max)
		# print('increment: ' + str(data.angle_increment))
		# print(len(data.ranges))
		# TODO: get actual target by subscribing to node
		#for now suppose target angle is 81, i.e. sector 
		result = get_navigation_angle(target_sector, SECTOR_COUNT, SECTOR_ANGLE, HIST_TRESH, VISION_ANGLE, data)
		print(result)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('scan', LaserScan, callback)
	rospy.spin()


listener()