#!/usr/bin/python3
"""This is an unused version of the Organ/Piano P;ayer Code, for a raspberry pi

Using the mido midi library (https://mido.readthedocs.io/en/latest/).
The midi commands are parsed, and a corresponding servo is activated depending
on the data supplied.

This version runs on a pi, using this kit from adafruit:
https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/
you'll also need a usb to midi converter for the pi
"""

import Adafruit_PCA9685
import mido

inport = mido.open_input('CH345 MIDI 1')

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 140  # Min pulse length out of 4096

servo_max = 600  # Max pulse length out of 4096
servo_press = 310
servo_low_press = 270

ON = servo_press
OFF = servo_min

C4 = 60
D4 = 62
Eb4 = 63
E4 = 64
F4 = 65
G4 = 67
A4 = 69
B4 = 71
C5 = 72
D5 = 74
E5 = 76
F5 = 77
G5 = 79
A5 = 81
B5 = 83
C6 = 84

NOTE_DICT = {C4: 0, D4: 1, E4: 2, F4: 3, G4: 4, A4: 5, B4: 6,
             C5: 7, D5: 8, E5: 9, F5: 10, G5: 11, A5: 12, B5: 13,
             C6: 14, Eb4: 15}


def noteCheck(in_message, pwm_channel=0):
    """Take the data attributes of the midi event, and assign it
    to the appropiate values to work with the servos. If the data is not
    in the dictionary of notes, pass it along."""
    note_servo = None
    signal = None
    if in_message.type == 'note_on':
        if in_message.note in NOTE_DICT.keys():
            note_servo = NOTE_DICT.get(in_message.note)
            if in_message.velocity > 0:
                signal = ON
    elif in_message.type == 'note_off' or in_message.velocity == 0:
        if in_message.note in NOTE_DICT.keys():
                note_servo = NOTE_DICT.get(in_message.note)
                signal = OFF
    elif in_message.type == 'control_change':
        print("all notes off")
        for i in range(0, 15):
            pwm.set_pwm(i, pwm_channel, OFF)
    else:
        return in_message

    if (note_servo is not None) and (signal is not None):
        pwm.set_pwm(note_servo, pwm_channel, signal)
        print(note_servo, signal)


while True:
    with inport as port:
        for message in port:
            noteCheck(message)
