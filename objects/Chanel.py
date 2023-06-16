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
        # zmienna dla G-E, dzieki niej mozna okreslic wspołczynnik pozostania w dobrym i złym stanie kanału
        self.timeInGoodState = 0

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

        if not isinstance(tableOfFrames,list) and not isinstance(tableOfFrames,Signal):
            dataLen = len(tableOfFrames)
            bitsOfFrame = [int(bit) for bit in tableOfFrames]
            counter = 0
            for i in range(dataLen):
                if self.goodBSCState:
                    los = random.choices(elements,weights)
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
                    los = random.choices(elements,badWeights)
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

            newData = ''.join(str(b) for b in bitsOfFrame)
            return newData


        if not isinstance(tableOfFrames,list):
            dataLen = len(tableOfFrames.data)
            bitsOfFrame = [int(bit) for bit in tableOfFrames.data]
            counter = 0
            for i in range(dataLen):
                if self.goodBSCState:
                    los = random.choices(elements,weights)
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
                    los = random.choices(elements,badWeights)
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

            newData = ''.join(str(b) for b in bitsOfFrame)
            tableOfFrames.data = newData
            tableOfFrames.updateFrame()
            return tableOfFrames

        counter = 0
        for signal in tableOfFrames:
            bitsOfFrame = [int(bit) for bit in signal.data]
            signalLen = len(signal.data)
            # licznik do zliczania potrzebny do zmiany stanu
            counter = 0
            for i in range(signalLen):
                if self.goodBSCState:
                    # print("Dobry stan")
                    self.goodBSCState += 1
                    los = random.choices(elements,weights)
                    # print("Los dobry: ",los)
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
                else:
                    # print("Zły stan")
                    los = random.choices(elements,badWeights)
                    # print("Los zły: ", los)
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
                # print("Counter: ",counter)
            newData = ''.join(str(b) for b in bitsOfFrame)
            signal.data = newData
            signal.updateFrame()
            tableOfNewFrames.append(signal)
        return tableOfNewFrames

    def BSCChannelSimulation(self, tableOfFrames):
        tableOfNewFrames = []
        elements = ["yes", "no"]  # elementy do losowania
        weights = [self.errorProbability, 1 - self.errorProbability]
        #print(weights)
        if not isinstance(tableOfFrames,Signal) and not isinstance(tableOfFrames,list):
            dataLen = len(tableOfFrames)
            bitsOfFrame = [int(bit) for bit in tableOfFrames]
            for i in range(dataLen):
                los = random.choices(elements,weights)
                if los[0] == "yes":  # dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] = 1
                if los[0] == "no":  # nie dochodzi do zamiany bitów
                    continue
            newData = ''.join(str(b) for b in bitsOfFrame)
            return newData

        if not isinstance(tableOfFrames,list):
            dataLen = len(tableOfFrames.data)
            bitsOfFrame = [int(bit) for bit in tableOfFrames.data]
            for i in range(dataLen):
                los = random.choices(elements,weights)
                if los[0] == "yes":  # dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] = 1
                if los[0] == "no":  # nie dochodzi do zamiany bitów
                    continue
            newData = ''.join(str(b) for b in bitsOfFrame)
            tableOfFrames.data = newData
            tableOfFrames.updateFrame()
            return tableOfFrames

        for signal in tableOfFrames:
            signalLen = len(signal.data)
            bitsOfFrame = [int(bit) for bit in signal.data]
            for i in range(signalLen):
                los = random.choices(elements,weights)
                # print("los", los)
                if los[0] == "yes":  # dochodzi do zamiany bitów
                    if bitsOfFrame[i] == 1:
                        bitsOfFrame[i] = 0
                    else:
                        bitsOfFrame[i] = 1
                if los[0] == "no":  # nie dochodzi do zamiany bitów
                    continue
            newData = ''.join(str(b) for b in bitsOfFrame)
            signal.data = newData
            signal.updateFrame()
            tableOfNewFrames.append(signal)
        return tableOfNewFrames
