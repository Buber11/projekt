import math

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

        self.errors = []
        self.falseAcceptance = 0

    def executeDecoder(self):
        if self.arqMode == 1:
            self.executeStopAndWait()
        if self.arqMode == 2:
            self.executeSelectiveRepeat()

    def executeStopAndWait(self):
        decoder = Decoder()
        errorCount = 0
        for i in range(len(self.tableOfFrames)):
            if not decoder.executeFrameDecoding(self.tableOfFrames[i].frame):
                sender = Sender()
                while True:
                    newFrame = self.originalSignal[i]
                    newFrame = sender.prepareFrames(newFrame, self.code)
                    newFrame = self.model.simulateChannel(newFrame)
                    errorCount += 1
                    if decoder.executeFrameDecoding(newFrame.frame):
                        # Przypisanie prawidłowej ramki
                        self.tableOfFrames[i] = newFrame
                        break
            # Sprawdzenie czy potwierdzona ramka faktycznie powinna byc potwierdzona
            if self.tableOfFrames[i].data != self.originalSignal[i]:
                # print("Oryginalna wiadomosc   : ", self.originalSignal[i])
                # print("Zaakceptowana wiadomosc: ", self.tableOfFrames[i].data)
                self.falseAcceptance += 1

            self.errors.append(errorCount)
            errorCount = 0
        # Pomocniczy print
        print("Ilosc przeklaman: ", self.falseAcceptance)
        print(self.errors)

    def executeSelectiveRepeat(self):
        decoder = Decoder()

        # tabela indeksow w "sliding window"
        indexes = []
        indexesMaxSize = 4
        # tabela dzięki, której będzie można zauważyć czy jakiś indeks nie został zaakceptowany kilka razy
        indexesAcceptedByReciever = []
        indexesAcceptedByRecieverCounter = 0
        # tabela czasów
        frameTime = []
        maxTime = 20
        # tabela stanów ramek,  -1 = niewysłania, 0  = wysłana ale nie potwierdzona (rośnie frameTime w każdej iteracji), 1 = wysłana i potwierdzona
        frameStatus = []
        # licznik ile ramek juz jest potwierdzonych
        acceptedFrames = 0

        # inicjalizacja początkowych wartosci w tabelach
        for x in range(len(self.tableOfFrames)):
            self.errors.append(0)
            indexesAcceptedByReciever.append(0)
            frameTime.append(-1)
            frameStatus.append(-1)

        #TODO
        # Jak to powinno wyglądać
        # tabela czasów deafultowo ma -1 na jakims indeksie ktory nie byl wyslany
        # 0.9 trzeba moze jakos sprawdzic, ktora ramka czeka najdluzej, chociaz nie wiem czy jest sens bo jak
        # wysylamy 3 i 1 przyjdzie ok to w tym samym momencie za x iteracji bedzie trzeba te 2 wyslac
        # 1. Nadajnik sprawdza czy jakaś ramka nie czeka już na potwierdzenie za długo, jeśli tak to dodaje ją do indexes i zmienia czas na 0
        # 1.1 Dodaje kolejne indexy do indexes jeżeli nie przekroczy to długości
        # 2. Nadajnik wysyla ramki
        # 3. przy odbieraniu zakłócamy indeksy po sprawdzeniu poprawności
        # 4. jeżeli jest git, (jesli nie git to 5) to wysyłamy potwierdzenie o danym indeksie zakłóconym,
        # które też może sie znowu zakłócić i dodajemy ten pojedynczo zaklocony do tabeli indexesAcceptedByReciever
        # nadajnik otrzymuje potwierdzenia i jesli przyjdzie potwierdzenie nie wyslanej ramki to to ignoruje, jesli przyjdzie dobrej to usuwa z indexes
        # aktualizacja wszystkich czasów wysłanych a nie potwierdzonych
        # 5. wysyla indeks ramki ktora nie zostala zaakceptowana, ta wiadomosc moze byc tez zaklocona
        # 6. odbiornik przyjmuje zaklocona wiadomosc ktora jest bledna to ja ignoruje, jesli przyjdzie dobra to index pozostaje w indexes
        # aktualizacja wszystkich czasów wysłanych a nie potwierdzonych

        while acceptedFrames != len(self.tableOfFrames):
            # 1
            for x in range(len(self.tableOfFrames)):
                if frameTime[x] >= maxTime:
                    indexes.append(x)
                    frameTime[x] = 0
                if len(indexes) == indexesMaxSize:
                    break
            # 1.1
            if len(indexes) < 4:
                for x in range(len(self.tableOfFrames)):
                    if frameStatus[x] == -1:
                        indexes.append(x)
                        frameTime[x] = 0
                        frameStatus[x] = 0
                    if len(indexes) == indexesMaxSize:
                        break
            # tabele do przechowywania informacji o dobrych i złych ramkach
            acceptedIndexes = []
            rejectedIndexes = []
            # 2
            for x in range(len(indexes)):
                if decoder.executeFrameDecoding(self.tableOfFrames[indexes[x]].frame):
                    if not self.tableOfFrames[indexes[x]].data == self.originalSignal[indexes[x]]:
                        self.falseAcceptance += 1
                    binaryIndex = str(format(indexes[x],'09b'))
                    # 3
                    binaryIndexAfterChannel = self.model.simulateChannel(binaryIndex)
                    # 4
                    if int(binaryIndexAfterChannel,2) < len(self.tableOfFrames):
                        indexesAcceptedByReciever[int(binaryIndexAfterChannel,2)] = 1

                    acceptedIndexes.append(int(binaryIndexAfterChannel,2))
                else:
                    self.errors[indexes[x]] += 1
                    sender = Sender()
                    newFrame = self.originalSignal[indexes[x]]
                    newFrame = sender.prepareFrames(newFrame,self.code)
                    newFrame = self.model.simulateChannel(newFrame)
                    self.tableOfFrames[indexes[x]] = newFrame
                    # 5
                    binaryIndex = str(format(indexes[x],'09b'))
                    binaryIndexAfterChannel = self.model.simulateChannel(binaryIndex)
                    rejectedIndexes.append(int(binaryIndexAfterChannel,2))
            # zakłócenie tabeli potwierdzeń i odrzuceń w drodze do nadajnika z odbiornika jako wiadomości zwrotne
            for x in range(len(acceptedIndexes)):
                binaryIndex = str(format(acceptedIndexes[x], '09b'))
                binaryIndexAfterChannel = self.model.simulateChannel(binaryIndex)
                acceptedIndexes[x] = int(binaryIndexAfterChannel,2)
            for x in range(len(rejectedIndexes)):
                binaryIndex = str(format(rejectedIndexes[x], '09b'))
                binaryIndexAfterChannel = self.model.simulateChannel(binaryIndex)
                rejectedIndexes[x] = int(binaryIndexAfterChannel,2)
            # 6 przyjęcie ramek

            indexes = []

            for x in range(len(acceptedIndexes)):
                if acceptedIndexes[x] <= len(self.tableOfFrames):
                    if frameStatus[acceptedIndexes[x]] == 0:
                        frameStatus[acceptedIndexes[x]] = 1
                        acceptedFrames += 1

            for x in range(len(rejectedIndexes)):
                if rejectedIndexes[x] <= len(self.tableOfFrames):
                    if frameStatus[rejectedIndexes[x]] == 0:
                        indexes.append(rejectedIndexes[x])
                        frameTime[rejectedIndexes[x]] = 0
            # aktualizacja czasów wysłanych a niepotwierdzonych ramek
            for x in range(len(self.tableOfFrames)):
                if frameStatus[x] == 0:
                    frameTime[x] += 1

        for x in range(len(indexesAcceptedByReciever)):
            if indexesAcceptedByReciever[x] == 1:
                indexesAcceptedByRecieverCounter += 1

        print("Accepted frames: ",acceptedFrames)
        print("indexes accepted counter: ",indexesAcceptedByRecieverCounter)
        print(self.errors)
