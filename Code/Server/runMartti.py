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



def excecuteCommand(msg):
    if msg == "chase":
		ledi.theaterChaseRainbow()
	if msg == "autobots":
		 car.test_car_sonic()
	if msg == "I love you":
		ledi.colorWipe((255, 0, 0))
	if msg == "ping":
	    sock.sendMessage("pong")
	if msg == "play":	
		speaker.playFrequency("A4")
	if msg == "servo":	
		servo.setServoAngle('0', 50)
		servo.setServoAngle('1', 70) 
		time.sleep(2)
		servo.setServoAngle('0', servo0_home)
		servo.setServoAngle('1', servo1_home)  
	if msg == "stop":		
		speaker.stop()
	if msg == "kys":
	    sock.shutDown()
	    break

excecute = Thread(target = excecuteCommand, args = ())


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
	excecute = Thread(target = excecuteCommand, args = (msg,))
	excecute.start()
	

	

