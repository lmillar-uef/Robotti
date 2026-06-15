from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

class Speaker:
    def __init__(self):
        self.channel = 19
        self.PwmSpeaker = TonalBuzzer(self.channel)

    def playFrequency(self, tone):
        #tone voi olla joko int(freq) -> esim. 440, 131
        #tai str(tone) -> esim. "A4", "C3"
       self.PwmSpeaker.play(Tone(tone)) #tone voi olla joko int(freq) -> esim 

    def stop(self):
       self.PwmSpeaker.stop()
