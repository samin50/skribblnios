import threading
import intel_jtag_uart

class SkribblNIOS():
    #Instantiate only once
    def __init__(self, gameInstance=None):
        self.gameInstance = gameInstance
        self.UART = intel_jtag_uart.intel_jtag_uart()
        self.isActive = False
        self.sendThread = None
        self.recieveThread = None

    def setGame(self, game):
        self.gameInstance = game
        return
    
    #Will be used to change the parameters that is sent to the draw function
    def changeParams(self):
        return
    
    #Start gathering XY coords to send to program, can be disabled ie for when the current user isnt drawing
    def start(self):
        if self.isActive == True:
            self.isActive = False
            return
        self.isActive = True
        self.sendThread = threading.Thread(target=self.getXY, daemon=True)
        self.sendThread.start()
        return

    #Dont use, handled by start
    def getXY(self):
        while self.isActive:
            try:
                Data = self.UART.read().decode('utf-8')
            except:
                print("Error, connection lost to FPGA.")
                continue
            if len(Data) > 0:
                print(Data)
                #Use parameters here
                if self.gameInstance is not None:
                    try: #Sometimes all data from FPGA is not recieved, causing errors
                        commandParam = Data.split()
                        if commandParam[0] == 'C':
                            self.gameInstance.draw_check(int(commandParam[2]), -int(commandParam[1]), True) #Game drawing function
                        elif commandParam[0] == 'S':
                            self.gameInstance.switch_update(str(int(commandParam[1], base=2)))
                        elif commandParam[0] == 'B':
                            if commandParam[1] == "1":
                                self.gameInstance.size_update(True)
                            elif commandParam[1] == "2":
                                self.gameInstance.size_update(False)
                    except:
                        None
                else:
                    print(Data)
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


