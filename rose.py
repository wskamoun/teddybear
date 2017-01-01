# Alexa Personal Assitant for Raspberry Pi
# Coded by Simon Beal and Matthew Timmons-Brown for "The Raspberry Pi Guy" YouTube channel
# Built upon the work of Sam Machin, (c)2016
# Feel free to look through the code, try to understand it & modify as you wish!
# The installer MUST be run before this code.

#!/usr/bin/python
import subprocess
import signal
import sys
import time
from sense_hat import SenseHat
import os
import alsaaudio
import wave
import numpy
import copy
import random
from evdev import InputDevice, list_devices, ecodes

#import alexa_helper # Import the web functions of Alexa, held in a separate program in this directory

sense = SenseHat() # Initialise the SenseHAT
sense.clear()  # Blank the LED matrix

# Search for the SenseHAT joystick
found = False
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True 
        break

# Exit if SenseHAT not found
if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()

# Initialise audio buffer
audio = ""
inp = None

# We're British and we spell "colour" correctly :) Colour code for RAINBOWZ!!
colours = [[255, 0, 0], [255, 0, 0], [255, 105, 0], [255, 223, 0], [170, 255, 0], [52, 255, 0], [0, 255, 66], [0, 255, 183]]

# Loudness for highest bar of RGB display
max_loud = 1024



'''
# When button is released, audio recording finishes and sent to Amazon's Alexa service
def release_button():
    global audio, inp
    sense.set_pixels([[0,0,0]]*64)
    w = wave.open(path+'recording.wav', 'w') # This and following lines saves voice to .wav file
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(16000)
    w.writeframes(audio)
    w.close()
    sense.show_letter("?") # Convert to question mark on display
    alexa_helper.alexa(sense) # Call upon alexa_helper program (in this directory)
    sense.clear() # Clear display
    inp = None
    audio = ""
    '''

'''
# When button is pressed, start recording
def press_button():
    global audio, inp
    try:
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, alexa_helper.device)
    except alsaaudio.ALSAAudioError:
        print('Audio device not found - is your microphone connected? Please rerun program')
        sys.exit()
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)
    audio = ""
    l, data = inp.read()
    if l:
        audio += data
        '''
'''
# Whilst button is being pressed, continue recording and set "loudness"
def continue_pressed():
    global audio, inp
    l, data = inp.read()
    if l:
        audio += data
        a = numpy.fromstring(data, dtype='int16') # Converts audio data to a list of integers
        loudness = int(numpy.abs(a).mean()) # Loudness is mean of amplitude of sound wave - average "loudness"
        set_display(loudness) # Set the display to show this "loudness"
'''

def count_down(n):
	for i in range(n, 0, -1):
		if i<10:
			sense.show_letter(str(i),text_colour=[255, 0, 0])
		else:
			sense.show_message(str(i),text_colour=[255, 0, 0],scroll_speed=0.05)
		time.sleep(1)

class MathExercice:
    	
    def __init__(self,level):
        self.level = level
        
    def read_word(self,statement):
        os.system('pico2wave -l fr-FR -w temp.wav "' + statement + '" && aplay temp.wav')
        sense.show_message(statement,scroll_speed=0.05)

    def main(self,n):
        for i in range(0, n):
            a = random.randint(0,20*self.level)
            b = random.randint(0,20*self.level)
            statement = str(a) + ' + ' + str(b) + ' = ?'
            self.read_word(statement)
            count_down(5)
            statement = str(a) + ' + ' + str(b) + ' = ' + str(a+b)
            self.read_word(statement)

class Spelling:

    words_fr = ["chauffage", "belle", "encore", "dessin", "ballon", "balle", "dix", "arbre", "avant", "avion", "brebis"]
    words_i = 0
    	
    def __init__(self,language):
        self.language = language
        
    def read_word(self):
        word = self.words_fr[self.words_i]
        os.system('pico2wave -l fr-FR -w temp.wav "' + word + '" && aplay temp.wav')

    def spell_word(self):
        word = self.words_fr[self.words_i]
        for i in range(0, len(word)):
            sense.show_letter(word[i],text_colour=[255, 0, 0])
            os.system('pico2wave -l fr-FR -w temp.wav "' + word[i] + '" && aplay temp.wav')
            time.sleep(1)
    
    def display_word(self):
        word = self.words_fr[self.words_i]
        for i in range(0, len(word)):
            sense.show_letter(word[i],text_colour=[255, 0, 0])
            time.sleep(1)

    def main(self,n):
        for i in range(0, n):
            self.words_i = random.randint(0,len(self.words_fr)-1)
            self.read_word()
            self.read_word()
            count_down(20)
            self.read_word()
            self.spell_word()

            
# initiate Spelling tool
spell = Spelling("FR")
math_exercice = MathExercice(1)


# menu letters
menu_letters = ['a','m','s','r']
menu_messages_EN = ["Alexa", "Math", "Spelling", "Recorder"]
menu_messages_FR = ["Alexa", "Math", "Dictee", "Enregistrement"]
menu_i = 0
global language
global menu_messages

def set_language(l):
    global language
    global menu_messages
    language = l
    if l == "FR":
        menu_messages = menu_messages_FR
    elif l == "EN":
        menu_messages = menu_messages_EN

# Event handler for button
def handle_enter():
    sense.show_message(menu_messages[menu_i],scroll_speed=0.2)	
    if menu_i == 0:
        os.system("python /home/pi/Artificial-Intelligence-Pi/main.py")
    elif menu_i == 1:
        math_exercice.main(2)
    elif menu_i == 2:
        spell.main(2)
    elif menu_i == 3:
        os.system("python voice_game.py") 
    menu_update("off")
        
def set_menu_i(delta):
    global menu_i
    menu_i += delta
    if menu_i==-1:
        menu_i = 0
    if menu_i>len(menu_letters)-1:
        menu_i = len(menu_letters)-1
    menu_update("off")


def menu_update(status):
    if status == "on":
        c = [255, 0, 0]
    elif status == "off":
        c = [200, 200, 200] 
    sense.show_letter(menu_letters[menu_i], text_colour=c)
    if language == "FR":
        os.system('pico2wave -l fr-FR -w temp.wav "' + menu_messages[menu_i] + '" && aplay temp.wav')
    elif language == "EN":
        os.system('pico2wave -w temp.wav "' + menu_messages[menu_i] + '" && aplay temp.wav') 

# Continually loops for events, if event detected and is the middle joystick button, call upon event handler above
def event_loop():
    try:
        for event in dev.read_loop(): # for each event
            print(event.value)
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_ENTER and event.value == 1: # if event is a key and is the enter key (middle joystick)
                menu_update("on")
                handle_enter()
                #handle_enter(event.value) # handle event
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_UP: # if event is a key and is the enter key (middle joystick)
                print "Key UP"
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_RIGHT and event.value == 1: # if event is a key and is the enter key (middle joystick)
                print "Key Right"
                set_menu_i(1)
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_LEFT and event.value == 1: # if event is a key and is the enter key (middle joystick)
                print "Key Left"
                set_menu_i(-1)
            if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_DOWN: # if event is a key and is the enter key (middle joystick)
                print "Key Down"
                raise KeyboardInterrupt
					
    except KeyboardInterrupt: # If Ctrl+C pressed, pass back to main body - which then finishes and alerts the user the program has ended
        pass

# Run when program is called (won't run if you decide to import this program)
set_language("FR")
menu_update("off")
event_loop()
print "\nYou have exited Alexa. I hope that I was useful. To talk to me again just type: python main.py"
