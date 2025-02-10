from numpy.lib.function_base import average
from translateKinect import Kinect
from infoWrap import Info
from kinectUSBMonitor import KinectMonitor
from colorama import Fore, Style
import numpy as np
import cv2
import time
import json
import threading

global version, zrncode
version = 1.0
zrncode = ('\n\n'+Fore.LIGHTBLUE_EX + '[ZRN-PRJCT-VISUM-ENGINE-1.X]' + Style.RESET_ALL)
global kinect
debug = True


def systemInit():
    global kinect
    Info.info("System","Initializing Systems...")
    Info.info("System","Initializing Kinect Monitor to background...")
    monitor = KinectMonitor()
    monitor.start()
    try:
        Info.info("","Testing Kinect Capabilities...")
        Info.info("","Initializing Kinect Globally...")
        kinect = Kinect()
        Info.info("","Getting Depth Data...")
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
        Info.info("","Systems Checked and Ready !")
    except Exception as e:
        monitor.stop()
        Info.error("Error",f"Initialization Failed ! Stopping Systems...\n  Traceback -> {e}")
        return 1

# def showImg(title, output):
#     if debug:
#         cv2.imshow(f"[debug] {title}", output)
#         # if cv2.waitKey(1) & 0xFF == ord('1'):
#         #     break

def showDebugInfo(data):
    if debug:
        Info.debug("",data)

def streamCentroidData():
    while True:
        depth_data = kinect.getDepth()
        filtered_depth, mask, depth_mm = kinect.processDepth(depth_data)
        centroid, avg_depth = kinect.calculateCentroidnDepth(mask, depth_mm)
        output_image = cv2.cvtColor(filtered_depth.astype(np.uint8), cv2.COLOR_GRAY2BGR)

        if centroid is not None and avg_depth is not None:
            min_depth  = 50
            max_depth = 100
            min_radius = 5
            max_radius = 50
            radius = int(np.interp(avg_depth, [min_depth, max_depth], [max_radius, min_radius]))
            cv2.circle(output_image, centroid, radius, (0,0,255), -1)

        try:
            data_entry = {
                            "timestamp": time.time(),  # Add a timestamp
                            "centroid": {"x": centroid[0], "y": centroid[1]},
                            "average_depth": avg_depth
                        }
            with open('centroid_data.json', 'w') as json_file:
                json_file.write(json.dumps(data_entry, indent=4) + "\n")
        except Exception as e:
            Info.error("",f"Error writing centroid data, Packet Loss: {e}")

        if debug:
            cv2.imshow('Inverted Filtered Depth w. Centroid', output_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        showDebugInfo(f"{centroid}, {avg_depth}")


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

    Info.info("","Calling Depth Translater")
    # streamCentroidData()
    cdThread = threading.Thread(target=streamCentroidData)
    cdThread.start()
    Info.info("","Depth data is being Translated and streamed to centroid_data.json file")
    while True:
        Info.command("", "")
        x = input("Waiting For Command >")
        if x == "thread.cd.stop":
            cdThread.stop()
        # if x.split(".")[0] == "thread":
        #     ifx.split(".")[1] == "stop"
