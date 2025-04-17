import os
import subprocess
import threading as th
import time
from infoWrap import Info
from sysCheck import System, BtLowEnergy, Gpio, VisumServer, Kinect


class KinectMonitor:
    def __init__(self):
        self.kinect = None
        self.stop_flag = False
        self.usbTrip = False
        self.monitor = th.Thread(target=self.monitorKinect)

    def monitorKinect(self):
        sysCheck = Kinect()
        sysCheck.setModal("True")
        while not self.stop_flag:
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
                        sysCheck.setModal("True")

                    else:
                        self.usbTrip = True
                        Info.error("[ERROR]", "XBOX Kinect Read Buffer Failure! Check Connection")
                        sysCheck.setModal("False")
            else:
                if not self.usbTrip:
                    self.usbTrip = True
                    sysCheck.setModal("False")
                    Info.error("ERR", "Unable to detect XBOX Kinect Module! Retrying...")
                    Info.info("I","Re-Flashing Kinect Firmware")
                    os.system("timeout 5 freenect-micview")

                    

    def stop(self):
        self.stop_flag = True
        self.monitor.join()
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
