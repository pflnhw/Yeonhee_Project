#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import rospy
from geometry_msgs.msg import Twist
import pyzbar.pyzbar as pyzbar

frame_crop_x1 = 0
frame_crop_y1 = 120
frame_crop_x2 = 640
frame_crop_y2 = 480

minLineLength = 30
maxLineGap = 15
vel = Twist()
cap_0 = cv2.VideoCapture(0)  # 웹캠 장치 인덱스를 0으로 변경 (첫 번째 웹캠)


def cam_0_read():
    global retval_0, frame_0, original, gray_line_1
    retval_0, frame_0 = cap_0.read()
    original = frame_0
    gray_line_1 = cv2.cvtColor(frame_0, cv2.COLOR_BGR2GRAY)

def cam_0_use_line():
    global retval_0, frame_0, original, theta
    blurred = frame_0[frame_crop_y1:frame_crop_y2, frame_crop_x1:frame_crop_x2]
    blurred = cv2.boxFilter(blurred, ddepth=-1, ksize=(31, 31))
    retval2, blurred = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
    edged = cv2.Canny(blurred, 85, 85)
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 10, minLineLength, maxLineGap)
    max_diff = 1000
    final_x = 0
    if lines is not None:
        add_line = 0
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(original, (x1+frame_crop_x1, y1+frame_crop_y1), (x2+frame_crop_x1, y2+frame_crop_y1), (0, 255, 0), 3)
            mid_point = (x1 + x2) / 2
            diff = abs((640/2) - mid_point)
            if max_diff > diff:
                max_diff = diff
                final_x = mid_point
            add_line = add_line + final_x
        average_x = add_line / len(lines)
        if int(average_x) != 0:
            original = cv2.circle(original, (int(average_x), int((frame_crop_y1+frame_crop_y2)/2)), 5, (0, 0, 255), -1)
            original = cv2.rectangle(original, (int(frame_crop_x1), int(frame_crop_y1)), (int(frame_crop_x2), int(frame_crop_y2)), (0, 0, 255), 1)
        frame_0 = original
        cv2.imshow('frame_0', frame_0)
        theta = int((int(average_x) - 320.0) / 640.0 * 100)
        
        # 라인을 따라 움직임을 설정합니다.
        if int(average_x) < (640/2 - 40):  # 중점이 화면 왼쪽에 위치할 때
            # 좌회전 설정
            vel.linear.x = 0.0  # 원하는 선속도 설정
            vel.angular.z = 0.2  # 각속도 설정 (시계 방향 회전)
        elif int(average_x) > (640/2 + 40):  # 중점이 화면 오른쪽에 위치할 때
            # 우회전 설정
            vel.linear.x = 0.0  # 원하는 선속도 설정
            vel.angular.z = -0.2  # 각속도 설정 (반시계 방향 회전)
        else:
            # 직진 설정
            vel.linear.x = 0.02  # 원하는 선속도 설정
            vel.angular.z = 0.0  # 각속도는 0으로 설정

    if lines is None:  # 검출되지 않았을 경우
        theta = -50
        # 정지 설정
        vel.linear.x = 0.0  # 선속도를 0으로 설정
        vel.angular.z = 0.0  # 각속도를 0으로 설정



def cam_0_use_qrcode():
    global barcode_data_line_QR, barcode_type_line_QR
    decoded_line_QR = pyzbar.decode(gray_line_1)
    for qr_code in decoded_line_QR:
        x, y, w, h = qr_code.rect
        barcode_data_line_QR = qr_code.data.decode("utf-8")
        barcode_type_line_QR = qr_code.type
        cv2.rectangle(frame_0, (x, y), (x + w, y + h), (0, 0, 255), 2)
        text_0 = '%s (%s)' % (barcode_data_line_QR, barcode_type_line_QR)
        cv2.putText(frame_0, text_0, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    
    if decoded_line_QR == []:
        barcode_data_line_QR = "QR_X"


# 웹캠 영상 처리
# 웹캠 영상 처리
while True:
    cam_0_read()
    cam_0_use_line()
    cam_0_use_qrcode()
    
    if barcode_data_line_QR == "http://m.site.naver.com/1aDPf":
        # QR 코드의 데이터가 "http://m.site.naver.com/1aDPf"인 경우 움직임을 멈추도록 설정
        vel.linear.x = 0.0  # 선속도를 0으로 설정
        vel.angular.z = 0.0  # 각속도를 0으로 설정
    
    key = cv2.waitKey(1)
    if key == 27:  # ESC 키를 누르면 종료
        break

    # 로봇 이동
    rospy.init_node('cmd_vel_publisher', anonymous=True)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 퍼블리셔의 발행 속도 설정
    pub.publish(vel)  # 움직임 설정을 발행합니다.
    rate.sleep()
