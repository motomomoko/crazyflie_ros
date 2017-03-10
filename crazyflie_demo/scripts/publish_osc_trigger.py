#!/usr/bin/env python

import rospy
from crazyflie_driver.srv import UpdateParams
from std_srvs.srv import Empty
import threading
import OSC

trigger = None

def msgPrint(addr, tags, data, client_address):
    global trigger
    trigger = data
#    print trigger

server_address = ("192.168.11.102", 5000)
server = OSC.OSCServer(server_address)
server.addDefaultHandlers()
server.addMsgHandler("/trigger", msgPrint)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

if __name__ == '__main__':
    rospy.init_node('crazyflie_demo_controller', anonymous=True)

    rospy.wait_for_service('update_params')
    rospy.loginfo("found update_params service")
    update_params = rospy.ServiceProxy('update_params', UpdateParams)

    rospy.loginfo("waiting for emergency service")
    rospy.wait_for_service('emergency')
    rospy.loginfo("found emergency service")
    emergency = rospy.ServiceProxy('emergency', Empty)

    rospy.loginfo("waiting for land service")
    rospy.wait_for_service('land')
    rospy.loginfo("found land service")
    land = rospy.ServiceProxy('land', Empty)

    rospy.loginfo("waiting for takeoff service")
    rospy.wait_for_service('takeoff')
    rospy.loginfo("found takeoff service")
    takeoff = rospy.ServiceProxy('takeoff', Empty)

    buttons = None

    while not rospy.is_shutdown():
#    while True:
#        global trigger
#        print "while"
        if trigger == None:
            continue
        for i in range(0, len(trigger)):
            if buttons == None or trigger[i] != buttons[i]:
#                print "enter"
#                print trigger
#                print buttons
                if i == 0 and trigger[i] == 1 and land != None:
#                    print "land"
                    land()
                if i == 1 and trigger[i] == 1:
#                    print "emergency"
                    emergency()
                if i == 2 and trigger[i] == 1 and takeoff != None:
#                    print"takeoff"
                    takeoff()
                if i == 3 and trigger[i] == 1:
#                    print "LED"
                    value = int(rospy.get_param("ring/headlightEnable"))
                    if value == 0:
                        rospy.set_param("ring/headlightEnable", 1)
                    else:
                        rospy.set_param("ring/headlightEnable", 0)
                    update_params(["ring/headlightEnable"])
                    print(not value)

        buttons = trigger

#        rospy.spin()
