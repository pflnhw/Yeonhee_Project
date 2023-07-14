#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist

frame_crop_x1 = 0
frame_crop_y1 = 120
frame_crop_x2 = 640
frame_crop_y2 = 480

minLineLength = 30
maxLineGap = 15

cap_0 = cv2.VideoCapture(0)  # 웹캠 장치 인덱스를 0으로 변경 (첫 번째 웹캠)

def cam_0_read():
    global retval_0, frame_0, original, gray_line_0
    retval_0, frame_0 = cap_0.read()
    original = frame_0

def cam_0_use_line():
    global retval_0, frame_0, original, theta
    blurred = frame_0[frame_crop_y1:frame_crop_y2, frame_crop_x1:frame_crop_x2] # 이미지를 y1~y2 까지 자르고 x1~x2까지 자른다
    blurred = cv2.boxFilter(blurred, ddepth=-1, ksize=(31, 31)) # 이미지 흐릿하게 지정후 덮어쓴다. (깊이(입력이미지와 출력이미지를 동일하게 유지) -1, 필터크기 : 31,31 )
    retval2, blurred = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY) # 영상 2진화 (100: 픽셀값,임계값 , 255: 기준보다 큰값,cv2.THRESH_BINARY: 크면 value 작으면 0)
    edged = cv2.Canny(blurred, 85, 85)  # cv2.Canny : 이미지 가장자리 검출 (이미지,최소값,최대값)
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 10, minLineLength, maxLineGap) # cv2.HoughLinesP : 직선검출 (이미지,해상도비율,각도(라디안,np.pi:원주율),임계값,검출될 선의 최소길이,선의 최대 간격)
    max_diff = 1000 # 선과의 거리 최대치(작아질수록 선의 중점이 이미지 중앙에 가깝다는 것)
    final_x = 0  # 선의 중점
    if lines is not None:
        add_line = 0 # 변수초기화
        for line in lines: 
            x1, y1, x2, y2 = line[0]  # 시작점 끝점 좌표
            cv2.line(original, (x1+frame_crop_x1, y1+frame_crop_y1), (x2+frame_crop_x1, y2+frame_crop_y1), (0, 255, 0), 3) # 검출된선의 양끝을 녹색으로 표시
            mid_point = (x1 + x2) / 2  # mid_point: 선의 중점 x좌표
            diff = abs((640/2) - mid_point) # diff: 선의 중점과 이미지 가운데x좌표의 차이
            if max_diff > diff:
                max_diff = diff
                final_x = mid_point # 최대 차이가 가장 작은 선의 중점을 찾는다.
            add_line = add_line + final_x
        average_x = add_line / len(lines)  # x좌표값을 선의 개수로 나누어 평균값계산
        if int(average_x) != 0:
            original = cv2.circle(original, (int(average_x), int((frame_crop_y1+frame_crop_y2)/2)), 5, (0, 0, 255), -1) #선에 중점에 점표시
            original = cv2.rectangle(original, (int(frame_crop_x1), int(frame_crop_y1)), (int(frame_crop_x2), int(frame_crop_y2)), (0, 0, 255), 1)
        frame_0 = original
        theta = int((int(average_x) - 320.0) / 640.0 * 100)
    if lines is None: # 검출되지 않았을 경우
        theta = -50

# 웹캠 영상 처리
while True:
    cam_0_read()
    cam_0_use_line()

    cv2.imshow('frame_0', frame_0)

    key = cv2.waitKey(1)
    if key == 27:  # ESC 키를 누르면 종료
        break

    # 로봇 이동
    rospy.init_node('cmd_vel_publisher', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 퍼블리셔의 발행 속도 설정

    vel = Twist()
    vel.linear.x = 0.05  # 원하는 선속도 설정
    vel.angular.z = 0.0  # 각속도는 0으로 설정
    pub.publish(vel)
    rate.sleep()

# 웹캠 사용 종료
cap_0.release()
cv2.destroyAllWindows()
