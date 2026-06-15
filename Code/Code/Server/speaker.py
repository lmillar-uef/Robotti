from servoForSpeaker import Servo
import time

speaker = Servo()

try:
    while True:
        for i in range(440, 880, 10):       
            speaker.setServoAngle('1', 100, i)
            time.sleep(1)
        

except KeyboardInterrupt:
    speaker.setServoStop()
    speaker.setServoStop()
