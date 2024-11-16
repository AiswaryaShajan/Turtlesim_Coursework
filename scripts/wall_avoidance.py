#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from pynput.keyboard import Key, Listener, KeyCode
twist = Twist() # Declaring the global variables so that they can be accessed in any of the functions.
pose= Pose()
last_pressed_key= None

def listener_node():
    rospy.init_node('listener_node', anonymous=True)
    rate=rospy.Rate(30)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    def callback(data): # data is a local variable. it can only be used inside the callback function.
        global pose
        pose=data   #it has to be stored somewhere so that it can be accessed outside the callback.
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    def on_press(key):
        global twist
        global pose
        global last_pressed_key
        print(f'new last pressed key:{last_pressed_key}')
        try: 
            print('try block is seen')
            if 1.5 < pose.x < 10 and 1.5 < pose.y < 10:
                print('turtle is within the bounds')
                if key.char == 'w':
                    print('pressed w')
                    twist.linear.x = 2
                    last_pressed_key= 'w'
                    print(f'last pressed key value set to {last_pressed_key}')
                elif key.char == 'a':
                    twist.linear.x=0
                    twist.angular.z= 2
                    last_pressed_key = 'a'
                elif key.char == 's':
                    twist.angular.z=0
                    twist.linear.x = -2
                    last_pressed_key = 's'
                elif key.char == 'd':
                    twist.linear.x =0
                    twist.angular.z= -2
                    last_pressed_key = 'd'
                pub.publish(twist)
            else:
                print('Oops! you are off-limits!')
                if last_pressed_key in ['w','a', 'd']:
                    if key.char == 'w':
                        twist.linear.x=0
                        last_pressed_key = 'w'
                        print('why still pressing w')
                    elif key.char == 'a':
                        print('ok so you press a ayee')
                        last_pressed_key ='a'
                        twist.angular.z= 2
                    elif key.char == 's':
                        print('ok good plan lets retract')
                        last_pressed_key = 's'
                        twist.linear.x = -2
                    elif key.char == 'd':
                        twist.angular.z= -2
                        last_pressed_key = 'd'
                elif last_pressed_key in ['s','a','d']:
                    if key.char == 'w':
                        twist.linear.x=2
                        last_pressed_key = 'w'
                    elif key.char == 'a':
                        twist.angular.z=2
                    elif key.char == 's':
                        twist.linear.x = 0
                        print('why you still pressing s?')
                        last_pressed_key = 's'
                    elif key.char == 'd':
                        twist.angular.z= -2
                elif key.char == 'a':
                    print('regular a condition works')
                    last_pressed_key='a'
                    twist.angular.z = 2
                elif key.char == 'd':
                    print('regular d condition works')
                    last_pressed_key = 'd'
                    twist.angular.z = -2
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



