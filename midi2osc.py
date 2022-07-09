#!/usr/bin/env python3

import sys
import time
import rtmidi
from rtmidi.midiutil import open_midiinput
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF, CONTROLLER_CHANGE

import liblo

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1", help="Sink host ")
parser.add_argument("--port", default="9001", help="Sink port")
parser.add_argument("--midi", default="0", help="midi number")
args = parser.parse_args()

def midiin_callback(event, data=None):
    message, deltatime = event

    if message[0] & 0xF0 == NOTE_ON or message[0] & 0xF0 == NOTE_OFF:
        status, note, velocity = message
        channel = (status & 0xF) + 1
        liblo.send(
            (args.host, args.port),
            f"/midi/{channel}/{'noteon' if message[0] & 0xF0 == NOTE_ON else 'noteoff'}",
            note,
            velocity
        )

    if message[0] & 0xF0 == CONTROLLER_CHANGE:
        status, cc, value = message
        channel = (status & 0xF) + 1
        liblo.send(
            (args.host, args.port),
            f"/midi/{channel}/cc",
            cc,
            value
        )



with open_midiinput(args.midi, client_name='noteon2osc')[0] as midiin:
    midiin.set_callback(midiin_callback)
    while True:
        time.sleep(1)