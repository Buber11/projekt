import random


class FileManager:
    def __init__(self):
        pass

    def saveSimulationData(self, reciever, frameLength, model, probability, code, arqMode):
        with open("testy7.txt", "a") as file:
            file.write(";model;")
            if model.type == 1:
                file.write("bsc")
            if model.type == 2:
                file.write("gillberta-elliota")

            file.write(";frameLength;")
            file.write(str(frameLength))

            file.write(";number of frames;")
            file.write(str(len(reciever.originalSignal)))

            file.write(";prob1;")
            file.write(str(probability[0]))

            if probability[1] != 0.0:
                file.write(";prob2;")
                file.write(str(probability[1]))
                file.write(";\n")
                file.write(";timeInGood;")
                file.write(str(model.timeInGoodState))

            file.write(";code;")
            if code == "01":
                file.write("crc8")
            if code == "10":
                file.write("crc16")
            if code == "11":
                file.write("bit parzystosci")

            file.write(";arqMode;")
            if arqMode == 1:
                file.write("Stop and Wait")
            if arqMode == 2:
                file.write("Selective Repeat")
            file.write(";\n")

            file.write(";falseAcceptance;")
            file.write(str(reciever.falseAcceptance))

            numberOfErrors = 0
            file.write(";errors;")
            for x in range(len(reciever.errors)):
                if reciever.errors[x] > 0:
                    numberOfErrors += 1
                file.write(str(reciever.errors[x]))
                file.write(";")
            file.write("\n")

            file.write(";numberOfErrors;")
            file.write(str(numberOfErrors))

            if arqMode == 2:
                file.write(";SRframes;")
                file.write(str(reciever.indexesAcceptedByRecieverCounter))
                file.write(";")

            file.write("\n\n")

    def saveAvgData(self, frameNumber, frameLength, model, probability, code, arqMode,avg):
        with open("testyAVG.txt", "a") as file:
            file.write(";")
            if model.type == 1:
                file.write("BSC ")
            if model.type == 2:
                file.write("G-E ")

            file.write(str(frameLength))

            file.write(" ")
            file.write(str(probability[0]))

            file.write(" ")
            if code == "01":
                file.write("CRC8")
            if code == "10":
                file.write("CRC16")
            if code == "11":
                file.write("BP")

            file.write(" ")
            if arqMode == 1:
                file.write("SW")
            if arqMode == 2:
                file.write("SR")

            file.write(";")
            file.write(str(round(avg,2)))
            file.write(";")
            file.write("\n")