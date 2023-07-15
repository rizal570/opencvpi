# Python code for Multiple Color Detection


import numpy as np
import cv2
import RPi.GPIO as GPIO
import time


# Capturing video through webcam
webcam = cv2.VideoCapture(0)
_,imageFrame = webcam.read()
rows, cols,_ = imageFrame.shape

# setup the GPIO pin for the servo
servo_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

# setup PWM process
pwm = GPIO.PWM(servo_pin,50) # 50 Hz (20 ms PWM period)
x_medium =int(cols / 2)
center = int(cols / 2)
pwm.start(0) # start PWM by rotating to 90 degrees


# Start a while loop
while webcam.isOpened():
	
	# Reading the video from the
	# webcam in image framesq
	_, imageFrame = webcam.read()

	# Convert the imageFrame in
	# BGR(RGB color space) to
	# HSV(hue-saturation-value)
	# color space
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

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
	res_red = cv2.bitwise_and(imageFrame, imageFrame,
							mask = red_mask)
	


	# Creating contour to track red color
	contours, hierarchy = cv2.findContours(red_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	contours =sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 300):
			x, y, w, h = cv2.boundingRect(contour)
			x_medium = int((x + x + w) / 2)
			break
			
			cv2.putText(imageFrame, "Orange Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX, 1.0,
						(0, 0, 255))	
	cv2.line(imageFrame, (x_medium,0), (x_medium, 480),(0, 255, 0), 2)
	# Program Termination
	cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		break
		
	#move servo
if x_medium < center:
	pwm.ChangDutyCycle(12.5)
elif x_medium > center:
	pwm.ChangDutyCycle(4)
	

GPIO.cleanup()
webcam.release()
cv2.destroyAllWindows()
	
	
