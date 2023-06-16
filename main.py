from objects.Sender import Sender
from objects.FileManager import FileManager
from objects.Receiver import Receiver
from objects.Chanel import Chanel
import numpy as np
import random

# tablica przechowująca sygnały, ktore nie przeszly przez kanał komunikacyjny ani nie zostaly zakodowane
originalSignal = []

# dlugosc ramek
frameLength = 0

# model kanału
model = ""
modelType = -1
probability = np.array([0.0, 0.0])
# kod detekcyjny
code = ""
# tryb działania ARQ
arqMode = ""

# zakodowana tablica ramek z informacjami
tablesOfFrames = []


def menu():
    while True:
        print("Menu: ")
        print("1. Ręczna symulacja")
        print("2. Testy")
        print("3. Testy średniej")
        print("0. Zakończ działanie programu")
        choice = int(input("Wybór: "))
        if choice == 1:
            numberOfFrames = int(input("Podaj ilość ramek: "))
            global originalSignal
            originalSignal = []
            global frameLength
            frameLength = int(input("Podaj długośc pojedyńczej ramki danych: "))

            for x in range(numberOfFrames):
                originalSignal.append(''.join(random.choice(['0', '1']) for _ in range(frameLength)))

            global model, probability, modelType
            modelType = int(input("Wybierz model kanału:\n 1. BSC \n 2. Gilberta-Elliota"))

            # Musiałem zrobić tablice z numpy bo inaczej nie chcialo dzialac xd
            if modelType == 1:
                probability[0] = input("Podaj prawdopodobieństwo wysątpienia błędu: ")
                model = Chanel(probability, modelType)
            if modelType == 2:
                probability[0] = input("Podaj prawdopodobieństwo wysątpienia błędu w dobrym stanie: ")
                probability[1] = input("Podaj prawdopodobieństwo wysątpienia błędu w złym stanie: ")
                model = Chanel(probability, modelType)
            print("Wybierz kod detekcyjny:")
            print("a. CRC8")
            print("b. CRC16")
            print("c. Kontrola parzystości")
            choice = input("Wybór: ")
            print("\n")
            global code
            if choice == "a":
                code = "01"
            if choice == "b":
                code = "10"
            if choice == "c":
                code = "11"
            global arqMode
            arqMode = int(input("Wybierz tryb działania ARQ:\n 1. Stop and Wait \n 2. Selective Repeat"))

            if code not in ("01", "10", "11"):
                print("Brak wybranego kodu detekcyjnego!")
                break

            sender = Sender()
            # Przygytowanie ramek przed przejściem przez kanał komunikacyjny
            global tablesOfFrames
            tablesOfFrames = sender.prepareFrames(originalSignal, code)

            if arqMode not in (1, 2):
                print("Brak wybranego trybu ARQ!")
                break

            # for i in range(len(tablesOfFrames)):
            #    print(i," przed kanalem ",tablesOfFrames[i].data)
            # print("dlugosc przed",len(tablesOfFrames[1].data))

            # tutaj ramki przechodzą przez kanał ale nie są odbierane jeszcze
            tablesOfFrames = model.simulateChannel(tablesOfFrames)

            # for i in range(len(tablesOfFrames)):
            #    print(i," poooo kanalem ",tablesOfFrames[i].data)
            # print("dlugosc pooo", len(tablesOfFrames[1].data))

            receiver = Receiver(tablesOfFrames, arqMode, model, code, originalSignal)

            # tutaj ramki są odbierane
            receiver.executeDecoder()

            # zapis danych do pliku
            fileManager = FileManager()

            fileManager.saveSimulationData(receiver, frameLength, model, probability, code, arqMode)
        if choice == 2:
            testFrameLength = [32, 64, 128]
            testFrameNumber = [100, 200]
            testCode = ["01", "10", "11"]
            testArqMode = [1, 2]
            testModelType = [1, 2]
            testProb = [0.001, 0.01, 0.02]
            testProb2 = [0.005, 0.05, 0.10]
            for modelType in range(len(testModelType)):
                for frameLength in range(len(testFrameLength)):
                    for prob in range(len(testProb)):
                        for arqMode in range(len(testArqMode)):
                            for frameNumber in range(len(testFrameNumber)):
                                for code in range(len(testCode)):
                                    originalSignal = []
                                    for x in range(testFrameNumber[frameNumber]):
                                        originalSignal.append(''.join(
                                            random.choice(['0', '1']) for _ in range(testFrameNumber[frameNumber])))
                                    probability = np.array([0.0, 0.0])
                                    if testModelType[modelType] == 1:
                                        probability[0] = testProb[prob]
                                        model = Chanel(probability, testModelType[modelType])
                                    else:
                                        probability[0] = testProb[prob]
                                        probability[1] = testProb2[prob]
                                        model = Chanel(probability, testModelType[modelType])
                                    arqModeT = testArqMode[arqMode]
                                    codeT = testCode[code]
                                    sender = Sender()
                                    tablesOfFrames = sender.prepareFrames(originalSignal, codeT)
                                    tablesOfFrames = model.simulateChannel(tablesOfFrames)
                                    receiver = Receiver(tablesOfFrames, arqModeT, model, codeT, originalSignal)
                                    receiver.executeDecoder()
                                    fileManager = FileManager()
                                    fileManager.saveSimulationData(receiver, testFrameLength[frameLength], model,
                                                                 probability, codeT, arqModeT)
        if choice == 3:
            testFrameLength = [32,64,128,256,512]
            testFrameNumber = [100]
            testCode = ["01", "10", "11"]
            testArqMode = [1]
            testModelType = [1]
            testProb = [0.05,0.07]
            testProb2 = [0.25,0.35]
            for code in range(len(testCode)):
                for frameLength in range(len(testFrameLength)):
                    for prob in range(len(testProb)):
                        for modelType in range(len(testModelType)):
                            for frameNumber in range(len(testFrameNumber)):
                                for arqMode in range(len(testArqMode)):
                                    originalSignal = []
                                    avg = 0
                                    for numberOfTests in range(5):
                                        for x in range(testFrameNumber[frameNumber]):
                                            originalSignal.append(''.join(
                                                random.choice(['0', '1']) for _ in range(testFrameNumber[frameNumber])))
                                        probability = np.array([0.0, 0.0])
                                        if testModelType[modelType] == 1:
                                            probability[0] = testProb[prob]
                                            model = Chanel(probability, testModelType[modelType])
                                        else:
                                            probability[0] = testProb[prob]
                                            probability[1] = testProb2[prob]
                                            model = Chanel(probability, testModelType[modelType])
                                        arqModeT = testArqMode[arqMode]
                                        codeT = testCode[code]
                                        sender = Sender()
                                        tablesOfFrames = sender.prepareFrames(originalSignal, codeT)
                                        tablesOfFrames = model.simulateChannel(tablesOfFrames)
                                        receiver = Receiver(tablesOfFrames, arqModeT, model, codeT, originalSignal)
                                        receiver.executeDecoder()
                                        avg += sum(receiver.errors)/len(receiver.errors)
                                    avg /= 5
                                    fileManager = FileManager()
                                    fileManager.saveAvgData(testFrameNumber[frameNumber], testFrameLength[frameLength], model,
                                                            probability, codeT, arqModeT,avg)
        if choice == 0:
            return False


menu()
