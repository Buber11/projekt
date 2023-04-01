from objects.Sender import Sender
from objects.FileManager import FileManager

#tablica przechowująca sygnały, ktore nie przeszly przez kanał komunikacyjny ani nie zostaly zakodowane
originalSignal = []

#model kanału
model = ""
#kod detekcyjny
code = ""
#tryb działania ARQ
arqMode = ""

#zakodowana tablica ramek z informacjami
tablesOfFrames = []

def simulationMenu():
    while True:
        print("Menu symulacji: ")
        print("1. Wybierz model kanału komunikacyjnego")
        print("2. Wybierz kod detekcyjny")
        print("3. Wybierz tryb działania ARQ")
        print("4. Przygotuj dane")
        print("5. Rozpocznij symulacje")
        print("0. Wroć do poprzedniego menu")
        choice = int(input("Wybór: "))
        if choice == 1:
            global model
            model = input("Wybierz model kanału:\n 1. BSC \n 2. Gilberta-Elliota")
        if choice == 2:
            print("Wybierz kod detekcyjny:")
            print("1. CRC8")
            print("2. CRC16")
            print("3. Kontrola parzystości")
            choice = int(input("Wybór: "))
            print("\n")
            global code
            if choice == 1:
                code = "01"
            if choice == 2:
                code = "10"
            if choice == 3:
                code = "11"
        if choice == 3:
            global arqMode
            arqMode = input("Wybierz tryb działania ARQ:\n 1. Stop and Wait \n 2. Selective Repeat")
        if choice == 4:
            sender = Sender()
            tablesOfFrames = sender.prepareFrames(originalSignal,code)
        if choice == 5:
            print("5")
        if choice == 0:
            return False
def menu():
    while True:
        print("Menu: ")
        print("1. Wygeneruj dane do pliku")
        print("2. Wczytaj dane z pliku")
        print("3. Wybierz parametry symulacji")
        print("0. Zakończ działanie programu")
        choice = int(input("Wybór: "))
        if choice == 1:
            filePath = input("Podaj ścieżkę do pliku: ")
            dataLength = int(input("Podaj dlugość danych: "))
            fileManager = FileManager()
            fileManager.generateToFile(filePath, dataLength)
        if choice == 2:
            filePath = input("Podaj ścieżkę do pliku: ")
            frameLenth = input("Podaj długość pojedynczej ramki danych")
            fileManager = FileManager()
            global originalSignal
            originalSignal = fileManager.loadFromFile(filePath,frameLenth)
            for i in originalSignal:
                print(i)
        if choice == 3:
            simulationMenu()
        if choice == 0:
            return False

menu()



"""
length = int(input("napisz ilosc bitów danych w każdej ramce:"))

receiver = Receiver(length)
receiver.createSignals("dane.txt", usedCode, "1", "Reszta")
"""
