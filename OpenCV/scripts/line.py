import cv2
import numpy as np

cap = cv2.VideoCapture('/home/go/pro/helloworld/res/20230706_131228.mp4')

while True:
    ret, frame = cap.read()

    # 바닥 이미지를 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 검은색에 대한 임계값 범위 설정
    lower_black = np.array([0, 0, 0], dtype=np.uint8)
    upper_black = np.array([179, 255, 30], dtype=np.uint8)

    # 임계값 적용하여 검은 선 영역 추출
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # 사다리꼴 모양 영역 생성
    height, width = frame.shape[:2]
    roi_vertices = np.array([[(0, height), (width // 2 + width // 4, height // 2 - height // 4),
                             (width // 2 + width // 4, height // 2 - height // 4), (width, height)]], dtype=np.int32)

    # 사다리꼴 모양 영역 내의 검은 선 영역을 녹색으로 표시
    roi_mask = np.zeros_like(mask)
    cv2.fillPoly(roi_mask, roi_vertices, 255)
    roi_masked = cv2.bitwise_and(mask, roi_mask)
    frame[np.where(roi_masked == 255)] = [0, 255, 0]

    cv2.imshow('Black Line Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
