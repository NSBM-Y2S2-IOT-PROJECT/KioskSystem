import serial
import time
from sysCheck import System, BtLowEnergy, Gpio, VisumServer, Kinect
from infoWrap import Info
from pynput.keyboard import Key, Controller
import os

# Initialize keyboard controller
keyboard = Controller()

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
sysCheck = Gpio()

time.sleep(2)

info = Info()
# Track button states to prevent key spamming
last_b1_state = 1  # Initialize to released
last_b2_state = 1  # Initialize to released
no_user_counter = 0
time.sleep(5)

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
                    keyboard.press(Key.f5)
                    keyboard.release(Key.f5)
                    info.debug("Emulated keyboard press: F5")
                
                if b1 == 0 and b2 == 0:
                    info.debug("Both buttons pressed")
                    os.system("setsid sudo bash /home/zerone/KioskSystem/Dev/VSM_Serve/server_reset.sh")

                # Update button states
                last_b1_state = b1
                last_b2_state = b2
                
                info.debug(f"Distance: {distance:.2f} cm")
                if distance >= 50 and distance < 100 :
                    print("User Detected !")
                    no_user_counter = 0
                elif distance >= 150:
                    no_user_counter += 1
                
                if no_user_counter > 10:
                    os.system("xrandr --output VGA-1-1 --off")
                else:
                    os.system("xrandr --output VGA-1-1 --auto")

                # if distance >= 0:
                #     pass
                #     info.debug(f"Distance: {distance:.2f} cm")
                # else:
                #     pass
                #     info.debug("Distance: No Echo")
                info.debug("-" * 30)
            except Exception as e:
                info.debug(f"Parse error: {e}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
    sysCheck.setModal("False")
    ser.close()