import cv2
import numpy as np

import gbvision as gbv

stdv = np.array([10, 80, 80])

#threshold là phân ngưỡng ảnh


def main():
    camera = gbv.USBCamera(0) #tạo camera (chuyển thành 1 nếu dùng webcam)
    camera.set_exposure(-5) #điều chình giá trị đo sáng 
    window = gbv.CameraWindow('feed', camera) #tạo window (cửa sổ mới)
    window.open()
    while True: #lặp lại mãi mãi
        frame = window.show_and_get_frame() #tạo và lấy frame
        k = window.last_key_pressed  #tạo k là phím đầu được nhấn từ bàn phím
        if k == 'r':
            bbox = cv2.selectROI('feed', frame) #chọn vùng quan tâm (ROI là Region of interest)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV') #tạo threshold
            break #tắt cửa sổ cũ
    cv2.destroyAllWindows()
    


    print(thr) #in ra phần threshold 

    original = gbv.FeedWindow(window_name='original') #tạo ảnh gốc
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr) #tạo ảnh sau khi threshold

    original.open() #mở ảnh
    after_proc.open() #mở ảnh
    while True:
        ok, frame = camera.read()
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break
        #hiển thị ảnh trc và sau threshold

    original.close() #đóng
    after_proc.close()


if __name__ == '__main__':
    main()