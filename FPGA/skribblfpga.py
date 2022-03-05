import threading
import intel_jtag_uart

class SkribblNIOS():
    #Instantiate only once
    def __init__(self):
        self.Connected = False
        try:
            self.UART = intel_jtag_uart.intel_jtag_uart()
        except Exception as e:
            self.Connected = True
            print(e)
            exit(0)
        self.isActive = False
        self.sendThread = None
        self.recieveThread = None

    def setGame(self, game):
        self.gameInstance = game
        return
    
    def isConnected(self):
        return self.Connected
    
    #Will be used to change the parameters that is sent to the draw function
    def changeParams(self):
        return
    
    #Start gathering XY coords to send to program, can be disabled ie for when the current user isnt drawing
    def start(self):
        if self.isActive == True:
            self.isActive = False
            return
        self.isActive = True
        self.sendThread = threading.Thread(target=self.getXY)
        self.sendThread.start()
        return

    #Dont use, handled by start
    def getXY(self):
        while self.isActive:
            XYData = self.UART.read().decode('utf-8')
            if self.gameInstance is None:
                if len(XYData) > 0:
                    print(XYData)
            else:
                #Use parameters here
                self.gameInstance.Draw(XYData) #Game drawing function
        return

    #Used to update data on the FPGA, unless KILL is sent
    def send(self, outputStr):
        if outputStr == "KILL":
            self.stop()
            return
        sendStr = bytes(outputStr+'\n', 'utf-8')
        self.UART.write(sendStr)

    #Disable XY gathering, used for when the player isnt drawing
    def disable(self):
        self.isActive = False
        self.sendThread.join()
    
    #Close the JTAG connection, used when the game closes
    def stop(self):
        self.disable()
        self.UART.write(b'KILL\n')
        self.UART.close()

if __name__ == "__main__": 
    FPGA = SkribblNIOS()
    FPGA.start()
    inputCmd = str()
    while inputCmd != "KILL":
        inputCmd = input("Enter command: ")
        FPGA.send(inputCmd)
    print("Exited.")


