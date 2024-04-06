import argparse
import sys
import serial
import functools
from time import sleep
from random import randint

from .volkszaehler import get_values_from_stream
from .server import run

def _print_it(data):
    for key, value in data.items():
        print(key, "\t", value)

parser = argparse.ArgumentParser("SML volkszaehler")
parser.add_argument("device")
parser.add_argument("--mqtt-broker")
parser.add_argument("--interval")
args = parser.parse_args()

if args.device:
    s = serial.Serial(sys.argv[1])
    data = get_values_from_stream(s)

    to_call = _print_it
    if args.mqtt_broker:
        to_call = functools.partial(run, args.mqtt_broker)

    if args.interval:
        while True:
            to_call(data)
            sleep(int(args.interval))
    else:
        to_call(data)
