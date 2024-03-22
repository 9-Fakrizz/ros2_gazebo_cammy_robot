#!/usr/bin/env python3
# Copyright 2011 Brown University Robotics.
# Copyright 2017 Open Source Robotics Foundation, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Willow Garage nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys

import geometry_msgs.msg
from std_msgs.msg import Float64MultiArray
import rclpy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import subprocess

if sys.platform == "win32":
    import msvcrt
else:
    import termios
    import tty


msg = """


Robotics & AI Engineering,
@Chiangmai University,
Student ID : 650610858, 
Suphakrit Kongkham.

          
           FINAL PROJECT OF ROBOTICS LAB 2

          
                       _oo0oo_
                      o8888888o
                      88" . "88 --- -- -
                      (| -_- |) -- -
                      0\  =  /0--- - -
                    ___/`---'\___---- -- -- 
                  .' \\|     |# '.---- - --
                 / \\|||  :  |||# ----- -- -
                / _||||| -:- |||||-- ------
               |   | \\\  -  #/ |   |------ -
               | \_|  ''\---/''  |_/ |---- - -
               \  .-\__  '-'  ___/-. /- - - -
             ___'. .'  /--.--\  `. .'___--------- -
          ."" '<  `.___\_<|>_/___.' >' "".----- --- --
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |--- -- - -
         \  \ `_.   \_ __\ /__ _/   .-` /  / ---- - - -
     =====`-.____`.___ \_____/___.-`___.-'===== --- - -
                       `=---='
 ______________________________________________________
    
    ----- PUTTO  ----   THUMMO    ---     SUNKKO  ----
 ______________________________________________________


 
    ->> KEYBOARD CONTROLLER INTERFACES V1.0 <<-


    
  Drive control                 Arms control
 ---------------      ------------------------------
       W              base arm       >>   '1' and '2'    
   A       D          middile arm    >>   '3' and '4'
       S              camera arm     >>   '4' and '5'
                      camera rotate  >>   '6' and '7'
  
 
 'W' (forward) ,'S' (backward) ,'A' (left) ,'D' (right) 
 
 --------------------------
 Thanks For Faitful Picture. 
 ref: https://github.com/IanSmith123/nobug.git
 --------------------------
 Thanks For All of my friends.
 ref: https://github.com/CannabiZz9/Gazebo_Gripper_Control.git
 ref: https://github.com/JayAleecha/Project_lab_robotic_2.git
 

"""


controlBindings = {
    "1": (0.5 ,0.0 ,0.0 ,0.0    ,0.0,0.0),
    "2": (-0.5 ,0.0 ,0.0 ,0.0    ,0.0,0.0),
    "3": (0.0 ,0.5 ,0.0 ,0.0    ,0.0,0.0),
    "4": (0.0 ,-0.5 ,0.0 ,0.0    ,0.0,0.0),
    "5": (0.0 ,0.0 ,0.5 ,0.0    ,0.0,0.0),
    "6": (0.0 ,0.0 ,-0.5 ,0.0    ,0.0,0.0),
    "7": (0.0 ,0.0 ,0.0 ,5.0    ,0.0,0.0),
    "8": (0.0 ,0.0 ,0.0 ,-5.0    ,0.0,0.0),

    "w": (0.0 ,0.0 ,0.0 ,0.0    ,5.0,5.0),
    "s": (0.0 ,0.0 ,0.0 ,0.0    ,-5.0,-5.0),
    "a": (0.0 ,0.0 ,0.0 ,0.0    ,15.0,-15.0),
    "d": (0.0 ,0.0 ,0.0 ,0.0    ,-15.0,15.0),
}

def getKey(settings):
    if sys.platform == "win32":
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == "win32":
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == "win32":
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)


def main():
    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node("teleop_twist_keyboard")
    pub = node.create_publisher(geometry_msgs.msg.Twist, "cmd_vel", 10)
    pub1 = node.create_publisher(Float64MultiArray, "/gripper_controller/commands", 10)
    

    speed = 0.4
    turn = 0.35
    a1 = 0.0
    b1 = 0.0
    c1 = 0.0
    d1 = 0.0
    lw = 0.0
    rw = 0.0
    th = 0.0
    status = 0.0

    try:
        print(msg)
        print(vels(speed, turn))
        while True:
            key = getKey(settings)
            if key in controlBindings.keys():
                a1 = controlBindings[key][0]
                b1 = controlBindings[key][1]
                c1 = controlBindings[key][2]
                d1 = controlBindings[key][3]
                lw = controlBindings[key][4]
                rw = controlBindings[key][5]
            elif key == 'x':  # Add this condition for the 'w' key
                # Define the value you want to publish to the gripper control topic
                control_value = [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0]  # Modify this value as needed
                Float1 = Float64MultiArray()
                Float1.data = control_value
                pub1.publish(Float1)
            
            else:
                a1 = 0.0
                b1 = 0.0
                c1 = 0.0
                d1 = 0.0
                lw = 0.0
                rw = 0.0
                if key == "\x03":
                    break

            # Only publish to the gripper control topic if it's not 'w' key
            if key != 'x':
                Float1 = Float64MultiArray()
                Float1.data = [a1, b1 ,c1 ,d1, lw ,rw]
                pub1.publish(Float1)

            twist = geometry_msgs.msg.Twist()
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.linear.z = 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
        # print(pub.publish(twist))
        Float1.data = [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0]
        pub1.publish(Float1)
        restoreTerminalSettings(settings)


if __name__ == "__main__":
    main()