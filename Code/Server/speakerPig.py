import pigpio

class Speaker:
   def __init__(self):
       self.channel = 19
       self.PwmSpeaker = pigpio.pi()
       self.PwmSpeaker.set_mode(self.channel, pigpio.OUTPUT)
       self.PwmSpeaker.set_PWM_frequency(self.channel, 440)
       self.PwmSpeaker.set_PWM_range(self.channel, 100)

   def playFrequency(self, freq):
       self.PwmSpeaker.set_PWM_frequency(self.channel, freq)

   def stop(self):
       self.PwmSpeaker.set_PWM_dutycycle(self.channel, 0)
