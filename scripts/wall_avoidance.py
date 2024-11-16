#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from pynput.keyboard import Key, Listener, KeyCode
twist = Twist() # Declaring the global variables so that they can be accessed in any of the functions.
pose= Pose()

def listener_node():
    rospy.init_node('listener_node', anonymous=True)
    rate=rospy.Rate(10)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    def callback(data): # data is a local variable. it can only be used inside the callback function.
        global pose
        pose=data   #it has to be stored somewhere so that it can be accessed outside the callback.
        print(f'pose undated: {pose}')
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    def on_press(key):
        global twist
        global pose
        try: 
            print('try block is seen')
            if 1.5 < pose.x < 10 and 1.5 < pose.y < 10:
                print('turtle is within the bounds')
                if key.char == 'w':
                    twist.linear.x = 2
                    print('w pressed')
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
                previous_linear = twist.linear.x
                if key.char in ['w', 'a','s', 'd']:
                    print('Freeze! This place is off-limits. You can rotate or go back.')
                twist.linear.x = 0
                start_time=rospy.get_time()
                pub.publish(twist)
                if (rospy.get_time()-start_time < 0.785):
                    twist.angular.z= 2
                    twist.linear.z = -previous_linear
                    pub.publish(twist)
                if key.char == 'a':
                    twist.angular.z= 2
                elif key.char == 'd':
                    twist.angular.z= -2
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
        print('Listener started.') #Check if listener is working.
    except KeyboardInterrupt:
        pass
    
    while not rospy.is_shutdown():
        rate.sleep()

if __name__== "__main__":
    try:
        listener_node()
    except rospy.ROSInterruptException:
        pass



