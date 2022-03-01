import Communicator #Will force the communicator to start first
from FPGA import skribblfpga
from Game import client
FPGA = skribblfpga.SkribblNIOS()
if FPGA.isConnected() == False:
    exit()
Game = client.Game('playerName')
FPGA.setGame(Game)
FPGA.start()
print("Game started.")