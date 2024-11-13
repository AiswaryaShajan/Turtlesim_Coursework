#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

rospy.init_node('navigation_node', anonymous=True)
pub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
a, b= map(float, input('Enter the coordinates separated by a space. Make sure the values are between 0 and 11   ').split()) #input () takes the user input as a string. it is then split into 2 strings. the map function applies the float function across the list...giving two float numbers
print(f"Lets go to: ({a}, {b}") 

def callback(pose):
    rospy.loginfo('the turtle is at %f, %f, %f', pose.x, pose.y, pose.theta)
    twist = Twist()
    rate = rospy.Rate(10)

    y = pose.y - b
    x = pose.x - a
    angle_to_target = math.atan2(y, x)
    if abs(angle_to_target - pose.theta) > 0.1:
        twist.angular.z = 0.1
        pub.publish(twist)
    else: 
        twist.angular.z = 0
        pub.publish(twist)
        distance_to_target = math.sqrt((a-pose.x)**2+(b-pose.y)**2)
        if distance_to_target > 0.1:
            twist.linear.x = 0.5
        else:
            twist.linear.x = 0
            pub.publish(twist)
    rate.sleep()
    
    if distance_to_target < 0.1:
        print('Destination arrived.. Aloha!')
        rospy.signal_shutdown()

rospy.SubscribeListener('/turtle1/pose', Pose, callback )
if __name == '__main__':
    try:
        callback()
    except rospy.ROSInterruptException:
        pass



        

        


