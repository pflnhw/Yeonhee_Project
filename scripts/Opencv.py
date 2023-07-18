#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from geometry_msgs.msg import Twist
import rospy

Roi_x1 = 0
Roi_x2 = 320
Roi_y1 = 0
Roi_y2 = 120

cap0 = cv2.VideoCapture(2) # 웹캠 장치 인덱스를 0으로 변경 (첫 번째 웹캠)

cap0.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
cap0.set(cv2.CAP_PROP_FRAME_WIDTH,320)

def cam0_read():
    global ret, frame0, original, gray0
    ret, frame0 = cap0.read()
    original = frame0
    gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

def cam0_line():
    global Roi, frame, original, theta
    Roi = gray0[Roi_y1:Roi_y2,Roi_x1:Roi_x2] # 이미지를 y1~y2 까지 자르고 x1~x2까지 자른다
    Roi = cv2.GaussianBlur(Roi, (5, 5), 0) # 이미지 흐릿하게 지정후 덮어쓴다. (깊이(입력이미지와 출력이미지를 동일하게 유지) -1, 필터크기 : 31,31 )
    _, Roi = cv2.threshold(Roi, 100, 255, cv2.THRESH_BINARY_INV) # 영상 2진화 (100: 픽셀값,임계값 , 255: 기준보다 큰값,cv2.THRESH_BINARY: 크면 value 작으면 0)
    # Noise Canceling
    kernel = np.ones((3, 3), np.uint8)
    Roi = cv2.erode(Roi, kernel, iterations=1)
    Roi = cv2.dilate(Roi, kernel, iterations=1)
    edged = cv2.Canny(Roi, 85, 85) # cv2.Canny : 이미지 가장자리 검출 (이미지,최소값,최대값)
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 30, 10, 1) # cv2.HoughLinesP : 직선검출 (이미지,해상도비율,각도(라디안,np.pi:원주율),임계값,검출될 선의 최소길이,선의 최대 간격)
    max_diff = 1000 # 선과의 거리 최대치(작아질수록 선의 중점이 이미지 중앙에 가깝다는 것)
    final_x = 0  # 선의 중점
    if ( lines is not None ):
        add_line = 0 # 변수초기화
        for line in lines:
            x1, y1, x2, y2 = line[0] # 시작점 끝점 좌표
            cv2.line(original,(x1+Roi_x1,y1+Roi_y1),(x2+Roi_x1,y2+Roi_y1),(0,255,0),3) # 검출된선의 양끝을 녹색으로 표시
            mid_point = ( x1 + x2 ) / 2  # mid_point: 선의 중점 x좌표
            diff = abs(320 - mid_point)  # diff: 선의 중점과 이미지 가운데x좌표의 차이
            if ( max_diff > diff ) :
                max_diff = diff
                final_x = mid_point # 최대 차이가 가장 작은 선의 중점을 찾는다.
            add_line = add_line + final_x 
        average_x = add_line / len(lines) # x좌표값을 선의 개수로 나누어 평균값계산
        original = cv2.circle(original,(int(average_x),int((Roi_y1+Roi_y2)/2)),5,(0,0,255),-1) #선에 중점에 점표시
        original = cv2.rectangle(original,(int(Roi_x1),int(Roi_y1)),(int(Roi_x2),int(Roi_y2)),(0,0,255),1)
        frame = original
        theta = int(( int(average_x) - 160.0 ) / 640.0 * 100)
        speed_angle_make()
    else:  # 검출되지 않았을 경우
        theta = -50
        Stop()
        frame = original


def speed_angle_make():
    global angle, speed
    angle = round((-theta) * (0.006), 2)
    # angle = 0
    speed = 0.1 - abs(angle * 0.2)

def Stop():
    global angle, speed
    speed = 0
    angle = 0

def Start():
    global speed, angle
    rospy.init_node('cmd_vel_publisher', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    while not rospy.is_shutdown():
        pub.publish(vel_msg)
        cam0_read()
        cam0_line()
        print(theta)
        cv2.imshow('Start', frame)
        vel_msg.linear.x = speed  # 원하는 선속도 설정
        vel_msg.angular.z = angle # 각속도는 0으로 설정
        if cv2.waitKey(25) != -1: # 키를 누르면 종료
            break   
    cap0.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    Start()