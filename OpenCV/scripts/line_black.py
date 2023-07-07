import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 이미지 전처리, 가우시안블루
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # 검은색상, 감지 범위 설정
    height, width = edges.shape[:2]
    roi_vertices = np.array([[(0, height), (width, height), (width//2, height//2)]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, roi_vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # 허프변환 라인검출
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=100)

    # 검출된 라인 중에서 일정 크기의 검은 테이프만을 선택하여 표시
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if line_length > 100 and line_length < 300:  # 일정 크기의 선 설정
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    cv2.imshow('Lane Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()