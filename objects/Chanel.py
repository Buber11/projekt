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
            signalLen = len(tableOfFrames.data)
            for i in range(len(frame)):
                if self.goodBSCState:
                    los = random.choices(elements,weights)
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
            newSignal = Signal(bit_string[3:signalLen+3],
                               bit_string[0:1],
                               bit_string[1:3],
                               bit_string[signalLen+2::])
            return newSignal

        for signal in tableOfFrames:
            frame = signal.frame
            bitsOfFrame = [int(bit) for bit in frame]
            signalLen = len(signal.data)
            # licznik do zliczania potrzebny do zmiany stanu
            counter = 0
            for i in range(len(frame)):
                if self.goodBSCState:
                    los = random.choices(elements, weights=weights)
                    if los[0] == "yes":  # dochodzi do zamiany bitów oraz zmianu stanu w zły
                        counter += 1
                        if bitsOfFrame[i] == 1:
                            bitsOfFrame[i] = 0
                        else:
                            bitsOfFrame[i] = 1
                        if counter == 5:
                            self.goodBSCState = bool(False)
                            counter = 0
                    if los[0] == "no":  # nie dochodzi do zamiany bitów i pozostaje w dobrym stanie
                        counter = 0
                        continue
                else:
                    los = random.choices(elements, weights=badWeights)
                    if los[0] == "yes":  # dochodzi do zamiany bitów i pozostaje w złym stanie
                        counter = 0
                        if bitsOfFrame[i] == 1:
                            bitsOfFrame[i] = 0
                        else:
                            bitsOfFrame[i] = 1

                        self.goodBSCState = bool(False)
                    if los[0] == "no":  # nie dochodzi do zamiany bitów i przechodzi w stan dobry
                        counter += 1
                        if counter == 5:
                            self.goodBSCState = bool(True)
                        continue

            bit_string = ''.join(str(b) for b in bitsOfFrame)
            newSignal = Signal(bit_string[3:signalLen+3],
                               bit_string[0:1],
                               bit_string[1:3],
                               bit_string[signalLen+2::])
            # print(m, "b", bit_string)
            # print(newSignal.__str__(newSignal))
            tableOfNewFrames.append(newSignal)
        return tableOfNewFrames

    def BSCChannelSimulation(self, tableOfFrames):
        tableOfNewFrames = []
        elements = ["yes", "no"]  # elementy do losowania
        weights = [self.errorProbability, 1 - self.errorProbability]
        #print(weights)
        if not isinstance(tableOfFrames,list):
            signalLen = len(tableOfFrames.data)
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
            newSignal = Signal(bit_string[3:signalLen+3],
                               bit_string[0:1],
                               bit_string[1:3],
                               bit_string[signalLen+2::])
            return newSignal

        for signal in tableOfFrames:
            signalLen = len(signal.data)
            frame = signal.frame
            # print(m, "a",frame)
            bitsOfFrame = [int(bit) for bit in frame]
            for i in range(len(frame)):
                los = random.choices(elements, weights=weights)
                # print("los", los)
                if los[0] == "yes":  # dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] = 1
                if los[0] == "no":  # nie dochodzi do zamiany bitów
                    continue
            bit_string = ''.join(str(b) for b in bitsOfFrame)
            newSignal = Signal(bit_string[3:signalLen+3],
                               bit_string[0:1],
                               bit_string[1:3],
                               bit_string[signalLen+2::])
            # print(m, "b", bit_string)
            # print(newSignal.__str__(newSignal))
            tableOfNewFrames.append(newSignal)
        return tableOfNewFrames
