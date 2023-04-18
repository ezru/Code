import serial, random, time

handSignal = ''
arduinoSerial1 = serial.Serial('com7',9600)

while True:
    choice = random.randint(1, 3)
    
    if choice == 1:
        handSignal = '00000\r'
    elif choice == 2:
        handSignal = '11111\r'
    else:
        handSignal = '01100\r'
        
    arduinoSerial1.write(handSignal.encode())
        
    print(handSignal)
    time.sleep(2)
    
    