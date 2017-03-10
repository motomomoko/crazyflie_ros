#!/usr/bin/env python

from geometry_msgs.msg import Pose  #型Poseをimport
import OSC
import rospy
import threading    #マルチスレッド

lastData = None


def msgPrint(addr, tags, data, client_address):
    global lastData
    lastData = data

server_address = ("192.168.0.88", 9000)
server = OSC.OSCServer(server_address)  
server.addDefaultHandlers()
server.addMsgHandler("/pos", msgPrint)  #OSCタグの指定
server_thread = threading.Thread(target=server.serve_forever)   #パケットの監視とメイン関数実行
server_thread.start()

if __name__ == '__main__':
    rospy.init_node('broadcast', anonymous=True)    #(node名、launchファイルで指定したものと揃えようanonymousは匿名(複数回立ち上げるときは必須))

    name0 = rospy.get_param("~name0")   #get_param関数(launchファイルで設定したvalueが代入)
    name1 = rospy.get_param("~name1")
    name2 = rospy.get_param("~name2")
    name3 = rospy.get_param("~name3")
    name4 = rospy.get_param("~name4")
    cast = Pose()   #Poseのインスタンス作成

    pub0 = rospy.Publisher(name0, Pose, queue_size=1)   #Publisherクラス(引数3つ)
    pub1 = rospy.Publisher(name1, Pose, queue_size=1)   #que_sizeは保持するパケット数
    pub2 = rospy.Publisher(name2, Pose, queue_size=1)   #Poseはメッセージの中身の型
    pub3 = rospy.Publisher(name3, Pose, queue_size=1)
    pub4 = rospy.Publisher(name4, Pose, queue_size=1)

    while not rospy.is_shutdown():
        if lastData is not None:
            if lastData[0] == 0:
                cast.position.x = lastData[1]   #インスタンス.型指定.x
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
