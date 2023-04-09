from objects.Coder import Coder
from objects.Signal import Signal
class Sender:
    def __init__(self):
        pass
    def prepareFrames(self, originalSignal,code):
        tablesOfFrames = []
        coder = Coder()
        for data in originalSignal:
            codeInformation = coder.getCodeInformation(data,code)
            tablesOfFrames.append(Signal(data,"0",code,codeInformation))
        return tablesOfFrames



