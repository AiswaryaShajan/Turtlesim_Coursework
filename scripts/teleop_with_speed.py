#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from pynput.keyboard import Key, Listener



def teleoperation():
    rospy.init_node('teleop', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    twist = Twist()
    while not rospy.is_shutdown():
        def on_press(key):
            try:
                if key == Key.up:
                    twist.linear.x = 1
                    pub.publish(twist)
                elif key == Key.down:
                    twist.linear.x = -1
                    pub.publish(twist)
                elif key == Key.left:
                    twist.angular.z = 1
                    pub.publish(twist)
                elif key == Key.right:
                    twist.angular.z = -1
                    pub.publish(twist)
                else:
                    pass
            except AttributeError:
                pass
        
        def on_release(key):
            try:
                if key == Key.up:
                    twist.linear.x = 0
                    pub.publish(twist)
                elif key == Key.down:
                    twist.linear.x = 0
                    pub.publish(twist)
                elif key == Key.left:
                    twist.angular.z = 0
                    pub.publish(twist)
                elif key == Key.right:
                    twist.angular.z = 0
                    pub.publish(twist)
                elif key == Key.esc:
                    return False
            except AttributeError:  
                pass
        try:
            listener = Listener(on_press=on_press, on_release=on_release)
            listener.start()  
        except KeyboardInterrupt:
            pass
        rate.sleep()
if __name__ == '__main__':
    try:
        teleoperation()
    except rospy.ROSInterruptException:
        pass
    


        
        



