#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import PoseStamped
import threading
import OSC

lastData = None


def msgPrint(addr, tags, data, client_address):
    global lastData
    lastData = data
#    print lastData

server_address = ("192.168.11.102", 8000) 
server = OSC.OSCServer(server_address)
server.addDefaultHandlers()
server.addMsgHandler("/pos", msgPrint)
#server.addMsgHandler("/pos1", msgPrint)
#server.addMsgHandler("/pos2", msgPrint)
#server.addMsgHandler("/pos3", msgPrint)
#server.addMsgHandler("/pos4", msgPrint)

server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

if __name__ == '__main__':
    rospy.init_node('publish_pose', anonymous=True)
    worldFrame = rospy.get_param("~worldFrame", "/world")
    name = rospy.get_param("~name")
    r = rospy.get_param("~rate")
    x0 = rospy.get_param("~x0")
    y0 = rospy.get_param("~y0")
    z0 = rospy.get_param("~z0")
    x1 = rospy.get_param("~x1")
    y1 = rospy.get_param("~y1")
    z1 = rospy.get_param("~z1")
    x2 = rospy.get_param("~x2")
    y2 = rospy.get_param("~y2")
    z2 = rospy.get_param("~z2")
    x3 = rospy.get_param("~x3")
    y3 = rospy.get_param("~y3")
    z3 = rospy.get_param("~z3")
    x4 = rospy.get_param("~x4")
    y4 = rospy.get_param("~y4")
    z4 = rospy.get_param("~z4")

    rate = rospy.Rate(r)

    msg = PoseStamped()
    msg.header.seq = 0
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = worldFrame
    msg.pose.position.x0 = x0
    msg.pose.position.y0 = y0
    msg.pose.position.z0 = z0
    yaw0 = 0
    msg.pose.position.x1 = x1
    msg.pose.position.y1 = y1
    msg.pose.position.z1 = z1
    yaw1 = 0
    msg.pose.position.x2 = x2
    msg.pose.position.y2 = y2
    msg.pose.position.z2 = z2
    yaw2 = 0
    msg.pose.position.x3 = x3
    msg.pose.position.y3 = y3
    msg.pose.position.z3 = z3
    yaw3 = 0
    msg.pose.position.x4 = x4
    msg.pose.position.y4 = y4
    msg.pose.position.z4 = z4
    yaw4 = 0
    quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)
    msg.pose.orientation.x = quaternion[0]
    msg.pose.orientation.y = quaternion[1]
    msg.pose.orientation.z = quaternion[2]
    msg.pose.orientation.w = quaternion[3]

    pub = rospy.Publisher(name, PoseStamped, queue_size=1)

    while not rospy.is_shutdown():
        # global lastData
        if lastData != None:
            if lastData[0] == 0:
                msg.pose.position.x0 = lastData[1]
                msg.pose.position.y0 = lastData[2]
                msg.pose.position.z0 = lastData[3]
                yaw0 = lastData[4]
            if lastData[0] == 1:
                msg.pose.position.x1 = lastData[1]
                msg.pose.position.y1 = lastData[2]
                msg.pose.position.z1 = lastData[3]
                yaw1 = lastData[4]
            if lastData[0] == 2:
                msg.pose.position.x2 = lastData[1]
                msg.pose.position.y2 = lastData[2]
                msg.pose.position.z2 = lastData[3]
                yaw2 = lastData[4]
            if lastData[0] == 3:
                msg.pose.position.x3 = lastData[1]
                msg.pose.position.y3 = lastData[2]
                msg.pose.position.z3 = lastData[3]
                yaw3 = lastData[4]
            if lastData[0] == 4:
                msg.pose.position.x4 = lastData[1]
                msg.pose.position.y4 = lastData[2]
                msg.pose.position.z4 = lastData[3]
                yaw4 = lastData[4]

            quaternion0 = tf.transformations.quaternion_from_euler(0, 0, yaw)
            msg.pose.orientation.x = quaternion[0]
            msg.pose.orientation.y = quaternion[1]
            msg.pose.orientation.z = quaternion[2]
            msg.pose.orientation.w = quaternion[3]
#            print(pose)
        msg.header.seq += 1
        msg.header.stamp = rospy.Time.now()
        pub.publish(msg)
        rate.sleep()
