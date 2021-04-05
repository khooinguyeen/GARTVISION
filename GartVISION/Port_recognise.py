import cv2
import numpy as np

import gbvision as gbv

stdv = np.array([10, 80, 80])
# LOGITECH_C922 = gbv.CameraData(697.0395744431028 * 3.67 / 10, 0.61453043 , 0.377863783, is_immutable=True,
#                           name='LOGITECH_C922')
# LOGITECH_C922 = gbv.CameraData(453.4608732, 0.61453043 , 0.377863783, is_immutable=True,
#                           name='LOGITECH_C922')
LOGITECH_C922 = gbv.CameraData(640, 0.61453043 , 0.377863783, is_immutable=True,
                          name='LOGITECH_C922')

THRESHOLD_CONST = gbv.ColorThreshold([[16, 36], [100, 255], [100, 255]], 'HSV')
OBJECT_CONST = gbv.GameObject(0.09680909)
IMAGE_PATH = 'C:\\Users\\admin\\OneDrive\\Desktop\\GARTVISION\\GartVISION\\20cm.png'
def main():
    camera = gbv.USBCamera(1, LOGITECH_C922)
    camera.set_exposure(-5)
    threshold_function = THRESHOLD_CONST + gbv.MedianBlur(5)
    window = gbv.CameraWindow('feed', camera) #tạo window (cửa sổ mới)
    window.open()
    while window.is_opened():
        frame = window._get_frame()
        frame = cv2.flip(frame, 1)

        # frame = cv2.imread(IMAGE_PATH)

        window.show_frame(frame)
        pth = window.last_key_pressed
        if pth == 'r':
            bbox = cv2.selectROI('feed', frame)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()


    print(thr)

    original = gbv.FeedWindow(window_name='original') #ảnh gốc
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr)
    final = gbv.FeedWindow(window_name='final', drawing_pipeline=gbv.DrawRotatedRects( #tạo cửa sổ (bao gồm viền nhận diện ctct,...)
        # threshold_func=threshold_function,  
        threshold_func=thr,  
        color=(255, 0, 0), #tạo viền xanh
        contours_process=gbv.FilterContours(1000),
        rotated_rects_process=gbv.sort_rotated_rects + gbv.filter_inner_rotated_rects #phải sort khoảng cách các thứ mình nhận diện đc
    ))
    finder = gbv.RotatedRectFinder(thr, OBJECT_CONST, contour_min_area=100,
                                rotated_rects_process=gbv.sort_rotated_rects + gbv.filter_inner_rotated_rects)

    original.open()
    after_proc.open()
    final.open()

    kernel = np.ones((5,5), np.uint8)
    while True:
        frame = camera.read()[1]
        frame = cv2.flip(frame, 1)

        # frame = cv2.imread(IMAGE_PATH)

        frame = cv2.erode(frame, kernel, iterations=1)
        frame = cv2.dilate(frame, kernel, iterations=1)
        objects = finder(frame, camera)
        if len(objects):
            print("object is at distance: %s meters" % (gbv.distance_from_object(objects[0]))) #in ra khoảng cách từ cam đến object[0](vật nhận diện gần nhất)
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break
        if not final.show_frame(frame):
            break
        #hiển thị ảnh 

if __name__ == '__main__':
    main()
