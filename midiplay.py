#!/usr/bin/python3

from __future__ import division
#import sys
#import time
import mido
import Adafruit_PCA9685

inport = mido.open_input('CH345 MIDI 1')

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
# pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 155  # Min pulse length out of 4096

servo_max = 600  # Max pulse length out of 4096
servo_press = 278

ON = servo_press
OFF = servo_min

C5 = 72
D5 = 74
E5 = 76
F5 = 77
G5 = 79
A5 = 81
B5 = 83
C6 = 84
D6 = 86
E6 = 88
F6 = 89
G6 = 91
A6 = 93
B6 = 95

NOTE_DICT = {C5: 0, D5: 1, E5: 2, F5: 3, G5: 4, A5: 5, B5: 6,
             C6: 7, D6: 8, E6: 9, F6: 10, G6: 11, A6: 12, B6: 13}

def noteCheck(in_message, pwm_channel=0):
    note_servo = None
    signal= None
    """take the data attributes of the midi event, and assign it
    to the appropiate values to work with the servos. If the data is not
    in the dictionary of notes, pass it along"""
    if in_message.type != 'control_change':
        if in_message.type == 'note_on':
            if in_message.note in NOTE_DICT.keys():
                note_servo = NOTE_DICT.get(in_message.note)
                if in_message.velocity > 0:
                    signal = ON
        elif in_message.type == 'note_off':
            if in_message.note in NOTE_DICT.keys():
                note_servo = NOTE_DICT.get(in_message.note)
                signal = OFF
    elif in_message.type == 'control_change':
        print("all notes off")
    else:
        return in_message

    if (note_servo is not None) and (signal is not None):
        pwm.set_pwm(note_servo, pwm_channel, signal)
        print(note_servo, signal)


while True:
    with inport as port:
        for message in port:
            noteCheck(message)

