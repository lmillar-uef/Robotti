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
from queue import Queue




connected = False
speaker=speakerGpio.Speaker()
motor = motor.tankMotor()
servo = servo.Servo()
servo0_home = 90
servo1_home = 90
motor_speed = 1000




def excecuteCommand(in_q):

	while True:
		print("getting mesage...")
		#get message from queue
		msg = in_q.get()
		print("got.")
		#excecute command
		if msg == "flash":
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
			motor.setMotorModel(0,0)
		if msg == "go forwards":
			 motor.setMotorModel(motor_speed, motor)
		if msg == "go backwards":
			 motor.setMotorModel(-motor_speed, -motor_speed)
		if msg == "turn left":
			motor.setMotorModel(-motor_speed, motor_speed)
		if msg == "turn right":
			motor.setMotorModel(motor_speed, -motor_speed)
		if msg == "off":
			sock.shutDown()
			break
		print("exceuted")
		in_q.task_done()
    

	    
def listenForCommand(out_q):
	while True:
		print("Listening...")
		#ledi.colorWipe((0, 255, 0))
		msg = sock.listenSock()
		print(msg)
		##put msg in queue for excecution
		out_q.put(msg)
		if msg == "kys":
			break #bomboclat


##CONNECTION
while connected == False:
	connected = sock.connectSock() ### Jetson send "connectd" -> connected True
	if sock.listenSock() == "connected":
		connected = True
		print("connected")
		ledi = led.Led()
		
##Two threads for excecuting and listening
enderChest = Queue()
excecute = Thread(target = excecuteCommand, args = (enderChest,))
listen = Thread(target = listenForCommand, args = (enderChest,))
listen.start()
excecute.start()

enderChest.join()


	

