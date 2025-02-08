import wrappers.python.freenect as freenect

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
