#!/usr/bin/env python

from geometry_msgs.msg import Pose  # import type = Pose
import OSC
import rospy
import threading    # multi thread

lastData = None


def msgPrint(addr, tags, data, client_address):
    global lastData
    lastData = data

server_address = ("192.168.0.88", 9000)
server = OSC.OSCServer(server_address)  
server.addDefaultHandlers()
server.addMsgHandler("/pos", msgPrint)  # OSC tag
server_thread = threading.Thread(target=server.serve_forever)   # multi thread monitoring packet and runing main function
server_thread.start()

if __name__ == '__main__':
    rospy.init_node('broadcast', anonymous=True)    # ('node name' better to match in launch file, anonymous)

    name0 = rospy.get_param("~name0")   # get_param function (set "value" in launch file)
    name1 = rospy.get_param("~name1")
    name2 = rospy.get_param("~name2")
    name3 = rospy.get_param("~name3")
    name4 = rospy.get_param("~name4")
    cast = Pose()   # Pose instance

    pub0 = rospy.Publisher(name0, Pose, queue_size=1)   # Publisher class(3 arguments)
    pub1 = rospy.Publisher(name1, Pose, queue_size=1)   # que_size is packet number
    pub2 = rospy.Publisher(name2, Pose, queue_size=1)   # Pose is type in message
    pub3 = rospy.Publisher(name3, Pose, queue_size=1)
    pub4 = rospy.Publisher(name4, Pose, queue_size=1)

    while not rospy.is_shutdown():
        if lastData is not None:
            if lastData[0] == 0:
                cast.position.x = lastData[1]   # instance.type.x
                cast.position.y = lastData[2]
                cast.position.z = lastData[3]
                cast.orientation.w = lastData[4]
                pub0.publish(cast)
            elif lastData[0] == 1:
                cast.position.x = lastData[1]
                cast.position.y = lastData[2]
                cast.position.z = lastData[3]
                cast.orientation.w = lastData[4]
                pub1.publish(cast)
            elif lastData[0] == 2:
                cast.position.x = lastData[1]
                cast.position.y = lastData[2]
                cast.position.z = lastData[3]
                cast.orientation.w = lastData[4]
                pub2.publish(cast)
            elif lastData[0] == 3:
                cast.position.x = lastData[1]
                cast.position.y = lastData[2]
                cast.position.z = lastData[3]
                cast.orientation.w = lastData[4]
                pub3.publish(cast)
            elif lastData[0] == 4:
                cast.position.x = lastData[1]
                cast.position.y = lastData[2]
                cast.position.z = lastData[3]
                cast.orientation.w = lastData[4]
                pub4.publish(cast)
            else:
                print "cannot read position"
