import pygame
import GameUI
from text_input import Textbox

class mainMenu():
    def __init__(self, gameInstance=None):
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
        self.port = ""
        self.fpga_connected = False
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
        self.ip_box = Textbox("Enter IP") #creating self.ip_box object for the IP
        self.ip_box.rect.center = (self.width/2,self.height/2) #position of self.ip_box on screen
        self.ip_selected = False
        self.port_box = Textbox("Enter Port") #creating self.ip_box object for the IP
        self.port_selected = False
        self.port_box.rect.center = (self.width/2,self.height/1.5) #position of self.ip_box on screen


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
            pygame.draw.rect(self.display,(255,255,255),(self.ip_box)) #self.ip_box for IP being drawn onto the display
            pygame.draw.rect(self.display,(255,255,255),(self.port_box)) #self.ip_box for IP being drawn onto the display
            if self.fpga_connected:
                pygame.draw.rect(self.display,(0,250,0),(self.fpga_box)) #box changes colour if not connected to fpga
            else:
                pygame.draw.rect(self.display,(250,0,0),(self.fpga_box))

            pygame.draw.rect(self.display,(0,200,0),(self.connect_box))
            self.display.blit(self.ip_box.message, self.ip_box.rect)
            self.display.blit(self.port_box.message, self.port_box.rect)

            if self.ip_box.rect.collidepoint(self.mouse_pos):
                self.run_text(self.ip_box)
            elif self.port_box.rect.collidepoint(self.mouse_pos):
                self.run_text(self.port_box)
            
            elif self.connect_box.collidepoint(self.mouse_pos):
                for e in pygame.event.get():
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        self.connect_pressed = True
                        self.ip =self.ip_box.text 
                        self.port =self.port_box.text
                        print(self.ip)
                        print(self.port)
                        print("CONNECTING")
                        #PUT FUNCTION TO CONNECT HERE
            
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
                if e.key == pygame.K_BACKSPACE:
                    box.text = box.text[:-1]
                    box.update()
                '''if e.key == pygame.K_RETURN:
                    if (box.text) > 0:
                        pygame.display.update(box.rect)
                        print(box.text)'''
                        #self.received_msgs.append((self.username+":  "+self.ip_box.text))
                        #print(self.messages)
                        #self.ip_box = Textbox("Type to chat")
                        #self.ip_box.rect.center = (1030,500)
    #pygame.display.flip()
    #self.display.blit(self.ip_box.message, self.ip_box.rect)
        return
if __name__ == "__main__":
    menu = mainMenu()
        