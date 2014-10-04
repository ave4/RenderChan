

__author__ = 'Konstantin Dmitriev'

from renderchan.module import RenderChanModule
from renderchan.utils import which
import subprocess
import os
import re
import random

class RenderChanPencil2dModule(RenderChanModule):
    def __init__(self):
        RenderChanModule.__init__(self)
        self.conf['binary']="pencil2d"
        self.conf["packetSize"]=0

    def getInputFormats(self):
        return ["pcl"]

    def getOutputFormats(self):
        return ["png"]

    def checkRequirements(self):
        for key in ['binary']:
            if which(self.conf[key]) == None:
                self.active=False
                print "Module warning (%s): Cannot find '%s' executable." % (self.getName(), self.conf[key])
                print "    Please install pencil2d package."
                return False
        self.active=True
        return True

    def render(self, filename, outputPath, startFrame, endFrame, format, updateCompletion, extraParams={}):

        comp = 0.0
        updateCompletion(comp)

        output = os.path.join(outputPath,"file")
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        commandline=[self.conf['binary'], filename, "--export-sequence", output]
        subprocess.check_call(commandline)

        updateCompletion(1.0)