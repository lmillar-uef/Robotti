import  servo
import servoForSpeaker
import motor
import ultrasonic
#import infrared
import led
#import camera
import sock


connected = False

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
	if msg == "I love you":
		ledi.colorWipe((255, 0, 0))
		
		
	

