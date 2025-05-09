import serial
import time
import struct
from dataclasses import dataclass

SERIAL_PORT = '/dev/cu.usbmodem21101'  # Right-side USB port

@dataclass
class Control:
    pot1: int
    pot2: int
    pot3: int
    button1: bool
    button2: bool
    switch1: bool

def read_control_struct(serial_port: str, baud_rate: int = 9600, timeout: float = 1.0):
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    time.sleep(2)  # Wait for Arduino to reset
    STRUCT_FORMAT = 'BBB???'
    STRUCT_SIZE = struct.calcsize(STRUCT_FORMAT)
    try:
        while True:
            data = ser.read(STRUCT_SIZE)
            if len(data) == STRUCT_SIZE:
                pot1, pot2, pot3, button1, button2, switch1 = struct.unpack(STRUCT_FORMAT, data)
                yield Control(pot1, pot2, pot3, button1, button2, switch1)
    finally:
        ser.close()

if __name__ == "__main__":
    try:
        for result in read_control_struct(SERIAL_PORT):
            print(result)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting gracefully.")