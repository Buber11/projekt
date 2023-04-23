from objects.Decoder import Decoder
from objects.Sender import Sender
from objects.Signal import Signal
from objects.Chanel import Chanel


class Receiver:
    def __init__(self, tableOfFrames, arqMode, model, code, originalSignal):
        self.tableOfFrames = tableOfFrames
        self.arqMode = arqMode

        # Zmienne potrzebne do przeslania sygnału ponownie gdyby ARQ wykryło błąd
        self.model = model
        self.code = code
        self.originalSignal = originalSignal

    def executeDecoder(self):
        # arqMode = 1 -> Stop and Wait
        # arqMode = 2 -> Selective Repeat
        if self.arqMode == 1:
            self.executeStopAndWait()
        if self.arqMode == 2:
            self.executeSelectiveRepeat()

    def executeStopAndWait(self):
        decoder = Decoder()
        for i in range(len(self.tableOfFrames)):
            if not decoder.executeFrameDecoding(self.tableOfFrames[i].frame):
                sender = Sender()
                while True:
                    newFrame = self.originalSignal[i]
                    newFrame = sender.prepareFrames(newFrame, self.code)
                    newFrame = self.model.simulateChannel(newFrame)
                    if decoder.executeFrameDecoding(newFrame):
                        break

    def executeSelectiveRepeat(self):
        decoder = Decoder()
        indexes = [0, 1, 2, 3]

        for x in self.tableOfFrames:
            print(x.frame)

        while len(indexes) != 0:
            i = 0  # start at the beginning of the list
            while i < len(indexes):
                print("len indexes: {0}, indexes: {1}, i: {2}".format(len(indexes), indexes, i))
                if decoder.executeFrameDecoding(self.tableOfFrames[indexes[i]].frame):
                    indexes.remove(indexes[i])
                    if len(indexes) == 0:
                        break
                    nextIndex = indexes[-1] + 1
                    if nextIndex < len(self.tableOfFrames) - 1:
                        indexes.append(nextIndex)
                    indexes.sort()

                else:
                    sender = Sender()
                    newFrame = self.originalSignal[indexes[i]]
                    print("newFrame 1: ", newFrame)
                    newFrame = sender.prepareFrames(newFrame, self.code)
                    print("newFrame 2: ", newFrame)
                    newFrame = self.model.simulateChannel(newFrame)
                    print("newFrame 3: ", newFrame)
                    self.tableOfFrames[indexes[i]] = newFrame

                # update the index variable if we didn't remove an element
                if i < len(indexes):
                    i += 1
