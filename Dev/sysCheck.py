import os
import time
from typing_extensions import override
import psutil


class System:
    def __init__(self):
        self.btlowenergy = False
        self.gpio = False
        self.VisumServer  = False
        self.kinect = False

    def setModal(self, stat):
        self.global_sys = "GlobalSys"
        self.writeFile = open(f"~/.sysCheck{self.global_sys}.log", "w")
        self.writeFile.write(f"{stat}")
        self.writeFile.flush()


class BtLowEnergy(System):
    @override
    def setModal(self, stat):
        self.globalSys = "BtLowEnergy"
        super().setModal(stat)
        self.btlowenergy = True

class Gpio(System):
    @override
    def setModal(self, stat):
        self.globalSys = "GPIO"
        super().setModal(stat)
        self.gpio = True

class VisumServer(System):
    @override
    def setModal(self, stat):
        self.globalSys = "VisumServer"
        super().setModal(stat)
        self.VisumServer = True

class Kinect(System):
    @override
    def setModal(self, stat):
        self.globalSys = "Kinect"
        super().setModal(stat)
        self.kinect = True
