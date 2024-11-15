#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

rospy.init_node('navigation_node', anonymous=True)
pub=rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
a, b= map(float, input('Enter the coordinates separated by a space. Make sure the values are between 0 and 11   ').split()) #input () takes the user input as a string. it is then split into 2 strings. the map function applies the float function across the list...giving two float numbers
print(f"Lets go to: ({a}, {b}") 
rotation_done= False
linear_done=False
twist=Twist()
twist.linear.x =0
twist.angular.z=0

def callback(pose):
    rospy.loginfo('the turtle is at %f, %f, %f', pose.x, pose.y, pose.theta)
    global Twist
    global rotation_done
    global linear_done
    rate = rospy.Rate(10)
    y = b-pose.y
    x = a-pose.x 
    angle_to_target = math.atan2(y, x)
    distance_to_target = math.sqrt((a-pose.x)**2+(b-pose.y)**2)
    angle_difference = abs(angle_to_target - pose.theta)
    print(angle_difference)
    print(f'distance_to_target is {distance_to_target}')
    if not rotation_done:
        if angle_difference > 0.04:
            twist.angular.z = 2
            pub.publish(twist)
        else: 
            twist.angular.z = 0
            pub.publish(twist)
            rotation_done=True
            print(f'angular velocity is {twist.angular.z}') #To check if the angular velocity is set to zero.
            rate.sleep()
    else:
        print('rotation done')
        if not linear_done:
            if distance_to_target > 0.3:
                twist.linear.x = 1
                pub.publish(twist)
            else: 
                print('Yes we reached')
                linear_done=True
                
        else:
            twist.linear.x=0
            pub.publish(twist)
            print("Desintation arrived. Aloha!")
            rospy.signal_shutdown('destination reached')
    
def subscriber():
    rospy.Subscriber('/turtle1/pose', Pose, callback )
    rospy.spin()
if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass