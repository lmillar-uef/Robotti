from servo import Servo
from motor import tankMotor
from led import Led
from speakerGpio import Speaker
from car import Car
import ultrasonic
#import infrared
#import camera
import sockClient as sock
from threading import Thread
from threading import Event
import time
from queue import Queue

## ALL COMMANDS
motor_commands   = ["off", "autobots", "go forwards", "go backwards", "turn left", "turn right"]
led_commands     = ["off", "I love you", "flash"]
servo_commands   = ["off", "servo"]
speaker_commands = ["off", "play"]
override_commands= ["off", "stop", "pause"]

## initialise lists
threads = []

## events used
unpaused_event  = Event() #always on (except when you want to pause robot)
unpaused_event.set()
off_event       = Event() 
sonic_mode_event = Event()

## make instances of devices
speaker   = Speaker()
motor     = tankMotor()
servo     = Servo()
led       = Led()
car       = Car(servo, motor)

## setting default values
connected = False
servo0_home = 90
servo1_home = 90
motor_speed = 1400



##############################################################


##LISTENING
def listenForCommand(out_q):
	while True:
		print("Listening...")
		msg = sock.listenSock()
		print(msg)

		#event to tell if robot needs to stop everything it is doing
		if msg == "stop" or msg == "pause":
			print("pausing...")
			unpaused_event.clear()
		elif not unpaused_event.is_set():
			unpaused_event.set()
		
		##put msg in queue for excecution
		out_q.put(msg)
			
		if msg == "off":
			off_event.set()
			break 
		

############################################################################


##EXCECUTING
def excecuteCommand(in_q, q_mot, q_spe, q_ser, q_led, q_override):
	while True:
		#get message from queue
		msg = in_q.get()
		
		if msg in override_commands:
		    q_override.put(msg)
		
		unpaused_event.wait() ##Stops here if unpaused event is cleared 
	
		#send command to the right thread
		if msg in motor_commands:
		    q_mot.put(msg)
		if msg in speaker_commands:
		    q_spe.put(msg)
		if msg in servo_commands:
		    q_ser.put(msg)
		if msg in led_commands:
		    q_led.put(msg)
		
		    
		#excecute in this thread
		if msg == "ping":
			sock.sendMessage("pong")
		if msg == "off":
			sock.shutDown()
			break
			
		#mark as done
		in_q.task_done()

######################################################

def motorCommand(cmd):
	while True:
		#print("m...")
		msg = cmd.get()
		if msg == "autobots":
			sonic_mode_event.set()
		if msg == "go forwards":
			motor.setMotorModel(motor_speed, motor_speed)
		if msg == "go backwards":
			motor.setMotorModel(-motor_speed, -motor_speed)
		if msg == "turn left":
			motor.setMotorModel(-motor_speed, motor_speed)
		if msg == "turn right":
			motor.setMotorModel(motor_speed, -motor_speed)
		if msg == "off":
			break
		cmd.task_done()
		
def carCommand():
	while True:
		if off_event.is_set():
			car.close()
			break
		unpaused_event.wait()
		if sonic_mode_event.is_set():
			car.mode_ultrasonic()	
		
def ledCommand(cmd):
	while True:
		#print("l..")
		msg = cmd.get()
		if msg == "flash":
			led.theaterChaseRainbow()
		if msg == "I love you":
			led.colorWipe((255, 0, 0))
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
		if msg == "stop" or msg == "pause":
			#speaker
			speaker.stop()
			#motor
			motor.setMotorModel(0,0)
			#led
			led.colorWipe((0, 0, 0))
			#servo command????
			sonic_mode_event.clear()
			print("paused")
		if msg == "off":
			break	
		cmd.task_done()


#############################################

##CONNECTION
while connected == False:
	connected = sock.connectSock() ### Jetson send "connected" -> connected True
	if sock.listenSock() == "connected":
		connected = True
		

##make a queue to communicate between threads
q_com = Queue()  #listening and delegating
q_mot = Queue()  #motor specific
q_ser = Queue()  #servo specific
q_led = Queue()  #led specific
q_spe = Queue()  #speaker specific
q_override = Queue()  #commands that need to override everything, for ex. "off" or "pause"

##Different threads for listening, excecuting (+motor, servo, leds, speaker)
threads.append(Thread(target = listenForCommand, args = (q_com,)))                                        #listening for incoming commands
threads.append(Thread(target = excecuteCommand, args = (q_com, q_mot, q_spe, q_ser, q_led, q_override)))  #delegating commands to respective excecutor threads

threads.append(Thread(target = motorCommand, args = (q_mot,)))                                            #motor command excecutor
threads.append(Thread(target = speakerCommand, args = (q_spe,)))                                          #speaker command excecutor
threads.append(Thread(target = servoCommand, args = (q_ser,)))                                            #servo command excecutor
threads.append(Thread(target = ledCommand, args = (q_led,)))                                              #led command excecutor
threads.append(Thread(target = carCommand))                                                               #car/preset modes excecutor

threads.append(Thread(target = overrideCommand, args = (q_override,)))                                    #overall overriding command excecutor

# start threads
for t in threads:
	t.start()

#wait until "off" command is given
off_event.wait()

#merge all threads to this one 
for t in threads:
	t.join()


	

