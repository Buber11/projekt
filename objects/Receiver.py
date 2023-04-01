from objects.Signal import Signal
class Receiver:
    def __init__(self,length):
        self.length = length

    def readFromFile(self, fileName):
        self.tableOfData = []
        with open(fileName) as file:
            while True:
                word = file.read(self.length)
                if not word:
                    break
                self.tableOfData.append(word)

    def createSignals(self,fileName,usedCode,typeOfMessage,restOfDivision):
        self.readFromFile(fileName)
        self.tableOfFrames = []
        for data in self.tableOfData:
            self.tableOfFrames.append(Signal(data,typeOfMessage,usedCode,restOfDivision))


