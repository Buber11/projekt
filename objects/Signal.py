class Signal:
    def __init__(self,data,typeOfMessage,usedCode,restOfDivision):
        self.data = data
        self.type = typeOfMessage
        self.code = usedCode
        self.restOfDivison = restOfDivision
        self.createSignal()

    def createSignal(self):
        self.frame = self.type + self.code + self.data + self.restOfDivison





