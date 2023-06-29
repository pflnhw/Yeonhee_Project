import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time


# 캠켜기:  
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

time.sleep(2)
 # qr코드 해석(디코딩)
def decode(im) : 
   
    decodedObjects = pyzbar.decode(im)
    # 주소 print
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while(cap.isOpened()):
    # 실행 내역 및 프레임 가져오기
    ret, frame = cap.read()
    # 캠화면 이미지
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 가져온 이미지 해석    
    decodedObjects = decode(im)

    for decodedObject in decodedObjects: 
        points = decodedObject.polygon
     
        # 좌표지정 (points)
        if len(points) > 4 :
          # convexHull 블록(4각형의 qr코드)의 좌표계산 hull= 좌표할당 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points
          
        n = len(hull)     

        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)
        # 해당 코드에 왼쪽상단 좌표
        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)
        # 무슨타입인지 (바코드 or QR코드)
        print('Type : ', decodedObject.type)
        # qr코드 읽어서 결과 출력
        print('Data : ', decodedObject.data,'\n')

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
               
    # 화면띄우기
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break   

cap.release()
cv2.destroyAllWindows()