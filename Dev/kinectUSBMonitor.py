import os
import subprocess
import threading as th
import time
from infoWrap import Info

class KinectMonitor:
    def __init__(self):
        self.kinect = None
        self.stop_flag = False  # Flag to stop the thread
        self.usbTrip = False
        self.monitor = th.Thread(target=self.monitorKinect)

    def monitorKinect(self):
        while not self.stop_flag:  # Check the flag in the loop
            time.sleep(0.5)
            self.kinect = subprocess.Popen("lsusb | grep -i 'xbox nui camera'", shell=True, stdout=subprocess.PIPE)
            stdout, _ = self.kinect.communicate()

            if stdout != b"":
                if self.usbTrip:
                    self.usbTrip = False
                    Info.info("Success", f"XBOX Kinect is detected!")
                    Info.info("", "Trying to get information about the XBOX Kinect")
                    getData = subprocess.Popen("lsusb | grep -i 'xbox nui camera'", shell=True, stdout=subprocess.PIPE)
                    stdout2, _ = getData.communicate()
                    if stdout2.decode().strip():
                        Info.info("", f"{stdout2.decode().strip()}")
                    else:
                        self.usbTrip = True
                        Info.error("[ERROR]", "XBOX Kinect Read Buffer Failure! Check Connection")
            else:
                if not self.usbTrip:
                    self.usbTrip = True
                    Info.error("ERR", "Unable to detect XBOX Kinect Module! Retrying...")

    def stop(self):
        self.stop_flag = True  # Set the flag to stop the thread
        self.monitor.join()  # Wait for the thread to finish
        Info.warning("System", "Kinect Monitor Stopped!")

    def start(self):
        self.monitor.start()
        Info.info("System", "Kinect Monitor Initialized!")

if __name__ == "__main__":
    monitor = KinectMonitor()
    monitor.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
