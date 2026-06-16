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


motorCommands   = ["autobots", "go forwards", "go backwards", "turn left", "turn right"]
ledCommands     = ["I love you", "flash"]
servoCommands   = ["servo"]
speakerCommands = ["play"]
eventCommands   = ["stop", "start", "off"]

unpaused_event  = threading.Event() ##basically pause
off_event   = threading.Event()

connected = False
speaker   = speakerGpio.Speaker()
servo     = servo.Servo()


##LISTENING
def listenForCommand(out_q):
	while True:
		print("Listening...")
		msg = sock.listenSock()
		print(msg)
		if msg == "stop" or msg == "pause":
		    unpause_event.clear()
		else:
		    unpause_event.set()
		    ##put msg in queue for excecution
		    out_q.put(msg)
		    if msg == "off":
			    break #bomboclat
		



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
    msg = cmd.get()
    if msg == "autobots":
		car.test_car_sonic()
		
def ledCommand(cmd):
    msg = cmd.get()
    if msg == "flash":
		ledi.theaterChaseRainbow()
	if msg == "I love you":
		ledi.colorWipe((255, 0, 0))
		
def servoCommand(cmd):
    msg = cmd.get()
    if msg == "servo":	
		servo.setServoAngle('0', 50)
		servo.setServoAngle('1', 70) 
		time.sleep(2)
		servo.setServoAngle('0', servo.init0_angle)
		servo.setServoAngle('1', servo.init1_angle)  
	
def speakerCommand(cmd):
    msg = cmd.get()
    if msg == "play":	
		speaker.playFrequency("A4")
	if msg == "stop":		
			speaker.stop()


##CONNECTION
while connected == False:
	connected = sock.connectSock() ### Jetson send "connectd" -> connected True
	if sock.listenSock() == "connected":
		connected = True
		print("connected")
		ledi = led.Led()
		

##make a queue to communicate between threads
q_com = Queue()

q_mot = Queue()
q_ser = Queue()
q_led = Queue()
q_spe = Queue()

##Different threads for listening, excecuting (+motor, servo, leds, speaker)
excecute = Thread(target = excecuteCommand, args = (q_com,))
listen   = Thread(target = listenForCommand, args = (q_com, q_mot, q_spe, q_ser, q_led))

motor   = Thread(target = motorCommand, args = (q_mot,))
speaker = Thread(target = speakerCommand, args = (q_spe,))
servo   = Thread(target = servoCommand, args = (q_ser,))
led     = Thread(target = ledCommand, args = (q_led,))

# start threads
listen.start()
excecute.start()
motor.start()
speaker.start()
servo.start()
led.start()
override.start()

enderChest.join()


	

