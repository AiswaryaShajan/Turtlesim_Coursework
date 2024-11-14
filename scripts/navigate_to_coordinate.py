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
    y = b-pose.y
    x = a-pose.x 
    angle_to_target = math.atan2(y, x)
    distance_to_target = math.sqrt((a-pose.x)**2+(b-pose.y)**2)
    angle_difference = abs(angle_to_target - pose.theta)
    rounded_angle_difference = round(angle_difference,2)
    print(rounded_angle_difference)
    if rounded_angle_difference > 0.4:
        twist.angular.z = 2
        pub.publish(twist)
    else: 
        print('hey the reached theta..almost!') #To check if the else block is executed
        twist.angular.z = 0
        pub.publish(twist)
        print(f'angular velocity is {twist.angular.z}') #To check if the angular velocity is set to zero.
    
        if distance_to_target > 0.1:
            twist.linear.x = 0.5
        else:
            twist.linear.x = 0
            pub.publish(twist)
    rate.sleep()
    
    if distance_to_target < 0.1:
        print('Destination arrived.. Aloha!')
        rospy.signal_shutdown()
def subscriber():
    rospy.Subscriber('/turtle1/pose', Pose, callback )
    rospy.spin()
if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass



        

        