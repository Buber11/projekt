from objects.Signal import Signal
class Decoder:
    def __init__(self):
        pass

    def XORoperation(self,bitOfData, bitOfCRC):
        return bitOfData ^ bitOfCRC

    def executeCRC(self,frame,CRC):
        bitsOfData = [int(bit) for bit in frame]
        bitsOfCRC = [int(bit) for bit in CRC]
        for i in range(len(frame)):
            k = i;
            if bitsOfData[i] == 1 and i <= len(frame) - len(CRC):
                for j in range(len(CRC)):
                    bitsOfData[k] = self.XORoperation(bitsOfData[k], bitsOfCRC[j])
                    k += 1
        i = 0;
        for i in range(len(bitsOfData)):
            if bitsOfData[i] == 1:
                print("błedna ramka numer:" + i)
                break;

    def executeParityCheck(self,frame):
        bitsOfFrame = [int(bit) for bit in frame]
        counter = 0  # zmienna zliczająca ilość jedynek w danych
        for i in range(len(frame)):
            if bitsOfFrame[i] == 1:
                counter += 1
        if (counter % 2 == 0):
            bit_string = ''.join(str(b) for b in bitsOfFrame)
            if bitsOfFrame[len(bitsOfFrame)-1] == 1:
                print("błąd")
        else:
            bit_string = ''.join(str(b) for b in bitsOfFrame)
            if bitsOfFrame[len(bitsOfFrame)-1] == 0:
                print("błąd")
        return bit_string


    def executeFrameDecoding(self,frame):
        title = frame[:3] #pobieranie etykiety ramki w celu weryfikacji jakiego kodu użyć
        if title == "001":
            self.executeCRC(frame[3:],"10111111") #CRC8
        if title == "010":
            self.executeCRC(frame[3:],"1011111111111111") #CRC16
        if title == "111":
            self.executeParityCheck(frame[3:]) #parzystośc


