from translateKinect import Kinect
from infoWrap import Info
from kinectUSBMonitor import KinectMonitor
from colorama import Fore, Style
import time
global version, zrncode
version = 1.0
zrncode = ('\n\n'+Fore.LIGHTBLUE_EX + '[ZRN-PRJCT-VISUM-ENGINE-1.X]' + Style.RESET_ALL)

def systemInit():
    Info.info("System","Initializing Systems...")
    Info.info("System","Initializing Kinect Monitor to background...")
    monitor = KinectMonitor()
    monitor.start()
    try:
        Info.info("","Testing Kinect Capabilities...")
        Info.info("","Getting Depth Data...")
        kinect = Kinect()
        Info.info("","Depth Data Received !")
        Info.info("","Getting Video Data...")
        kinect.getVideo()
        Info.info("","Video Data Received !")
        # Display All Data
        Info.info("","Displaying All Data...")
        print(kinect.getDepth())
        print(kinect.getVideo())
        print(kinect.getVideoRGB())
        print(kinect.getVideoBGR())
        print(kinect.getVideoRGBA())
        print(kinect.getVideoBGRA())
        print(kinect.getVideoYUV())
        print(kinect.getVideoYUYV())
        Info.info("","All Data Displayed !")
    except Exception as e:
        monitor.stop()
        Info.error("Error",f"Initialization Failed ! Stopping Systems...\n  Traceback -> {e}")
        return 1


# def keyHandler():


if __name__ == "__main__":
    print(f"{zrncode} Project Visum - Detection and Recognition Engine v{version}\n\n")
    sysCheck = systemInit()
    if sysCheck == 1:
        Info.warning("System","Failed to Initialize Systems !, Retrying one more time...")
        time.sleep(1)
        sysCheck = systemInit()
        if sysCheck == 1:
            Info.error("System","Failed to Initialize Systems !, Exiting...")
    else :
        Info.info("System","Systems Initialized Successfully !")
        # keyHandler()
        while True:
            time.sleep(1)
