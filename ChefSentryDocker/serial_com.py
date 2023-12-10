import serial
import time


class Serial:
    startMarker = '<'
    endMarker = '>'
    dataStarted = False
    dataBuf = ""
    messageComplete = False

    def __init__(self, port, baudrate):
        self.serialPort = None
        self.setupSerial(baudrate, port)

    def setupSerial(self, baudRate, serialPortName):

        self.serialPort = serial.Serial(port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True)

        print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

        # waitForArduino()

    # ========================

    def sendToArduino(self, stringToSend):
        # this adds the start- and end-markers before sending

        stringWithMarkers = self.startMarker
        stringWithMarkers += stringToSend
        stringWithMarkers += self.endMarker

        self.serialPort.write(stringWithMarkers.encode('utf-8'))  # encode needed for Python3

    # ==================

    def recvLikeArduino(self):

        if self.serialPort.inWaiting() > 0 and self.messageComplete == False:
            x = self.serialPort.read().decode("utf-8")  # decode needed for Python3

            if self.dataStarted:
                if x != self.endMarker:
                    self.dataBuf = self.dataBuf + x
                else:
                    self.dataStarted = False
                    self.messageComplete = True
            elif x == self.startMarker:
                self.dataBuf = ''
                self.dataStarted = True

        if self.messageComplete:
            self.messageComplete = False
            return self.dataBuf
        else:
            return "XXX"

        # ==================

    def waitForArduino(self):
        # wait until the Arduino sends 'Arduino is ready' - allows time for Arduino reset
        # it also ensures that any bytes left over from a previous message are discarded

        print("Waiting for Arduino to reset")

        msg = ""
        while msg.find("Arduino is ready") == -1:
            msg = self.recvLikeArduino()
            if not (msg == 'XXX'):
                print(msg)
