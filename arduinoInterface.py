import time
import serial
import config
from threading import Thread

# connects to board
def connect():
    try:
        ard = serial.Serial(port=config.ARDUINO_PORT, baudrate=9600, timeout=.1)
        return ard
    except:
        print(f"{config.getTime()}: No Arduino Connection")
        return -1

# set led colors
def setColors(colorString):
    global currentColorsA
    currentColorsA[int(colorString[len(colorString) - 1])] = colorString[:len(colorString) - 1]
    if arduino != -1:
        arduino.write(colorString.encode())

# gets data from the Arduino
def getDataLoop():
    global arduino, recordedTemperatureData, currentTemp
    while True:

        # reconnect if needed
        if arduino == -1:
            time.sleep(20)
            arduino = connect()
            continue

        # reads the Serial until relevant data is found
        try:
            line = str(arduino.readline())
        # handles lost connections
        except:
            print(f"{config.getTime()}: Failed to read Arduino data")
            time.sleep(20)
            arduino = connect()
            continue

        if (line != "b''") and "TEMP DATA" in line:

            # gets data from string
            seg = ""
            dataArray = []
            for char in line:
                if char in "-0123456789.":
                    seg += char
                if (char == " ") or (char == "\\"):
                    try:
                        if seg != "":
                            dataArray.append(float(seg))
                    except ValueError:
                        print(f"\n{config.getTime()}: Error reading Arduino: {seg} \n{line}\n")
                    seg = ""
            if not dataArray:
                dataArray = [-99.99, -99.99]
            print(f"{config.getTime()}: Reading: {line} \nGot: {dataArray}")

            # update records with new data
            currentTemp = dataArray[0]
            averageTemp = dataArray[1]
            if (recordedTemperatureData[0] != averageTemp) and (averageTemp != -99.99):
                recordedTemperatureData = config.updateArray(recordedTemperatureData, averageTemp)
                config.updateRecords(recordedTemperatureData, config.RECORD_FILE_RED)
            time.sleep(1)

print(f"{config.getTime()}: ensureFileExists, {config.RECORD_FILE_RED},"
      f" status: {config.ensureFileExists(config.RECORD_FILE_RED)}")
recordedTemperatureData = config.loadRecords(config.RECORD_FILE_RED)
currentTemp = 0
currentColorsA = ["000 000 000", "000 000 000"]
arduino = connect()

# starts arduinoInterface
threadTemp = Thread(target=getDataLoop)
threadTemp.start()
print(f"{config.getTime()}: Started arduinoInterface")