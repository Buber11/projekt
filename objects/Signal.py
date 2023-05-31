class Signal:
    def __init__(self,data,typeOfMessage,code,codeInformation):
        self.data = data
        self.typeOfMessage = typeOfMessage
        self.code = code
        self.codeInformation = codeInformation
        self.frame = typeOfMessage+code+data+codeInformation

    def __str__(self):
        return f" typeOfMessage={self.typeOfMessage}," \
               f" code={self.code},"\
               f" data={self.data}," \
               f" codeInformation={self.codeInformation})"

    def updateFrame(self):
        self.frame = self.typeOfMessage + self.code + self.data + self.codeInformation



