import speaker
import time

imperial_march = [["A4", 1],
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
#no_surprises = [[note, dur],
             #   [note, dur]]
             
imperial_march_bpm = 100
no_surprises_bpm = 100


def playSong(speaker, song, i, bpm):
    while i >= song.len():
        i -= song.len()
    print(i)
    speaker.play(song[i][0])
    time.sleep(song[i][1]*60/bpm)
