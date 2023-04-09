class Coder:
    def __init__(self):
        pass

    def XORoperation(self,bitOfData, bitOfCRC):
        return bitOfData ^ bitOfCRC
    def setCRC8(self,data):
        data += "00000000"
        return data
    def setCRC16(self,data):
        data += "0000000000000000"
        return data

    def getCodeInformationOFCRC(self,data,CRC):
        bitsOfData = [int(bit) for bit in data]
        bitsOfCRC = [int(bit) for bit in CRC]
        for i in range(len(data)):
            k = i;
            if bitsOfData[i] == 1 and i <= len(data) - len(CRC):
                for j in range(len(CRC)):
                    bitsOfData[k] = self.XORoperation(bitsOfData[k], bitsOfCRC[j])
                    k += 1
        bit_string = ''.join(str(b) for b in bitsOfData)
        return bit_string[-len(CRC):]

    def getCodeInformationParity(self,data):
        bitsOfData = [int(bit) for bit in data]
        counter = 0 #zmienna zliczająca ilość jedynek w danych
        for i in range(len(data)):
            if bitsOfData[i] == 1:
                counter += 1
        if(counter%2 == 0 ):
            return "0"
        else:
            return "1"

    def getCodeInformation(self, data,code):
        """
        TODO
        tutaj trzeba dodać zdobywanie tej reszty z dzielenia dla CRC lub 0/1 dla bitu parzystosci
        w parametrze frame masz dane z ktorych trzeba to wydobyc, w code masz info czy uzywasz crc czy bitu i trzeba do tego 3 ify zrobic i w kazdym return
        :param frame:
        :return:
        """
        if code == "01": #wykonaj operacje dzielenia CRC8
            data = self.setCRC8(data)
            codeInformation = self.getCodeInformationOFCRC(data,"10111111")
        if code == "10": #wykonaj operacje dzielenia CRC16
            data = self.setCRC16(data)
            codeInformation = self.getCodeInformationOFCRC(data,"1011111111111111")
        if code == "11": #wykonaj operacje zliczającą parzyste
            codeInformation = self.getCodeInformationParity(data)
        return codeInformation

