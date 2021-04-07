from _pynetworktables.instance import NetworkTablesInstance
import cv2
import numpy as np
import threading
import gbvision as gbv
import time
import logging
from networktables import NetworkTables
import sys

# cond = threading.Condition()
# notified = [False]

# def connectionListener(connected, info):
#     print(info, '; Connected=%s' % connected)
#     with cond:
#         notified[0] = True
        # cond.notify()





# table = NetworkTablesInstance.getTable('SmartDashboard')
# foo = table.getBoolean('foo', True)


# subtable = table.getSubTable('bar')
# baz = table.getNumber('baz', 1)





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

    # if len(sys.argv) != 2:
    #     print("Error: specify an IP to connect to!")
    #     exit(0)

    # ip = sys.argv[1]
    # print(ip)
    # exit(0) //no need

    # NetworkTables.initialize(server='10.65.20.2')
    # NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # with cond:
    #     print("Waiting")
    #     if not notified[0]:
    #         cond.wait()

    # # Insert your processing code here
    # print("Connected!")



    # logging.basicConfig(level=logging.DEBUG)
    # sd = NetworkTables.getTable("vision")

    camera = gbv.USBCamera(0, LOGITECH_C922)
    camera.set_exposure(-5)
    threshold_function = THRESHOLD_CONST + gbv.MedianBlur(5)
    window = gbv.CameraWindow('feed', camera) #tạo window (cửa sổ mới)
    window.open()
    while window.is_opened():
        frame = window._get_frame()
        frame = cv2.flip(frame, 1)

        #frame = cv2.imread(IMAGE_PATH)

        window.show_frame(frame)
        pth = window.last_key_pressed
        if pth == 'r':
            bbox = cv2.selectROI('feed', frame)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()

    print('hi')
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

        #frame = cv2.imread(IMAGE_PATH)

        frame = cv2.erode(frame, kernel, iterations=1)
        frame = cv2.dilate(frame, kernel, iterations=1)
        objects = finder(frame, camera)
        if len(objects):
            print("object is at distance: %s meters" % (gbv.distance_from_object(objects[0])))
            # i = gbv.distance_from_object(objects[0])
            #  #in ra khoảng cách từ cam đến object[0](vật nhận diện gần nhất)
            # sd.putNumber("Port distance", i)
            # time.sleep(1)

        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break
        if not final.show_frame(frame):
            break
        #hiển thị ảnh 

if __name__ == '__main__':
    main()
