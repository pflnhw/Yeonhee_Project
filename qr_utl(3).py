import cv2
from pyzbar import pyzbar
import webbrowser

def read_qrcode():
    # 웹캠 열기
    cap = cv2.VideoCapture(0)

    while True:
        # 웹캠에서 프레임 읽기
        _, frame = cap.read()

        # 프레임에서 QR 코드 인식
        decoded_objects = pyzbar.decode(frame)

        # 인식된 QR 코드가 있을 경우 처리
        if decoded_objects:
            # 첫 번째로 인식된 QR 코드 가져오기
            qr_code_data = decoded_objects[0].data.decode('utf-8')

            # 웹사이트 열기
            webbrowser.open(qr_code_data)

            break

        # 프레임 출력
        cv2.imshow('QR Code Scanner', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 웹캠과 창 닫기
    cap.release()
    cv2.destroyAllWindows()

# QR 코드 인식 및 웹사이트로 이동 실행
read_qrcode()
