import gbvision as gbv #define

THRESHOLD_CONST = gbv.ColorThreshold([[16, 36], [100, 255], [100, 255]], 'HSV')

OBJECT_CONST = gbv.GameObject(0.02482866647577738982015034781317) #diện tích 2D của power cell



def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    threshold_function = THRESHOLD_CONST + gbv.MedianBlur(5)
    finder = gbv.CircleFinder(threshold_function, OBJECT_CONST, contour_min_area=100,
                            circles_process=gbv.sort_circles + gbv.filter_inner_circles)
    window = gbv.CameraWindow('feed', camera, drawing_pipeline = gbv.DrawCircles(
        threshold_func=threshold_function,
        color=(0, 0, 255), #(0xe4, 0xc8, 0x27)
        contours_process=gbv.FilterContours(1000),
        circle_process=gbv.sort_circles + gbv.filter_inner_circles
    ))
    window.open()
    while window.is_opened():
        frame=window.show_and_get_frame()
        objects = finder(frame, camera)
        if len(objects):
            print("khoảng cách là: %s meters" % (gbv.distance_from_object(objects[0])))
    window.close()


if __name__ == '__main__':
    main()




