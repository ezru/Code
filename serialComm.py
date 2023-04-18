import serial

arduinoSer1 = serial.Serial('com10', 9600)

fingerList = [0, 1, 1, 0, 0]
fingSerial = ''
for fing in fingerList:
    fingSerial = fingSerial + str(fing)
fingSerial += '\r'
print(fingSerial)
arduinoSer1.write(fingSerial.encode())


print(fingSerial)

while True:
    cmd = input('Enter your command: ')
    if cmd == "q":
        break
    else:
        cmd = cmd + "\r"
        arduinoSer1.write(cmd.encode())

arduinoSer1.close()
