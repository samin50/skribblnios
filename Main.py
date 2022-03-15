import pygame
from Communicator import Client
#from FPGA import skribblfpga
from Game import GameUI
import threading
import time

class mainMenu():
    def __init__(self):
        pygame.init()
        self.fpga_connected = False
        self.font = pygame.font.Font("Game/assets/Gameplay.TTF", 20)

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
        self.width = 900
        self.height = 550
        self.fpga_box = pygame.Rect(self.width-110,0,110,70)
        self.connect_box = pygame.Rect(200,413,210,50)
        self.name_box = pygame.Rect(220,274,170,50) #Shan: this is where you need to move "Enter username" to
        self.name_box_border = pygame.Rect(219,274,171,50)
        self.name_box_secondary_border = pygame.Rect(170,265,277,68)
        self.lower_box = pygame.Rect(170,345,277,140)
        self.avatar_box = pygame.Rect(457,265,270,220)
        self.avatar_box_white = pygame.Rect(459,267,266,216) #Shan: you need to put the avatars here and add triangles and a switching option
        self.ip_port_box_border = pygame.Rect(224,359,160,37)
        self.ip_port_box_bg = pygame.Rect(226,361,156,33)
        self.connect_pressed = False
        self.server_connect = False
        self.isActive = True
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.background= pygame.transform.scale(self.background,(self.width,self.height))
        self.display = pygame.display.set_mode((self.width, self.height))
        #self.display.fill(self.white)

        self.clock = pygame.time.Clock()
          
        #self.music = pygame.mixer.music.load("Game/assets/bold_statement.mp3")
        #pygame.mixer.music.play(-1)
        self.backgrounds = []
        self.gifTracker = 0
        self.mouse_pos  = pygame.mouse.get_pos()
        self.username_box = GameUI.Textbox("Enter Username") #creating self.username_box object for the IP
        self.username_box.rect.center = (305,300) #position of self.username_box on screen
        self.ip_selected = False
        self.ip_port_box = GameUI.Textbox("Enter IP: Port") #creating self.ip:port object for the IP
        self.ip_port_selected = False
        self.ip_port_box.rect.center = (303,377) #position of self.username_box on screen


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
            pygame.draw.rect(self.display,(255,255,255),(self.ip_port_box))
            pygame.draw.rect(self.display,(0,0,0),(self.name_box),2)
            pygame.draw.rect(self.display,(160,217,250),(self.name_box))
            pygame.draw.rect(self.display,(0,0,0),(self.name_box_border),2)
            pygame.draw.rect(self.display,(0,0,0),(self.name_box_secondary_border), 2)
            pygame.draw.rect(self.display,(0,0,0),(self.lower_box), 2)
            pygame.draw.rect(self.display,(0,0,0),(self.avatar_box), 2)
            pygame.draw.rect(self.display,(0,0,0),(self.ip_port_box_border), 2)
            pygame.draw.rect(self.display,(240,227,40),(self.ip_port_box_bg))
            pygame.draw.rect(self.display,(255,255,255),(self.avatar_box_white))#self.username_box for IP being drawn onto the display
            pygame.draw.polygon(self.display,color=(200,0,200),points=[(480,376), (520,326), (520,426)])
            pygame.draw.polygon(self.display,color=(0,0,0),points=[(478,377), (520,325), (520,428)],width=4)
            pygame.draw.polygon(self.display,color=(200,0,200),points=[(700,376), (659,326), (659,426)])
            pygame.draw.polygon(self.display,color=(0,0,0),points=[(702,377), (658,325), (658,428)],width=4)
            
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

                if e.key == pygame.K_BACKSPACE:
                  box.text = box.text[:-1]
                  box.update()

                box.add_chr(pygame.key.name(e.key))
                if (len(box.text) < 15):

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
                #self.FPGA = skribblfpga.SkribblNIOS(self)
                print("This is meant to be the FPGA thread, but wont work on mac")
                #self.fpga_connected = True
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
        username = "aryan"
        ip = "146.169.186.165:9999"
        connectionData = ip.split(":")
        try:
            self.Client = Client.Client(username, connectionData[0], int(connectionData[1]))
        except:
            print("Unable to connect to server, check IP or if server is running.")
            return
        #Instantiate game and hook FPGA
        self.isActive = False
        self.Game = GameUI.Game(username, self.FPGA, self.Client)
        self.Client.setGame(self.Game)
        if self.fpga_connected:
            self.FPGA.setGame(self.Game)
        self.fpga_connected = True
        self.Game.round_start()
        return

if __name__ == "__main__":
    menu = mainMenu()
        