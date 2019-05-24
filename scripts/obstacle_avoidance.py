import rospy	
import time
from obst.finder import get_navigation_angle
from sensor_msgs.msg import PointCloud2, LaserScan

HIST_TRESH = 1.35
SECTOR_COUNT = 120
SECTOR_ANGLE = 360 / SECTOR_COUNT
VISION_ANGLE = 180
target_sector = 30

def update_target_sector():
	# get angle 0-360 counterclockwise, starting from right hand
	angle = 90
	# map angle to sector
	target_sector = angle / SECTOR_ANGLE


def data_average(data):
	num = 0.0
	for cur_range in data.ranges:
		num += cur_range
	
	return num / len(data.ranges)


def callback(data):
	if data_average(data) >= 2:
		result = get_navigation_angle(target_sector, SECTOR_COUNT, SECTOR_ANGLE, HIST_TRESH, VISION_ANGLE, data)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('scan', LaserScan, callback)
	rospy.spin()


listener()
