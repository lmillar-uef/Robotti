import  servo
import motor
import ultrasonic
#import infrared
import led
#import camera
import speakerGpio
import sockClient as sock
from threading import Thread
from threading import Event
import time
import car
from queue import Queue


motorCommands   = ["off", "autobots", "go forwards", "go backwards", "turn left", "turn right"]
ledCommands     = ["off", "I love you", "flash"]
servoCommands   = ["off", "servo"]
speakerCommands = ["off", "play"]
#eventCommands   = ["stop", "start", "off", "pause"]

unpaused_event  = Event() ##basically pause
off_event       = Event() 

connected = False

speaker = speakerGpio.Speaker()
motor   = motor.tankMotor()
servo   = servo.Servo()

servo0_home = 90
servo1_home = 90
motor_speed = 1400




##LISTENING
def listenForCommand(out_q):
	while True:
		#print("Listening...")
		msg = sock.listenSock()
		#print(msg)
		if msg == "stop" or msg == "pause":
			#print("pausing...")
			unpaused_event.clear()
			speaker.stop()
			motor.setMotorModel(0,0)
			#print("paused")
		else:
			#print("unpaused")
			unpaused_event.set()
		    ##put msg in queue for excecution
			out_q.put(msg)
			if msg == "off":
				off_event.set()
				break 
		



##EXCECUTING
def excecuteCommand(in_q, q_mot, q_spe, q_ser, q_led):
	while True:
		unpaused_event.wait() ##Stops here if unpaused event is cleared
		
		#get message from queue
		msg = in_q.get()
		
		#send command to the right thread
		if msg in motorCommands:
		    q_mot.put(msg)
		if msg in speakerCommands:
		    q_spe.put(msg)
		if msg in servoCommands:
		    q_ser.put(msg)
		if msg in ledCommands:
		    q_led.put(msg)
		    
		#excecute in this thread
		if msg == "ping":
			sock.sendMessage("pong")
		if msg == "off":
			sock.shutDown()
			break
			
		#mark as done
		in_q.task_done()


def motorCommand(cmd):
	while True:
		#print("m...")
		msg = cmd.get()
		if msg == "autobots":
			car.test_car_sonic()
		if msg == "go forwards":
			#print("forwards...")
			motor.setMotorModel(motor_speed, motor_speed)
			#print("going.....")
		if msg == "go backwards":
			motor.setMotorModel(-motor_speed, -motor_speed)
		if msg == "turn left":
			motor.setMotorModel(-motor_speed, motor_speed)
		if msg == "turn right":
			motor.setMotorModel(motor_speed, -motor_speed)
		if msg == "off":
			break
		cmd.task_done()
		
def ledCommand(cmd):
	while True:
		#print("l..")
		msg = cmd.get()
		if msg == "flash":
			ledi.theaterChaseRainbow()
		if msg == "I love you":
			ledi.colorWipe((255, 0, 0))
		if msg == "off":
			break
		cmd.task_done()
		
def servoCommand(cmd):
	while True:
		#print("s..")
		msg = cmd.get()
		if msg == "servo":	
			servo.setServoAngle('0', 100)
			servo.setServoAngle('1', 100) 
			time.sleep(2)
			servo.setServoAngle('0', servo.init0_angle)
			servo.setServoAngle('1', servo.init1_angle)  
		if msg == "off":
			break
		cmd.task_done()
	
def speakerCommand(cmd):
	while True:
		#print("sp..")
		msg = cmd.get()
		if msg == "play":	
			speaker.playFrequency("A4")
		if msg == "stop":		
			speaker.stop()
		if msg == "off":
			break	
		cmd.task_done()
	
def overrideCommand(cmd):
	while True:
		msg = cmd.get()
		if msg == "off":
			break	
		cmd.task_done()


##CONNECTION
while connected == False:
	connected = sock.connectSock() ### Jetson send "connectd" -> connected True
	if sock.listenSock() == "connected":
		connected = True
		#print("connected")
		ledi = led.Led()
		

unpaused_event.set()

##make a queue to communicate between threads
q_com = Queue()

q_mot = Queue()
q_ser = Queue()
q_led = Queue()
q_spe = Queue()
q_override = Queue()

##Different threads for listening, excecuting (+motor, servo, leds, speaker)
excecute = Thread(target = excecuteCommand, args = (q_com, q_mot, q_spe, q_ser, q_led))
listen   = Thread(target = listenForCommand, args = (q_com,))

motor_t    = Thread(target = motorCommand, args = (q_mot,))
speaker_t  = Thread(target = speakerCommand, args = (q_spe,))
servo_t    = Thread(target = servoCommand, args = (q_ser,))
led_t      = Thread(target = ledCommand, args = (q_led,))
override_t = Thread(target = overrideCommand, args = (q_override,))

# start threads
listen.start()
excecute.start()
motor_t.start()
speaker_t.start()
servo_t.start()
led_t.start()
override_t.start()


off_event.wait()
#print("joining threads...")
listen.join()
excecute.join()
motor_t.join()
speaker_t.join()
servo_t.join()
led_t.join()
override_t.join()


	

