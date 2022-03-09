from tkinter import EventType
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
        for i in range(100):
            dir = f"Game/assets/backgrounds/{i}.gif"
            img = pygame.image.load(dir)
            img = pygame.transform.scale(img,(self.width,self.height))
            self.backgrounds.append(img)

        #self.display.fill(self.white)
        #self.display.blit(self.backgrounds[gif_track],(0,0))
        #self.font_size=32
        self.font = pygame.font.Font("Game/assets/arcade.TTF",32)
        self.ip_box = Textbox("            ") #creating self.ip_box object for the IP
        self.ip_box.rect.center = (self.width/2,self.height/2) #position of self.ip_box on screen
        self.events = pygame.event.get()
        #While in main menu
        while self.isActive:
            self.events = pygame.event.get()
            #Update background
            self.display.fill(self.white)
            self.display.blit(self.backgrounds[self.gifTracker],(0,0))
            pygame.draw.rect(self.display,(0,0,0),(self.ip_box)) #self.ip_box for IP being drawn onto the display
            print("HALLOOO")

            self.display.blit(self.ip_box.message, self.ip_box.rect)
            self.run_text()
            
            self.gifTracker += 1
            if self.gifTracker == len(self.backgrounds): #ignore all the gifTrack stuff, it's for the background animation
                self.gifTracker = 0
            self.ip = ""
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.run = False
                if e.type == pygame.KEYDOWN:
                    self.ip_box.add_chr(pygame.key.name(e.key))
                    if e.key == pygame.K_SPACE:
                        if len(self.ip_box.text)<20:
                            self.ip_box.text += " "
                            self.ip_box.update()
                        else:
                            print("Text too long")
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        self.ip_box.upper_case = True
                    if e.key == pygame.K_BACKSPACE:
                        self.ip_box.text = self.ip_box.text[:-1]
                        self.ip_box.update()
                if e.key == pygame.K_RETURN:
                    if len(self.ip_box.text) > 0:
                        pygame.display.update(self.ip_box.rect)
                        print(self.ip_box.text)
                        #self.received_msgs.append((self.username+":  "+self.ip_box.text))
                        #print(self.messages)
                        #self.ip_box = Textbox("Type to chat")
                        #self.ip_box.rect.center = (1030,500)


            for events in pygame.event.get(): #Checks if ur clicking the exit button
                if events.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()
            self.clock.tick(10)

    def run_text(self):
        #pygame.display.flip()
        #self.display.blit(self.ip_box.message, self.ip_box.rect)
        
if __name__ == "__main__":
    menu = mainMenu()
        