#!/usr/bin/python3
"""
Attach to a MIDI device and send the contents of a MIDI file to it.
"""
import sys
import time
import midi
import midi.sequencer as sequencer

if len(sys.argv) != 3:
    print("Usage: {0} <client> <port>".format(sys.argv[0]))
    exit(2)

client = sys.argv[1]
port   = sys.argv[2]

hardware = sequencer.SequencerHardware()

if not client.isdigit:
    client = hardware.get_client(client)

if not port.isdigit:
    port = hardware.get_port(port)

seq = sequencer.SequencerRead(sequencer_resolution=120)
seq.subscribe_port(client, port)

seq.start_sequencer()

NOTE_DICT = {72:"servo_1", 74:"servo_2", 76:"servo_3"}
ON = 1
OFF = 0

def noteCheck(data, signal):
    """take the data attributes of the midi event, and assign it
    to the appropiate values to work with the servos. If the data is not
    in the dictionary of notes, pass it along"""
    if data in NOTE_DICT.keys():
        data = NOTE_DICT.get(data)
        if signal == 0:
            signal = OFF
        elif signal != 0:
            signal = ON
    else:
        note_key = data
        signal = signal
    return data, signal


def notePlay(midi_event):
    if midi_event is not None:
        print(noteCheck(midi_event.data[0], midi_event.data[1]))

while True:
    event = seq.event_read()
    if event is not None:
        notePlay(event)





