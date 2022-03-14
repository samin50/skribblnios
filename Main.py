import pygame
from Communicator import Client
from FPGA import skribblfpga
from Game import GameUI
import threading
import time
class mainMenu():
    def __init__(self):
        self.fpga_connected = False
        self.FPGA = None
        self.Client = None
        self.initiateFPGA = threading.Thread(target=self.connectFPGA, daemon=True)
        self.initiateFPGA.start()
        pygame.init()
        #Define white colour
        self.white = (205, 205, 205) 
        self.black = (0, 0, 0)
        """ 
        brown=(150,75,0)
        red=(255, 0, 0)
        yellow=(255, 255, 0)
        blue=(0, 0, 255)
        green=(0, 255, 0)
        grey=(128, 128, 128)
        turquoise = (0,255,239)"""
        #Declare dimensions and background
        self.ip = ""
        self.ip_port = ""
        self.fpga_box = pygame.Rect(300,300,70,50)
        self.connect_box = pygame.Rect(500,300,100,50)
        self.connect_pressed = False
        self.server_connect = False
        self.isActive = True
        self.width = 900
        self.height = 550
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.background= pygame.transform.scale(self.background,(self.width,self.height))
        self.display = pygame.display.set_mode((self.width, self.height))
        #self.display.fill(self.white)
        
        self.clock = pygame.time.Clock()
          
        self.music = pygame.mixer.music.load("Game/assets/menu_music.mp3")
        pygame.mixer.music.play(-1)
        self.backgrounds = []
        self.gifTracker = 0
        self.mouse_pos  = pygame.mouse.get_pos()
        self.username_box = GameUI.Textbox("Enter Username") #creating self.username_box object for the IP
        self.username_box.rect.center = (int(self.width/2),int(self.height/2)) #position of self.username_box on screen
        self.ip_selected = False
        self.ip_port_box = GameUI.Textbox("Enter IP:Port") #creating self.ip:port object for the IP
        self.ip_port_selected = False
        self.ip_port_box.rect.center = (int(self.width/2),int(self.height/1.5)) #position of self.username_box on screen


        for i in range(100):
            dir = f"Game/assets/backgrounds/{i}.gif"
            img = pygame.image.load(dir)
            img = pygame.transform.scale(img,(self.width,self.height))
            self.backgrounds.append(img)

        #self.display.fill(self.white)
        #self.display.blit(self.backgrounds[gif_track],(0,0))
        #self.font_size=32
        #self.font = pygame.font.Font("Game/assets/arcade.TTF",32)

        #While in main menu
        while self.isActive:
            #Update background
            self.mouse_pos = pygame.mouse.get_pos()
            
            self.display.fill(self.white)
            self.display.blit(self.backgrounds[self.gifTracker],(0,0))
            pygame.draw.rect(self.display,(255,255,255),(self.username_box)) #self.username_box for IP being drawn onto the display
            pygame.draw.rect(self.display,(255,255,255),(self.ip_port_box)) #self.username_box for IP being drawn onto the display
            if self.fpga_connected:
                pygame.draw.rect(self.display,(0,250,0),(self.fpga_box)) #box changes colour if not connected to fpga
            else:
                pygame.draw.rect(self.display,(250,0,0),(self.fpga_box))

            pygame.draw.rect(self.display,(0,200,0),(self.connect_box))
            self.display.blit(self.username_box.message, self.username_box.rect)
            self.display.blit(self.ip_port_box.message, self.ip_port_box.rect)

            if self.username_box.rect.collidepoint(self.mouse_pos):
                self.run_text(self.username_box)
            elif self.ip_port_box.rect.collidepoint(self.mouse_pos):
                self.run_text(self.ip_port_box)
            
            elif self.connect_box.collidepoint(self.mouse_pos):
                for e in pygame.event.get():
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        self.connect_pressed = True
                        #PUT FUNCTION TO CONNECT HERE
                        self.instantiateGame(self.username_box.text, self.ip_port_box.text)
            
            self.gifTracker += 1
            if self.gifTracker == len(self.backgrounds): #ignore all the gifTrack stuff, it's for the background animation
                self.gifTracker = 0
            self.ip = ""


            for events in pygame.event.get(): #Checks if ur clicking the exit button
                if events.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
            self.clock.tick(30)

    def run_text(self,box):
        for e in pygame.event.get():
            self.display.blit(box.message,box.rect)
            if e.type == pygame.KEYDOWN:
                box.add_chr(pygame.key.name(e.key))
                if e.key == pygame.K_SPACE:
                    if len(box.text)<20:
                        box.text += " "
                        box.update()
                    else:
                        print("Text too long")
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    box.upper_case = True
                else:
                    box.upper_case = False
                if e.key == pygame.K_BACKSPACE:
                    box.text = box.text[:-1]
                    box.update()
                '''if e.key == pygame.K_RETURN:
                    if (box.text) > 0:
                        pygame.display.update(box.rect)
                        print(box.text)'''
                        #self.received_msgs.append((self.username+":  "+self.username_box.text))
                        #print(self.messages)
                        #self.username_box = Textbox("Type to chat")
                        #self.username_box.rect.center = (1030,500)
    #pygame.display.flip()
    #self.display.blit(self.username_box.message, self.username_box.rect)
        return
    def connectFPGA(self):
        while not self.fpga_connected:
            try:
                #Check if FPGA connected every 2.5 sec
                time.sleep(2.5)
                self.FPGA = skribblfpga.SkribblNIOS(self)
                self.fpga_connected = True
            except Exception as e:
                print(e)
        return

    def instantiateGame(self, username, ip):
        #Ensure FPGA is connected
        if self.fpga_connected == False:
            print("FPGA not connected!")
            print("Will use mouse")
            #return
        #Attempt to connect to server
        username = "test"
        ip = "26.168.146.5:9999"
        connectionData = ip.split(":")
        try:
            self.Client = Client.Client(username, connectionData[0], int(connectionData[1]))
        except:
            print("Unable to connect to server, check IP or if server is running.")
            return
        #Instantiate game and hook FPGA
        self.isActive = False
        self.Game = GameUI.Game(username, self.FPGA, self.Client)
        if self.fpga_connected:
            self.FPGA.setGame(self.Game)
        self.Client.setGame(self.Game)
        self.fpga_connected = True
        self.Game.round_start()
        return

if __name__ == "__main__":
    menu = mainMenu()
        