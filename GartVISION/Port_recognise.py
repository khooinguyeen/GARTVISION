import cv2
from gbvision.gui.window import Window
from gbvision.models.contours import sort_circles, sort_contours
import numpy as np

import gbvision as gbv

stdv = np.array([10, 80, 80])
THRESHOLD_CONST = gbv.ColorThreshold([[16, 36], [100, 255], [100, 255]], 'HSV')
OBJECT_CONST = gbv.GameObject(0.20706279240848655)

def main():
    camera = gbv.USBCamera(1, gbv.LIFECAM_3000)
    camera.set_exposure(-8)
    threshold_function = THRESHOLD_CONST + gbv.median_blur(5)
    finder = gbv.ContourFinder(threshold_function, OBJECT_CONST, contour_min_area=100,
                                contours_process=gbv.sort_contours + gbv.filter_inner_convex_shapes)
    window = gbv.CameraWindow('feed', camera, drawing_pipeline = gbv.DrawContours(
        threshold_func=threshold_function,
        color = (0, 255, 0),
        contours_process=gbv.FilterContours(1000),
        contours_process=gbv.sort_contours + gbv.filter_inner_convex_shapes
    ))
    window.open()
    while window.is_opened():
        frame = window.show_and_get_frame()
        objects = finder(frame, camera)
        pth = window.last_key_pressed
        if pth == 'r':
            bbox = cv2.selectROI('feed', frame)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()


    print(thr)

    original = gbv.FeedWindow(window_name='original') #ảnh gốc
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr)
    final = gbv.FeedWindow(window_name='final', )





