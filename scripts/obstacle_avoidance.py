#!/usr/bin/env python

import math
import rospy    
import time
import threading
from finder import get_navigation_angle
from sensor_msgs.msg import PointCloud2, LaserScan
from manager.msg import IMU
from manager.msg import GPS
from drive.msg import Drive
from vision.msg import ObstaclesMsg

drive_pub = None
obstacle_pub = None

HIST_TRESH = 1.35
SECTOR_COUNT = 120
SECTOR_ANGLE = 360 / SECTOR_COUNT
VISION_ANGLE = 180
target_sector = 30
speed_factor = 0.5555555555

start = 0
old_lat = 0.0
old_long = 0.0
goal_lat = 0.0
goal_long = 0.0
curr_lat = 0.0
curr_long = 0.0

def set_gps(data):
    global start
    global old_lat
    global old_long
    global curr_lat
    global curr_long

    if 0 == start:
        # DEBUG
        old_lat = 41.8825490#data.lat
        old_long = -87.6232215#data.lon
        start = 1
    curr_lat = data.lat
    curr_long = data.lon

def set_goal(data):
    global goal_lat
    global goal_long

    goal_lat = data.lat
    goal_long = data.lon

def update_target_sector():
    global curr_long
    global old_long
    global goal_long
    global curr_lat
    global old_lat
    global goal_lat
    global target_sector

    print("current lat: ", curr_lat)
    print("current long: ", curr_long)
    print("old lat: ", old_lat)
    print("old long: ", old_long)
    print("goal lat: ", goal_lat)
    print("goal long: ", goal_long)

    # do math
    print("doing math")
    num = ((curr_long - old_long) * (goal_long - old_long)) + ((curr_lat - old_lat) * (goal_lat - old_lat))
    print("num: ", num)
    den = math.sqrt(math.pow(curr_long - old_long,2) + math.pow(curr_lat - old_lat,2)) * math.sqrt(math.pow(goal_long - old_long,2) + math.pow(goal_lat - old_lat,2))
    print("den: ", den)

    if (den < 0.0000001 and den > -0.0000001):
        # do nothing
        # DEBUG
        print("too close to old pt")
    else:
        angle_rad = math.acos(num/den)
        print("angle_rad: ", angle_rad)
        angle = math.degrees(angle_rad)
        print("angle: ", angle)
        # DEBUG
        #old_lat = curr_lat
        #old_long = curr_long

        # publish angle
        msg = ObstaclesMsg()
        msg.detectedTimestamp = time.time()
        msg.bestAngle = angle
        obstacle_pub.publish(msg)

        # map angle to sector
        target_sector = angle / SECTOR_ANGLE
    
    threading.Timer(0.25, update_target_sector).start()

def data_average(data):
    num = 0.0
    for cur_range in data.ranges:
        num += cur_range

    return num / len(data.ranges)

def callback(data):
    if data_average(data) >= 2:
        # print(data.range_max)
        # print('increment: ' + str(data.angle_increment))
        # print(len(data.ranges))
        #for now suppose target angle is 81, i.e. sector 
        result = get_navigation_angle(target_sector, SECTOR_COUNT, SECTOR_ANGLE, HIST_TRESH, VISION_ANGLE, data)

        # DEBUG
        print(result)

        msg = Drive()
        if (result >= 0 and result < 90): # quadrant 1
            right_prop = result
            left_prop = 180 - result
            msg.left = speed_factor * left_prop
            msg.right = speed_factor * right_prop
        elif (result >= 90 and result < 180): # quadrant 2
            right_prop = result
            left_prop = 180 - result
            msg.left = speed_factor * left_prop
            msg.right = speed_factor * right_prop
        elif (result >= 180 and results < 270): # quadrant 3
            left_prop = result - 180
            right_prop = 360 - result
            msg.left = -speed_factor * left_prop
            msg.right = speed_factor * right_prop
        else: # quadrant 4
            left_prop = result - 180
            right_prop = 360 - result
            msg.left = speed_factor * left_prop
            msg.right = -speed_factor * right_prop
        drive_pub.publish(msg)

def listener():
    global drive_pub
    global obstacle_pub

    rospy.init_node('listener', anonymous=True)

    # subscribers
    rospy.Subscriber('scan', LaserScan, callback)
    rospy.Subscriber('gps', GPS, set_gps)
    rospy.Subscriber('goal_gps', GPS, set_goal)

    # publishers
    drive_pub = rospy.Publisher('drive_cmd', Drive, queue_size=10)
    obstacle_pub = rospy.Publisher('obstacles', ObstaclesMsg, queue_size=10)

    threading.Timer(0.25, update_target_sector).start()

    rospy.spin()

listener()
