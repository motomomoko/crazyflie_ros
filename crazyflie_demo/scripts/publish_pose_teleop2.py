#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import Pose, PoseStamped

lastData = None


def read_pos(pos):
    global lastData
    lastData = pos

if __name__ == '__main__':
    rospy.init_node('publish_pose', anonymous=True)
    worldFrame = rospy.get_param("~worldFrame", "/world")
    name = rospy.get_param("~name")
    r = rospy.get_param("~rate")
    flie = rospy.get_param("~flie")
    print("pose name = %s" % flie)
    x = rospy.get_param("~x")
    y = rospy.get_param("~y")
    z = rospy.get_param("~z")

    rate = rospy.Rate(r)

    msg = PoseStamped()
    msg.header.seq = 0
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = worldFrame
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = z
    yaw = 0
    quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)
    msg.pose.orientation.x = quaternion[0]
    msg.pose.orientation.y = quaternion[1]
    msg.pose.orientation.z = quaternion[2]
    msg.pose.orientation.w = quaternion[3]

    pub = rospy.Publisher(name, PoseStamped, queue_size=1)
    rospy.Subscriber(flie, Pose, read_pos)  #第３引数は実行する関数

    while not rospy.is_shutdown():
        if lastData is not None:
            msg.pose.position.x = lastData.position.x
            msg.pose.position.y = lastData.position.y
            msg.pose.position.z = lastData.position.z
            yaw = lastData.orientation.w
            quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)
            msg.pose.orientation.x = quaternion[0]
            msg.pose.orientation.y = quaternion[1]
            msg.pose.orientation.z = quaternion[2]
            msg.pose.orientation.w = quaternion[3]
        msg.header.seq += 1
        msg.header.stamp = rospy.Time.now()
        pub.publish(msg)
        rate.sleep()
