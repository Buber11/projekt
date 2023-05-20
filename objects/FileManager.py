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
                word = file.read(int(frameLenth))
                if not word:
                    break
                tablesOfFrames.append(word)
        return tablesOfFrames

    def saveSimulationData(self,reciever,frameLength,model,probability,code,arqMode):
        with open("testy18maj.txt","a") as file:
            file.write("\n")
            file.write(";model;")
            if model == 1:
                file.write("bsc")
            if model == 2:
                file.write("gillberta-elliota")
            file.write(";\n")

            file.write(";frameLength;")
            file.write(str(frameLength))
            file.write(";\n")

            file.write(";number of frames;")
            file.write(str(len(reciever.originalSignal)))
            file.write(";\n")

            file.write(";prob1;")
            file.write(str(probability[0]))
            file.write(";\n")

            if probability[1] != 0.0:
                file.write(";prob2;")
                file.write(str(probability[1]))
                file.write(";\n")

            file.write(";code;")
            if code == "01":
                file.write("crc8")
            if code == "10":
                file.write("crc16")
            if code == "11":
                file.write("bit parzystosci")
            file.write(";\n")

            file.write(";arqMode;")
            if arqMode == 1:
                file.write("Stop and Wait")
            if arqMode == 2:
                file.write("Selective Repeat")
            file.write(";\n")

            file.write(";falseAcceptance;")
            file.write(str(reciever.falseAcceptance))
            file.write(";\n")

            numberOfErrors = 0
            for x in range(len(reciever.senderError)):
                if reciever.senderError[x] > 0:
                    numberOfErrors += 1
            file.write(";numberOfErrors;")
            file.write(str(numberOfErrors))
            file.write(";\n")

            file.write(";senderError;")
            for x in range(len(reciever.senderError)):
                file.write(str(reciever.senderError[x]))
                file.write(";")
            file.write("\n")

            if arqMode == 1:
                file.write(";receiverError;")
                for x in range(len(reciever.receiverError)):
                    file.write(str(reciever.receiverError[x]))
                    file.write(";")
                file.write("\n")


