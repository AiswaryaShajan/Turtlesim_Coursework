#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from pynput.keyboard import Key, Listener, KeyCode

def listener_node():
    twist = Twist()
    pose=Pose()
    rospy.init_node('listener_node', anonymous=True)
    rate=rospy.Rate(10)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    def callback(data):
        global pose
        pose=data
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    def on_press(key):
        global twist
        try: 
            if 0.5 < pose.x < 10.5 and 0.5 < pose.y < 10.5:
                if key.char == 'w':
                    twist.linear.x = 2
                elif key.char == 'a':
                    twist.linear.x=0
                    twist.angular.z= 2
                elif key.char == 's':
                    twist.angular.z=0
                    twist.linear.x = -2
                elif key.char == 'd':
                    twist.linear.x =0
                    twist.angular.z= -2
                pub.publish(twist)
            else:
                twist.linear.x =0
                twist.angular.z = 0
                pub.publish(twist)
        except AttributeError:
            pass
    def on_release(key):
        global twist
        try:
            if key.char in ['w', 'a', 's', 'd']:
                twist.linear.x = 0
                twist.angular.z = 0
                pub.publish(twist)
        except AttributeError:
            pass    
    try:
        listener = Listener(on_press=on_press, on_release=on_release)
    except KeyboardInterrupt:
        pass
    
    

if __name__== "__main__":
    try:
        listener_node()
    except rospy.ROSInterruptException:
        pass



