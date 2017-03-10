#!/usr/bin/env python

import OSC
import rospy
from sensor_msgs.msg import Joy
import threading

trigger = None


def msgPrint(addr, tags, data, client_address):
    global trigger
    trigger = data

server_address = ("192.168.0.88", 4000)
server = OSC.OSCServer(server_address)
server.addDefaultHandlers()
server.addMsgHandler("/trigger", msgPrint)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

if __name__ == '__main__':
    rospy.init_node('trigger', anonymous=True)

    name0 = rospy.get_param("~name0")
    name1 = rospy.get_param("~name1")
    name2 = rospy.get_param("~name2")
    name3 = rospy.get_param("~name3")
    name4 = rospy.get_param("~name4")
    tri = Joy()

    pub0 = rospy.Publisher(name0, Joy, queue_size=1)
    pub1 = rospy.Publisher(name1, Joy, queue_size=1)
    pub2 = rospy.Publisher(name2, Joy, queue_size=1)
    pub3 = rospy.Publisher(name3, Joy, queue_size=1)
    pub4 = rospy.Publisher(name4, Joy, queue_size=1)

    while not rospy.is_shutdown():
        if trigger is not None:
            flie = trigger.pop(0)
            tri.buttons = trigger
            if flie == 0:
                pub0.publish(tri)
            elif flie == 1:
                pub1.publish(tri)
            elif flie == 2:
                pub2.publish(tri)
            elif flie == 3:
                pub3.publish(tri)
            elif flie == 4:
                pub4.publish(tri)
            else:
                print "cannot read trigger"
            trigger = None
