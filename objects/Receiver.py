from objects.Decoder import Decoder
from objects.Signal import Signal
class Receiver:
    def __init__(self):
        pass

    def receiveFrames(self,tableOfFrames):
        self.tableOfFrames = tableOfFrames

    def executeDecoder(self):
        decoder = Decoder()
        for i in range(len(self.tableOfFrames)):
            decoder.executeFrameDecoding(self.tableOfFrames[i].frame)
