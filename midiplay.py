#!/usr/bin/python3
"""This is the program which controlled the Organ Player for my thesis project.

Using the servo library from adafruit, and a midi library by Christopher Arndt
(https://github.com/SpotlightKid/micropython-stm-lib). The midi commands are
parsed, and a corresponding servo is activated depending on the data supplied.

This version runs on a micropython device, using this lib from adafruit:
https://learn.adafruit.com/micropython-hardware-pca9685-pwm-and-servo-driver
"""

import machine
from midi.midiin import MidiIn
import pyb
import servo

# Configure min and max servo pulse length
servo_min = 140  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

ON = 310  # pulse length which will rotate the servo for a full key press
ON_LOW = 270
OFF = servo_min

# these midi codes are all/most of the possible "all note off" commands
MIDI_OFF_COMMANDS = [176, 123, 125, 124, 121, 120]

# variables to hold the available MIDI note numbers
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

# each key corresponds to the servo number attached to the microcontroller
NOTE_DICT = {C4: 0, D4: 1, E4: 2, F4: 3, G4: 4, A4: 5, B4: 6,
             C5: 7, D5: 8, E5: 9, F5: 10, G5: 11, A5: 12, B5: 13,
             C6: 14, Eb4: 15}


def midi_reader(msg):
    """Take the data of the midi event, and pass it through various checks.

    The MIDI message is parsed as a set of values structed along the lines of:
    command, note, velocity. the 'msg' variable holds this data, is checked, and
    if a note has to be played or turned off, send data to the servos
    """
    note_servo = None
    signal = None
    if (msg[0] == 144) and (msg[1] in NOTE_DICT.keys()):
        # a note-on command!
        note_servo = NOTE_DICT.get(msg[1])
        if msg[2] > 0:
            # any note velocity triggers a key press
            signal = ON
        else:
            # sometimes a note with velocity of 0 is used to indicate a note off
            signal = OFF
    elif (msg[0] == 128) and (msg[1] in NOTE_DICT.keys()):
        # note off message
        note_servo = NOTE_DICT.get(msg[1])
        signal = OFF
    elif msg[0] in MIDI_OFF_COMMANDS:
        # any 'all notes off command is recieved'
        print("all notes off")
        print("status off", msg[0])
        for i in range(0, 16):
            midi_player(i, OFF)
            pyb.delay(10)
    else:
        print("status:", msg[0], "note:", msg[1], "velocity:", msg[2])
    # take the compiled message and pass it to the servo
    midi_player(note_servo, signal)


def midi_player(servo_key, duty_signal):
    """Pass the collected data to the servo."""
    if (servo_key is not None) and (duty_signal is not None):
        servos.position(servo_key, duty=duty_signal)
        print(servo_key, duty_signal)

uart = pyb.UART(1, 31250)
midiin = MidiIn(uart, callback=midi_reader)

# main program ###
i2c = machine.I2C(machine.Pin('B10'), machine.Pin('B3'))
servos = servo.Servos(i2c)

while True:
    midiin.poll()
    pyb.udelay(20)
