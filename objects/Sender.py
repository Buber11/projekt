from objects.Coder import Coder
from objects.Signal import Signal


class Sender:
    def __init__(self):
        pass

    def prepareFrames(self, originalSignal, code):
        if len(originalSignal) == 1:
            coder = Coder()
            codeInformation = coder.getCodeInformation(originalSignal, code)
            return Signal(originalSignal, "0", code, codeInformation)

        tablesOfFrames = []
        coder = Coder()
        for data in originalSignal:
            codeInformation = coder.getCodeInformation(data, code)
            tablesOfFrames.append(Signal(data, "0", code, codeInformation))
        return tablesOfFrames
