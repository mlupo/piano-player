#!/usr/bin/python3
"""
Attach to a MIDI device and send the contents of a MIDI file to it.
"""
from __future__ import division
import sys
import time
import midi
import midi.sequencer as sequencer
# Import the PCA9685 module.
import Adafruit_PCA9685

#if len(sys.argv) != 3:
#    print("Usage: {0} <client> <port>".format(sys.argv[0]))
#    exit(2)

#client = sys.argv[1]
#port   = sys.argv[2]

client = 20
port = 0

hardware = sequencer.SequencerHardware()

if not client.isdigit:
    client = hardware.get_client(client)

if not port.isdigit:
    port = hardware.get_port(port)

seq = sequencer.SequencerRead(sequencer_resolution=120)
seq.subscribe_port(client, port)

seq.start_sequencer()

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 155  # Min pulse length out of 4096

servo_max = 600  # Max pulse length out of 4096
servo_press = 278

ON = servo_max
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

NOTE_DICT = {C5:0, D5:1, E5:2, F5:3, G5:4, A5:5, B5:6,
             C6:7, D6:8, E6:9, F6:10, G6:11, A6:12, B6:13}

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def noteCheck(data, signal, channel=0):
    """take the data attributes of the midi event, and assign it
    to the appropiate values to work with the servos. If the data is not
    in the dictionary of notes, pass it along"""
    if data in NOTE_DICT.keys():
        data = NOTE_DICT.get(data)
        if signal == 0:
            signal = OFF
        elif signal != 0:
            signal = ON
        pwm.set_pwm(data, channel, signal)
    else:
        note_key = data
        signal = signal
        return data, signal


def notePlay(midi_event):
    if midi_event is not None:
        print(noteCheck(midi_event.data[0], midi_event.data[1]))

while True:
    event = seq.event_read()
    noteCheck(event)





