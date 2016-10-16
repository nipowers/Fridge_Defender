import picamera #PiCamera library
import datetime #DateTime library to allow for time stamping
import RPi.GPIO as GPIO #Enable GPIO functionality for the Raspberry Pi
from time import sleep #Import sleep function to allow for code to sit quietly in the background until needed
import os #Allow for command line interaction with other scripts


#Set up pin 18 for the switch input
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Make a camera object
camera = picamera.PiCamera()

#Define a capture funtion that will run when the switch GPIO is triggered
def Capture(self):
	#Capture current date and time to stamp photo and video with
    append_time = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%MZ")
    
	#Capture an image of the food thief
    camera.capture('test_%s.jpg'% append_time)

	#Set camera resolution and image rotation
    camera.resolution = (640, 480)
	camera.rotation = 180
	
	#Capture a 10 second video to see what the theif took
    camera.start_recording('test_%s.h264'% append_time)
    camera.wait_recording(10)
    camera.stop_recording()

	#Create a string of the file name that will be sent
    to_send = str('test_%s.jpg'% append_time)
	#Activate the emailing script and pass it the image file name
    os.system("python send_attachement_input.py %s" % to_send)

#Create the switch event, set as RISING so that it detects the switch opening instead of closing
GPIO.add_event_detect(18, GPIO.RISING, callback = Capture, bouncetime = 2000)

#Start code and sleep waiting for a theif to come and try their luck
while 1:
    sleep(1)
