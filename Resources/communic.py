from tkinter import scrolledtext


s = score
t = timeratio


timeratio = (time_elapsed / total_time)





self.fpga.send("STARTGAME")

self.fpga.send("STARTROUND")
self.fpga.send(s)


self.fpga.send(t)   


self.fpga.send("ENDGAME")


















if selected =="start":
    self.fpga.send("STARTGAME")


if self.round_start == 1:
    self.fpga.send("STARTROUND")
    self.fpga.send(s)


while self.run == 1:
    self.fpga.send(t)


if self.game_end == 1:
    self.fpga.send("ENDGAME")







round start:
    send playerscore
    send state=roundstart

Drawing:
    send timeratio
    send draw command

Game end:
    send state=gameend