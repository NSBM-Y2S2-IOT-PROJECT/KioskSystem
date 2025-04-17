import os
import time
from typing_extensions import override
import psutil


class System:
    def __init__(self):
        self.btlowenergy = False
        self.gpio = False
        self.VisumServer = False
        self.kinect = False
        self.global_sys = "GlobalSys"

    def setModal(self, stat):
        filepath = os.path.expanduser(f"~/.sysCheck{self.global_sys}.log")
        with open(filepath, "w") as writeFile:
            writeFile.write(f"{stat}")
            writeFile.flush()


class BtLowEnergy(System):
    def __init__(self):
        super().__init__()
        self.global_sys = "BtLowEnergy"
        
    @override
    def setModal(self, stat):
        super().setModal(stat)
        self.btlowenergy = True


class Gpio(System):
    def __init__(self):
        super().__init__()
        self.global_sys = "GPIO"
        
    @override
    def setModal(self, stat):
        super().setModal(stat)
        self.gpio = True


class VisumServer(System):
    def __init__(self):
        super().__init__()
        self.global_sys = "VisumServer"
        
    @override
    def setModal(self, stat):
        super().setModal(stat)
        self.VisumServer = True


class Kinect(System):
    def __init__(self):
        super().__init__()
        self.global_sys = "Kinect"
        
    @override
    def setModal(self, stat):
        super().setModal(stat)
        self.kinect = True
