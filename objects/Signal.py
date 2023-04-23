class Signal:
    def __init__(self,data,typeOfMessage,code,codeInformation):
        self.data = data
        self.typeOfMessage = typeOfMessage
        self.code = code
        self.codeInformation = codeInformation
        self.frame = typeOfMessage+code+data+codeInformation

    def __str__(self):
        return f"Signal(data={self.data}," \
               f" typeOfMessage={self.typeOfMessage}," \
               f" code={self.code}," \
               f" codeInformation={self.codeInformation})"





