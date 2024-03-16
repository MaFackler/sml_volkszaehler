import sys
import serial

if len(sys.argv) == 2:
    s = serial.Serial(sys.argv[1])
else:
    print("Please provide tty device as argument")
