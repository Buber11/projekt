from objects.Coder import Coder
from objects.Signal import Signal
class Sender:
    def __init__(self):
        pass
    def prepareFrames(self, originalSignal,code):
        tablesOfFrames = []
        coder = Coder()
        for frame in originalSignal:
            codeInformation = coder.getCodeInformation(frame,code)
            tablesOfFrames.append(Signal(frame,"0",code,))



