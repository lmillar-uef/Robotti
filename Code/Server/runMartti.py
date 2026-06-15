import  servo
import motor
import ultrasonic
#import infrared
import led
#import camera
import speakerGpio
import sockClient as sock
from threading import Thread
import time
import car

connected = False
speaker=speakerGpio.Speaker()
servo = servo.Servo()
servo0_home = 90
servo1_home = 90


while connected == False:
	connected = sock.connectSock() ### Jetson send "connectd" -> connected True
	if sock.listenSock() == "connected":
		connected = True
		print("connected")
		ledi = led.Led()
	
while True:
	print("Listening...")
	msg = sock.listenSock()
	print(msg)
	if msg == "chase":
		ledi.theaterChaseRainbow()
	if msg == "ultra":
		 car.test_car_sonic()
	if msg == "I love you":
		ledi.colorWipe((255, 0, 0))
	if msg == "ping":
	    sock.sendMessage("pong")
	if msg == "play":	
		speaker.playFrequency("A4")
	if msg == "autobots":	
		servo.setServoAngle('0', 50)
<<<<<<< HEAD
		servo.setServoAngle('1',70)   
=======
		servo.setServoAngle('1', 70) 
		time.sleep(2)
		servo.setServoAngle('0', servo0_home)
		servo.setServoAngle('1', servo1_home)  
>>>>>>> refs/remotes/origin/master
	if msg == "stop":		
		speaker.stop()
	if msg == "kys":
	    sock.shutDown()
	    break

	

