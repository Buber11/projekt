import random
from objects.Signal import Signal


class Chanel:
    def __init__(self, probability, type):
        # Zmienna uzywana do BSC i G-E służąca do określenia szansy wystąpienia błędu w BSC, a w G-E do określenia szansy pozostania w dobrym stanie
        self.errorProbability = float(probability[0])
        # Zmienna uzywana do G-E służąca do określenia szansy pozostania w stanie złym
        self.maintainErrorProbability = float(probability[1])
        self.type = type
        self.goodBSCState = bool(True);

    def simulateChannel(self, tableOfFrames):
        if self.type == 1:
            return self.BSCChannelSimulation(tableOfFrames)
        if self.type == 2:
            return self.GEChanelSimulation(tableOfFrames)

    def GEChanelSimulation(self, tableOfFrames):
        tableOfNewFrames = []
        elements = ["yes", "no"]  # elementy do losowania

        # Wagi losowania do pozostania w dobrym stanie
        weights = [self.errorProbability, 1 - self.errorProbability]

        # Wagi losowania do pozostania w złym stanie
        badWeights = [self.maintainErrorProbability, 1 - self.maintainErrorProbability]

        if not isinstance(tableOfFrames,list):
            frame = tableOfFrames.frame
            bitsOfFrame = [int(bit) for bit in frame]
            for i in range(len(frame)):
                if self.goodBSCState:
                    los = random.choices(elements, weights=weights)
                    if los[0] == "yes":  # dochodzi do zamiany bitów oraz zmianu stanu w zły
                        if bitsOfFrame[i] == 1:
                            bitsOfFrame[i] = 0
                        else:
                            bitsOfFrame[i] = 1
                        self.goodBSCState = bool(False)
                    if los[0] == "no":  # nie dochodzi do zamiany bitów i pozostaje w dobrym stanie
                        continue
                else:
                    los = random.choices(elements, weights=badWeights)
                    if los[0] == "yes":  # dochodzi do zamiany bitów i pozostaje w złym stanie
                        if bitsOfFrame[i] == 1:
                            bitsOfFrame[i] = 0
                        else:
                            bitsOfFrame[i] = 1

                        self.goodBSCState = bool(False)
                    if los[0] == "no":  # nie dochodzi do zamiany bitów i przechodzi w stan dobry
                        self.goodBSCState = bool(True)
                        continue

            bit_string = ''.join(str(b) for b in bitsOfFrame)
            tableOfFrames.frame = bit_string
            return tableOfFrames

        for signal in tableOfFrames:
            frame = signal.frame
            bitsOfFrame = [int(bit) for bit in frame]
            for i in range(len(frame)):
                if self.goodBSCState:
                    los = random.choices(elements, weights=weights)
                    if los[0] == "yes":  # dochodzi do zamiany bitów oraz zmianu stanu w zły
                        if bitsOfFrame[i] == 1:
                            bitsOfFrame[i] = 0
                        else:
                            bitsOfFrame[i] = 1
                        self.goodBSCState = bool(False)
                    if los[0] == "no":  # nie dochodzi do zamiany bitów i pozostaje w dobrym stanie
                        continue
                else:
                    los = random.choices(elements, weights=badWeights)
                    if los[0] == "yes":  # dochodzi do zamiany bitów i pozostaje w złym stanie
                        if bitsOfFrame[i] == 1:
                            bitsOfFrame[i] = 0
                        else:
                            bitsOfFrame[i] = 1

                        self.goodBSCState = bool(False)
                    if los[0] == "no":  # nie dochodzi do zamiany bitów i przechodzi w stan dobry
                        self.goodBSCState = bool(True)
                        continue

            bit_string = ''.join(str(b) for b in bitsOfFrame)
            signal.frame = bit_string
            tableOfNewFrames.append(signal)
        return tableOfNewFrames

    def BSCChannelSimulation(self, tableOfFrames):
        tableOfNewFrames = []
        elements = ["yes", "no"]  # elementy do losowania
        weights = [self.errorProbability, 1 - self.errorProbability]
        if not isinstance(tableOfFrames,list):
            frame = tableOfFrames.frame
            bitsOfFrame = [int(bit) for bit in frame]
            for i in range(len(frame)):
                los = random.choices(elements, weights=weights)
                if los[0] == "yes":  # dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] = 1
                if los[0] == "no":  # nie dochodzi do zamiany bitów
                    continue
            bit_string = ''.join(str(b) for b in bitsOfFrame)
            tableOfFrames.frame = bit_string
            return tableOfFrames


        for signal in tableOfFrames:
            frame = signal.frame
            bitsOfFrame = [int(bit) for bit in frame]
            for i in range(len(frame)):
                los = random.choices(elements, weights=weights)
                if los[0] == "yes":  # dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] = 1
                if los[0] == "no":  # nie dochodzi do zamiany bitów
                    continue
            bit_string = ''.join(str(b) for b in bitsOfFrame)
            signal.frame = bit_string
            tableOfNewFrames.append(signal)
        return tableOfNewFrames
