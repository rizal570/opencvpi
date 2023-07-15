from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30


raw_capture = PiRGBArray(camera, size=(320,240))

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    img = frame.array

    # Start a while loop
    
        # Convert the imageFrame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Set range for red color and
        # define mask
    red_lower = np.array([5, 50, 50], np.uint8)
    red_upper = np.array([15, 255, 255], np.uint8)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        
        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
    kernel = np.ones((5, 5), "uint8")
        
        # For red color
    red_mask = cv2.dilate(red_mask, kernel)
        
        


        # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
        
    for pic, contour in enumerate(contours):
         area = cv2.contourArea(contour)
         if(area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(img, (x, y),
                                        (x + w, y + h),
                                        (0, 0, 255), 2)
                
            cv2.putText(imageFrame, "Orange Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))	

    cv2.imshow("Multiple Color Detection in Real-TIme", img)
    raw_capture.truncate(0)
    if cv2.waitKey(10) & 0xFF == ord('q'):
       break
