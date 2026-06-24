import speakerGpio
import time

##################
happy_sound = [["C5",1],
["A4",1],
["C5",0.5],
["A4",0.5],
["G4",0.5],
["E5",1]]

sad_sound = [["C5", 1], 
["Ab4", 2],
["E4",1],
["F4",2]]
 
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
                ["A4", 2],
                ["A5",1],
                ["A4",0.75],
                ["A4",0.25],
                ["A5",1],
                ["Ab5",0.75],
                ["G5",0.25],
                ["Gb5", 0.33],
                ["F5", 0.33],
                ["Gb5",0.33],
                [0,0.5],
                ["Bb4",0.5],
                ["Eb5",1],
                ["D5",0.75],
                ["Db5",0.25],
                ["C5",0.33],
                ["B4",0.33],
                ["C5",0.33],
                [0,0.5],
                ["F4",0.5],
                ["Ab4",1],
                ["F4",0.75],
                ["Ab4",0.25],
                ["C5",1],
                ["A4",0.75],
                ["C5",0.25],
                ["E5",2],
                ["A5",1],
                ["A4",0.75],
                ["A4",0.25],
                ["A5",1],
                ["Ab5",0.75],
                ["G5",0.25],
                ["Gb5", 0.33],
                ["F5", 0.33],
                ["Gb5",0.33],
                [0,0.5],
                ["Bb4",0.5],
                ["Eb5",1.],
                ["D5",0.75],
                ["Db5",0.25],
                ["C5",0.33],
                ["B4",0.33],
                ["C5",0.33],
                [0,0.5],
                ["F4",0.5],
                ["Ab4",1],
                ["F4",0.75],
                ["C5",0.25],
                ["A4",1],
                ["F4",0.75],
                ["C5",0.25],
                ["A4",2]]
                
                
                
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
                self.robot_sounds = [happy_sound,sad_sound]
                self.imperial_march_bpm = 100
                self.no_surprises_bpm = 67
                self.happy_sound_bpm = 150
                
                self.music_index = 0


        def playSong(self, speaker, song, bpm):
                while self.music_index >= len(song):
                        self.music_index -= len(song)
                if song[self.music_index][0] == 0:
                        speaker.stop()
                else:
                        speaker.playFrequency(song[self.music_index][0])
                time.sleep(song[self.music_index][1]*60/bpm)
                self.music_index += 1
                speaker.stop()
                time.sleep(0.05)
                
        def playSound(self, speaker, index, bpm):
                if self.music_index >= len(self.robot_sounds[index]):
                        return
                if self.robot_sounds[index][self.music_index][0] == 0:
                        speaker.stop()
                else:  
                        speaker.playFrequency(self.robot_sounds[index][self.music_index][0])
                time.sleep(self.robot_sounds[index][self.music_index][1]*60/bpm)
                self.music_index += 1
                speaker.stop()
                time.sleep(0.05)
