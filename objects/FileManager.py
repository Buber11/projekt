import random


class FileManager:
    def __init__(self):
        pass

    # Poprawnie dziala (można ewentualnie wprowadzic zasade ze pierwsza jest 1)
    def generateToFile(self, filePath, dataLength):
        with open(filePath, 'w') as file:
            random.seed()
            for i in range(dataLength):
                number = random.randint(0, 1)
                file.write(str(number))

    def loadFromFile(self, filePath,frameLenth):
        tablesOfFrames = []
        with open(filePath) as file:
            while True:
                word = file.read(frameLenth)
                if not word:
                    break
                tablesOfFrames.append(word)
        return tablesOfFrames
