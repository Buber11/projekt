import random
from objects.Signal import Signal
class Bsc:
    def __init__(self,probability):
        self.errorProbability = float(probability)

    def BSCChannelSimulation(self,tableOfFrames):
        tableOfNewFrames = []
        elements = ["yes","no"] #elementy do losowania
        weights = [self.errorProbability,1-self.errorProbability]
        for signal in tableOfFrames:
            frame = signal.frame
            bitsOfFrame = [int(bit) for bit in frame]
            for i in range(len(frame)):
                los = random.choices(elements, weights=weights)
                if los[0] == "yes": #dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] =1
                if los[0] == "no": #nie dochodzi do zamiany bitów
                    continue
            bit_string = ''.join(str(b) for b in bitsOfFrame)
            signal.frame = bit_string
            tableOfNewFrames.append(signal)
        return tableOfNewFrames
