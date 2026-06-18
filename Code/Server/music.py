import speakerGpio
import time

class Music():
        def __init__(self):
                self.imperial_march = [["A4", 1],
                ["A4", 1],
                ["A4", 1],
                ["F4", 0.75],
                ["C5", 0.25],
                ["A4", 1],
                ["F4", 0.75],
                ["C5", 0.25],
                ["A4", 2],
                ["E5", 1],
                ["E5", 1],
                ["E5", 1],
                ["F5", 0.75],
                ["C5", 0.25],
                [415, 1],
                ["F4", 0.75],
                ["C5", 0.25],
                ["A4", 2]]
                self.no_surprises = [["A5", 0.5],
                ["C5", 0.5],
                ["F5", 0.5],
                ["C5", 0.5],
                
                ["A5", 0.5],
                ["C5", 0.5],
                ["F5", 0.5],
                ["C5", 0.5],
                
                ["A5", 0.5],
                ["C5", 0.5],
                ["F5", 0.5],
                ["C5", 0.5],
                
                ["Bb4", 0.5],
                ["Db5", 0.5],
                ["F5", 0.5],
                ["G5", 0.5]]
                
                self.imperial_march_bpm = 100
                self.no_surprises_bpm = 67
                
                self.music_index = 0


        def playSong(self, speaker, song, bpm):
                while self.music_index >= len(song):
                        self.music_index -= len(song)
                print(self.music_index)
                speaker.playFrequency(song[self.music_index][0])
                time.sleep(song[self.music_index][1]*60/bpm)
                self.music_index += 1
                speaker.stop()
                time.sleep(0.05)
                
