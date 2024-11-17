#!/usr/bin/env python3 #SIMPLE CODE
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from pynput.keyboard import Key, Listener
twist = Twist() # Declaring the global variables so that they can be accessed in any of the functions.
pose= Pose()
in_bound= True

def listener_node():
    rospy.init_node('listener_node', anonymous=True)
    rate=rospy.Rate(10)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    def callback(data): # data is a local variable. it can only be used inside the callback function.
        global pose
        pose=data   #it has to be stored somewhere so that it can be accessed outside the callback.
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    def on_press(key):
        global twist
        global pose
        global in_bound
        try:
            if 1.5 < pose.x < 9.5 and 1.5< pose.y < 9.5:

                print('turtle is within the bounds')
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
                if key.char in ['w','s','a','d']:
                    print("Oops..you are off-limits! Let's get you back in")
                    twist.angular.z = 2
                    twist.linear.x = 2
                    pub.publish(twist)
                    
        except AttributeError:
            pass
    def on_release(key):
        global twist
        global pose
        try:
            if key.char in ['w', 'a', 's', 'd']:
                twist.linear.x = 0
                twist.angular.z = 0
                pub.publish(twist)
        except AttributeError:
            pass    
    try:
        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()
    except KeyboardInterrupt:
        rospy.signal_shutdown()
        listener.stop()
        
    
    while not rospy.is_shutdown():
        rate.sleep()

if __name__== "__main__":
    try:
        listener_node()
    except rospy.ROSInterruptException:
        pass