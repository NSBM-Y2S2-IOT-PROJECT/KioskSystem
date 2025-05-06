import serial
import time
from sysCheck import System, BtLowEnergy, Gpio, VisumServer, Kinect
from infoWrap import Info
from pynput.keyboard import Key, Controller

# Initialize keyboard controller
keyboard = Controller()

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
sysCheck = Gpio()

time.sleep(2)

info = Info()
# Track button states to prevent key spamming
last_b1_state = 1  # Initialize to released
last_b2_state = 1  # Initialize to released

try:
    sysCheck.setModal("True")
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                parts = line.split(',')
                b1 = int(parts[0].split(':')[1])
                b2 = int(parts[1].split(':')[1])
                distance = float(parts[2].split(':')[1])

                info.debug(f"Button 1: {'Pressed' if b1 == 0 else 'Released'}")
                info.debug(f"Button 2: {'Pressed' if b2 == 0 else 'Released'}")
                
                # Button 1 pressed (0 means pressed)
                if b1 == 0 and last_b1_state == 1:
                    keyboard.press('s')
                    keyboard.release('s')
                    info.debug("Emulated keyboard press: S")
                
                # Button 2 pressed
                if b2 == 0 and last_b2_state == 1:
                    keyboard.press('b')
                    keyboard.release('b')
                    info.debug("Emulated keyboard press: B")
                
                # Update button states
                last_b1_state = b1
                last_b2_state = b2
                
                if distance >= 0:
                    pass
                    info.debug(f"Distance: {distance:.2f} cm")
                else:
                    pass
                    info.debug("Distance: No Echo")
                info.debug("-" * 30)
            except Exception as e:
                info.debug(f"Parse error: {e}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
    sysCheck.setModal("False")
    ser.close()