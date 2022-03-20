import pygame
from Communicator import Client
try:
    from FPGA import skribblfpga
except Exception as e:
    print("FPGA import error, continuing without FPGA support.")
from Game import GameUI
import threading
import time

class mainMenu():
    def __init__(self):
        pygame.init()
        self.fpga_connected = False
        self.font = pygame.font.Font("Game/assets/Gameplay.TTF", 20)
        self.font_large = pygame.font.Font("Game/assets/Sketch College.TTF", 85)
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
        self.width = 950
        self.height = 550
        self.events = pygame.event.get()
        self.box_width = 320
        self.box_height =50 
        self.box_x = 150
        self.char_box_x = 570
        self.char_box_size = (270,220)
        self.fpga_box = pygame.Rect(self.width-110,0,110,70)
        self.fpga_cross  = pygame.image.load("Game/assets/cross.png")
        self.fpga_tick = pygame.image.load("Game/assets/tick.png")
        self.connect_box = pygame.Rect(214,413,210,50)
        self.name_box = pygame.Rect(self.box_x+10,274,self.box_width,50) #Shan: this is where you need to move "Enter username" to
        self.name_box_border = pygame.Rect(self.box_x+10,274,self.box_width+1,50)
        self.name_box_secondary_border = pygame.Rect(self.box_x,265,self.box_width+20,68)
        self.lower_box = pygame.Rect(self.box_x,345,self.box_width+20,140)
        self.avatar_box = pygame.Rect(self.char_box_x,265,self.char_box_size[0],self.char_box_size[1])
        self.avatar_box_white = pygame.Rect(self.char_box_x,265,self.char_box_size[0],self.char_box_size[1]) #Shan: you need to put the avatars here and add triangles and a switching option
        self.ip_port_box_border = pygame.Rect(self.box_x+10,359,self.box_width,37)
        self.ip_port_box_bg = pygame.Rect(self.box_x+10,361,self.box_width,33)
        self.connect_pressed = False
        self.server_connect = False
        self.isActive = True
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.background= pygame.transform.scale(self.background,(self.width,self.height))
        self.display = pygame.display.set_mode((self.width, self.height))
        self.text_limit = 24

        self.triangle_button1 = pygame.Rect(520,325,40,100) #rect for collosion detection of traingle buttons
        self.triangle_button2 = pygame.Rect(self.char_box_x + self.char_box_size[0]+10,325,40,100)
#avatars:
        self.avatar_list = [
            pygame.image.load("Game/assets/avatars/1.png"),
            pygame.image.load("Game/assets/avatars/2.png"),
            pygame.image.load("Game/assets/avatars/3.png"),
            pygame.image.load("Game/assets/avatars/4.png"),
            pygame.image.load("Game/assets/avatars/5.png"),
            pygame.image.load("Game/assets/avatars/6.png"),
            pygame.image.load("Game/assets/avatars/7.png"),
            pygame.image.load("Game/assets/avatars/8.png")
            ]
        self.avatar = 0
        self.clock = pygame.time.Clock()
          
        #self.music = pygame.mixer.music.load("Game/assets/bold_statement.mp3")
        #pygame.mixer.music.play(-1)
        self.backgrounds = []
        self.gifTracker = 0
        self.mouse_pos  = pygame.mouse.get_pos()
        self.username_box = GameUI.Textbox("Enter Username") #creating self.username_box object for the IP
        self.username_box.rect.center = (self.box_x+167,300) #position of self.username_box on screen
        self.ip_selected = False
        self.ip_port_box = GameUI.Textbox("Enter IP: Port") #creating self.ip:port object for the IP
        self.ip_port_selected = False
        self.ip_port_box.rect.center = (self.box_x+170,379) #position of self.username_box on screen


        for i in range(120):
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

            self.events = pygame.event.get()
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

            
            
            pygame.draw.rect(self.display,(240,227,40),(self.ip_port_box_bg))
            pygame.draw.rect(self.display,(0,0,0),(self.ip_port_box_border), 2)
            #pygame.draw.rect(self.display,(255,255,255),(self.avatar_box_white))#self.username_box for IP being drawn onto the display
            #pygame.draw.rect(self.display,(0,0,0),(self.avatar_box), 2)
            pygame.draw.polygon(self.display,color=(200,0,200),points=[(520,376), (560,326), (560,426)])
            pygame.draw.polygon(self.display,color=(0,0,0),points=[(520,376), (560,326), (560,426)],width=4)
            pygame.draw.polygon(self.display,color=(200,0,200),points=[(self.char_box_x + self.char_box_size[0]+50,377), (self.char_box_x + self.char_box_size[0]+10,325), (self.char_box_x + self.char_box_size[0]+10,428)])
            pygame.draw.polygon(self.display,color=(0,0,0),points=[(self.char_box_x + self.char_box_size[0]+50,377), (self.char_box_x + self.char_box_size[0]+10,325), (self.char_box_x + self.char_box_size[0]+10,428)],width=4)
            #pygame.draw.rect(self.display,(self.avatar*10,self.avatar*40,self.avatar*20),(self.avatar_list[self.avatar])) #avatar
            self.display.blit(self.avatar_list[self.avatar],(self.char_box_x+65,300))
            


            #pygame.draw.rect(self.display,(0,0,0),(self.triangle_button1))
            #pygame.draw.rect(self.display,(0,0,0),(self.triangle_button2))
            if self.fpga_connected:
                self.display.blit(self.fpga_tick,(self.fpga_box))
                #pygame.draw.rect(self.display,(0,250,0),(self.fpga_box)) #box changes colour if not connected to fpga
            else:
                self.display.blit(self.fpga_cross,(self.fpga_box))
                #pygame.draw.rect(self.display,(250,0,0),(self.fpga_box))

            pygame.draw.rect(self.display,(0,200,0),(self.connect_box))
            self.display.blit(self.username_box.message, self.username_box.rect)
            self.display.blit(self.ip_port_box.message, self.ip_port_box.rect)
            
            #Collisions:
            if self.name_box.collidepoint(self.mouse_pos):
                self.run_text(self.username_box)
            elif self.ip_port_box_bg.collidepoint(self.mouse_pos):
                self.run_text(self.ip_port_box)

            elif self.triangle_button1.collidepoint(self.mouse_pos):
                self.next_avatar(False)
            elif self.triangle_button2.collidepoint(self.mouse_pos):
                self.next_avatar(True)


            
            elif self.connect_box.collidepoint(self.mouse_pos):
                for e in self.events:
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        self.connect_pressed = True
                        #PUT FUNCTION TO CONNECT HERE
                        self.instantiateGame(self.username_box.text, self.ip_port_box.text)

            #FONTS:
            title = self.font_large.render('Skribblnios', True, self.black)
            title_rect = title.get_rect(center=(self.width/2,140))
            self.display.blit(title,title_rect)

            connect = self.font.render('Connect', True, self.black)
            connect_rect = connect.get_rect(center=(220+100,413+25))
            self.display.blit(connect,connect_rect)
            
            self.gifTracker += 1
            if self.gifTracker == len(self.backgrounds): #ignore all the gifTrack stuff, it's for the background animation
                self.gifTracker = 0
            self.ip = ""


            for events in self.events: #Checks if ur clicking the exit button
                if events.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
            self.clock.tick(30)

    #character select cycle
    def next_avatar(self,right):
        for event in self.events:
            if event.type ==pygame.MOUSEBUTTONDOWN:
                if right:
                    if self.avatar<len(self.avatar_list)-1:
                        self.avatar+=1
                    else:
                        self.avatar = 0 
                else:
                    if self.avatar>0:
                        self.avatar -=1
                    else:
                        self.avatar = len(self.avatar_list)-1
                    

    def run_text(self,box):
        for e in self.events:
            self.display.blit(box.message,box.rect)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                  box.text = box.text[:-1]
                  box.update()
                elif len(box.text)>self.text_limit: #text limiter for box
                    continue
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
    def closeAll(self):
        if self.FPGA is not None:
            self.FPGA.stop()

    def connectFPGA(self):
        while not self.fpga_connected:
            try:
                #Check if FPGA connected every 2.5 sec
                time.sleep(2.5)
                self.FPGA = skribblfpga.SkribblNIOS(self)
                self.FPGA.send("I 0 0") #Send connected signal to FPGA
                self.fpga_connected = True
                return
            except Exception as e:
                print(e)
        return

    def instantiateGame(self, username, ip):
        #username = "test"
        ip = "26.168.146.5:9999"
        #ip ="34.230.47.14:9999"
        if len(username) == 0:
            print("Enter a username!")
            return
        if len(ip) == 0:
            print("Enter a server ip!")
            return
        #Ensure FPGA is connected
        if self.fpga_connected == False:
            print("FPGA not connected!")
            print("Will use mouse")
            #return
        #Attempt to connect to server
        connectionData = ip.split(":")
        self.Client = Client.Client(username, connectionData[0], int(connectionData[1]))
        #Instantiate game and hook FPGA
        self.isActive = False
        self.Game = GameUI.Game(username, self.FPGA, self.Client, self.avatar)
        self.Client.setGame(self.Game)
        if self.fpga_connected:
            self.FPGA.setGame(self.Game)
            self.FPGA.start()
        self.Client.setGame(self.Game)
        self.fpga_connected = True
        self.Game.round_start()
        return

if __name__ == "__main__":
    menu = mainMenu()
        