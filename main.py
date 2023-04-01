from objects.Receiver import Receiver
from objects.Signal import Signal

while True:
    print("Menu:")
    choice = int(input("napisz ilosc bitów danych w każdej ramce:"))
    length = choice
    print("wybierz kod detekcyjny:")
    print("CRC8 -1")
    print("CRC16 -2")
    print("kontrola parzystości -3")
    choice = int(input("wybór: "))
    print("\n")
    if choice == 1:
        usedCode = "01"
    if choice == 2:
        usedCode = "10"
    if choice == 3:
        usedCode = "11"
    receiver = Receiver(length)
    receiver.createSignals("dane.txt", usedCode, "1", "Reszta")
    print(receiver.tableOfFrames[0].frame)
    print("\n")
    print("czy zakończyć?")
    print("TAK -1")
    print("NIE -2")
    choice = int(input("wybór: "))
    if choice == 1:
        break
    print("\n\n")










