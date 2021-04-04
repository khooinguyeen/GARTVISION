import gbvision as gbv

THRESHOLD_CONST = gbv.ColorThreshold([[16, 36], [100, 255], [100, 255]], 'HSV')
# lấy đc nhờ threshold
# HSV range của màu mình cần nhận diện

OBJECT_CONST = gbv.GameObject(0.20706279240848655) #diện tích 2d của vật mình cần nhận diện


def main():
    camera = gbv.USBCamera(1, gbv.LIFECAM_3000) #khởi tạo camera (nhớ ghi port với cam, chỉ số cam )
    threshold_function = THRESHOLD_CONST + gbv.MedianBlur(5) 
    finder = gbv.RotatedRectFinder(threshold_function, OBJECT_CONST, contour_min_area=100,
                                   rotated_rects_process=gbv.sort_rotated_rects + gbv.filter_inner_rotated_rects)#ấn ctrl + chuột trái để hiểu rõ hơn :)) 
    window = gbv.CameraWindow('feed', camera, drawing_pipeline=gbv.DrawRotatedRects( #tạo cửa sổ (bao gồm viền nhận diện ctct,...)
        threshold_func=threshold_function,  
        color=(255, 0, 0), #tạo viền xanh
        contours_process=gbv.FilterContours(1000),
        rotated_rects_process=gbv.sort_rotated_rects + gbv.filter_inner_rotated_rects #phải sort khoảng cách các thứ mình nhận diện đc
    ))
    window.open() #mở cửa sổ
    while window.is_opened():
        frame = window.show_and_get_frame() #tạo frame và lấy frame
        objects = finder(frame, camera) #vật cần nhận diện
        if len(objects):
            print("object is at distance: %s meters" % (gbv.distance_from_object(objects[0]))) #in ra khoảng cách từ cam đến object[0](vật nhận diện gần nhất)
    window.close() 


if __name__ == '__main__':
    main()