import wrappers.python.freenect as freenect
import numpy as np
# Kinect Class

class Kinect:
    def __init__(self):
        self.kinect = freenect.sync_get_depth()[0]
        self.kinect = freenect.sync_get_video()[0]
        self.kinect = freenect.sync_get_video()[0]

    def getDepth(self):
        return freenect.sync_get_depth()[0]

    def getVideo(self):
        return freenect.sync_get_video()[0]

    def getVideoRGB(self):
        return freenect.sync_get_video()[0]

    def getVideoBGR(self):
        return freenect.sync_get_video()[0]

    def getVideoRGBA(self):
        return freenect.sync_get_video()[0]

    def getVideoBGRA(self):
        return freenect.sync_get_video()[0]

    def getVideoYUV(self):
        return freenect.sync_get_video()[0]

    def getVideoYUYV(self):
        return freenect.sync_get_video()[0]


    def processDepth(self, data):
        self.depth_mm = data * 0.124987
        mask = np.logical_and(self.depth_mm >= 10, self.depth_mm <= 100)
        output = np.zeros_like(self.depth_mm)
        output[mask] = 255
        return output, mask, self.depth_mm

    def calculateCentroidnDepth(self, mask, depth_mm):
        y_coords, x_coords = np.nonzero(mask)

        if len(x_coords) == 0 or len(y_coords) == 0:
            return  None, None

        centroid_x = int(np.mean(x_coords))
        centroid_y = int(np.mean(y_coords))
        avg_depth = np.mean(depth_mm[mask])

        return (centroid_x, centroid_y), avg_depth
