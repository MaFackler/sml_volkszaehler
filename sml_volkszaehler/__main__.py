import sys
import serial

from pprint import pprint
from .volkszaehler import get_values_from_stream

if len(sys.argv) == 2:
    s = serial.Serial(sys.argv[1])
    res = get_values_from_stream(s)
    for key, value in res.items():
        print(key, "\t", value)

else:
    print("Please provide tty device as argument")
