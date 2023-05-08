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

        # Tablice przechowujące dane o błędach

        self.senderError = []
        self.receiverError = []
        self.falseAcceptance = 0


    def executeDecoder(self):
        # arqMode = 1 -> Stop and Wait
        # arqMode = 2 -> Selective Repeat
        if self.arqMode == 1:
            self.executeStopAndWait()
        if self.arqMode == 2:
            self.executeSelectiveRepeat()

    def executeStopAndWait(self):
        decoder = Decoder()
        senderErrorCount = 0
        receiverErrorCount = 0
        for i in range(len(self.tableOfFrames)):
            if not decoder.executeFrameDecoding(self.tableOfFrames[i].frame):
                senderErrorCount += 1
                sender = Sender()
                while True:
                    newFrame = self.originalSignal[i]
                    newFrame = sender.prepareFrames(newFrame, self.code)
                    newFrame = self.model.simulateChannel(newFrame)
                    receiverErrorCount += 1
                    if decoder.executeFrameDecoding(newFrame.frame):
                        # Przypisanie prawidłowej ramki
                        self.tableOfFrames[i] = newFrame
                        break
            # Sprawdzenie czy potwierdzona ramka faktycznie powinna byc potwierdzona
            # print("Oryginalna wiadomosc   : ",self.originalSignal[i])
            # print("Zaakceptowana wiadomosc: ", self.tableOfFrames[i].data)
            if not self.tableOfFrames[i].data == self.originalSignal[i]:
                self.falseAcceptance += 1

            self.senderError.append(senderErrorCount)
            self.receiverError.append(receiverErrorCount)
            senderErrorCount = 0
            receiverErrorCount = 0
        # Pomocniczy print
        print("Ilosc przeklaman: ",self.falseAcceptance)
        print(self.senderError)
        print(self.receiverError)

    def executeSelectiveRepeat(self):
        decoder = Decoder()
        indexes = [0, 1, 2, 3]

        for x in self.tableOfFrames:
            print(x.frame)

        senderErrorCount = 0

        for x in range(len(self.tableOfFrames)):
            self.senderError.append(0)

        while len(indexes) != 0:
            i = 0  # start at the beginning of the list
            while i < len(indexes):
                print("len indexes: {0}, indexes: {1}, i: {2}".format(len(indexes), indexes, i))
                if decoder.executeFrameDecoding(self.tableOfFrames[indexes[i]].frame):
                    if not self.tableOfFrames[indexes[i]].data == self.originalSignal[i]:
                        self.falseAcceptance += 1
                    indexes.remove(indexes[i])
                    if len(indexes) == 0:
                        break
                    nextIndex = indexes[-1] + 1
                    if nextIndex < len(self.tableOfFrames):
                        indexes.append(nextIndex)
                    indexes.sort()
                else:
                    self.senderError[indexes[i]] += 1
                    sender = Sender()
                    newFrame = self.originalSignal[indexes[i]]
                    newFrame = sender.prepareFrames(newFrame, self.code)
                    newFrame = self.model.simulateChannel(newFrame)
                    self.tableOfFrames[indexes[i]] = newFrame

                # update the index variable if we didn't remove an element
                if i < len(indexes):
                    i += 1
                print(self.senderError)
        print(self.senderError)
