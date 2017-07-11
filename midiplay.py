#!/usr/bin/python3
import pca9685
import servo
import machine
from midi.midiin import MidiIn

# Configure min and max servo pulse lengths
servo_min = 140  # Min pulse length out of 4096

servo_max = 600  # Max pulse length out of 4096
servo_press = 310
servo_low_press = 270

ON = servo_press
ON_LOW = servo_low_press
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
             C6:14, Eb4 : 15}

def midi_printer(msg):
    """take the data of the midi event, and assign it
    to the appropiate values to work with the servos. If the data is not
    in the dictionary of notes, pass it along"""
    note_servo = None
    signal= None
    #print(tuple(msg))
    if msg[0] == 144 or msg[0] == 128:
    # '123' is the 'all sound off' message. if reieved, we cut the noise
        if msg[0] == 144:
            if msg[1] in NOTE_DICT.keys():
                note_servo = NOTE_DICT.get(msg[1])
                if msg[2] > 0:
                # note velocity
                    if msg[1] <= 72:
                        signal = ON_LOW
                    else:
                        signal = ON
                elif msg[2] == 0:
                    # if there is a note_on with 0 velocity, turn it off
                    signal = OFF
        elif msg[0] == 128:
            if msg[1] in NOTE_DICT.keys():
                note_servo = NOTE_DICT.get(msg[1])
                signal = OFF
    elif msg[0] == 176:
        print("all notes off")
        print("status off", msg[0])
        for i in range(0, 13):
            servos.position(i, duty=OFF)
            pyb.delay(10)
    else:
        print("status", msg[0])

    if (note_servo is not None) and (signal is not None):
        servos.position(note_servo, duty=signal)
        print(note_servo, signal)

uart = pyb.UART(1, 31250)
midiin = MidiIn(uart, callback=midi_printer)
### main prog###

#while True:
#    data = midiin.poll()
#    pyb.udelay(50)

i2c = machine.I2C(machine.Pin('B10'), machine.Pin('B3'))
#i2c.init()
servos = servo.Servos(i2c)

while True:
    midiin.poll()
    pyb.udelay(20)

#i2c.deinit()


