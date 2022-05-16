__author__ = 'Ramanan'
import cv2
import pyrealsense2
from realsense_depth import *
import time
import serial
ser=serial.Serial("COM5",115200)
Set_Distance=100#in cm
point_depth = [
(50,120 ),(50,240 ),(50, 360),(50, 360),
(100,120 ),(100,240 ),(100, 360),(100, 480),
(150,120 ),(150,240 ),(150, 360),(150, 480),
(200,120 ),(200,240 ),(200, 360),(200, 480),
(250,120 ),(250,240 ),(250, 360),(250, 480),
(300,120 ),(300,240 ),(300, 360),(300, 480),
(350,120 ),(350,240 ),(350, 360),(350, 480),
(400,120 ),(400,240 ),(400, 360),(400, 480),
(450,120 ),(450,240 ),(450, 360),(450, 480)

]
point_show = [
(120,50 ), (240,50), (360,50),(480,50),
(120,100 ),(240,100),(360,100),(480,100),
(120,150 ),(240,150),(360,150),(480,150),
(120,200 ),(240,200),(360,200),(480,200),
(120,250 ),(240,250),(360,250),(480,250),
(120,300 ),(240,300),(360,300),(480,300),
(120,350 ),(240,350),(360,350),(480,350),
(120,400 ),(240,400),(360,400),(480,400),
(120,450 ),(240,450),(360,450),(480,450)
]

distance1=[]
# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
dist_right=[]
Right_pix=[]
Left_pix=[]
while True:
    ret,color_frame,depth_frame = dc.get_frame()
    for i in range(len(point_depth)):
            distance = depth_frame[point_depth[i]]
            distance=int(distance/10)
            #cv2.putText(color_frame, "#{}".format(distance), (point_show[i]), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            if distance<15 and distance<1 and distance < 0:
                continue
            else:
                if(i%4==0):
                    Right_pix.append(distance)
                    #print(i)
                elif(i==3 or i==7 or i==11 or i ==15 or i==19 or i== 23 or i == 27 or i ==31 or 1==35):
                    Left_pix.append(distance)
                else:
                    distance1.append(distance)
    if any(dist<Set_Distance for dist in distance1):
        print("In center Object Detected")
        ser.write(b'o')
    elif any (dist_right<Set_Distance for dist_right in Right_pix):
        ser.write(b'd')
        print("Left Detected")
        
    elif any (dist_left<Set_Distance for dist_left in Left_pix):
        ser.write(b'c')
        print("Right Detected")
    else:
        print(" NO object detected")
        ser.write(b'a')
    Left_pix.clear()
    Right_pix.clear()
    distance1.clear()
    dist_right.clear()
    #cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    #print(type(distance))
    
    key = cv2.waitKey(1)

    if key == 27:
        ser.write(b'o')
        break
    
