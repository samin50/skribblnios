import pygame
from Game import GameUI
from Communicator import Client
from FPGA import skribblfpga
"""
MAIN MENU needs to be reworked to allow IP address input and
nickname.
Will detect if FPGA is connected and can connect to server before
proceeding to game.
"""
class mainMenu():
    def __init__(self, fpgaInstance=None):
        self.fpgaInstance = fpgaInstance
        self.game = None
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
        self.display.fill(self.white)
        
        self.clock = pygame.time.Clock()
        pygame.init()   
        self.music = pygame.mixer.music.load("Game/assets/menu_music.mp3")
        pygame.mixer.music.play(-1)
        self.backgrounds = []
        self.gifTracker = 0
        for i in range(100):
            dir = f"Game/assets/backgrounds/{i}.gif"
            img = pygame.image.load(dir)
            img = pygame.transform.scale(img,(self.width,self.height))
            self.backgrounds.append(img)
        self.tracker=["START","CREATE CHARACTER","INSTRUCTIONS","HIGHSCORES","QUIT"]
        self.pointer=0
        pygame.display.update()
        self.display.fill(self.white)
        self.font_size=32
        self.font = "Game/assets/arcade.TTF"
        #While in main menu
        while self.isActive:
            #Update background
            self.display.fill(self.white)
            self.display.blit(self.backgrounds[self.gifTracker],(0,0))
            self.gifTracker += 1
            if self.gifTracker == len(self.backgrounds):
                self.gifTracker = 0
            #For event that occurs
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                #If key pressed
                if event.type==pygame.KEYDOWN:
                    #Key up
                    if event.key==pygame.K_UP:
                        if self.pointer > 0:
                            self.pointer -= 1
                    #Key down
                    if event.key==pygame.K_DOWN:
                        if self.pointer < len(self.tracker)-1:
                            self.pointer += 1
                    #Key enter
                    if event.key==pygame.K_RETURN:
                        if self.tracker[self.pointer] == "QUIT":
                            pygame.quit()
                            quit()
                        if self.tracker[self.pointer] == "START":
                            self.isActive = False
                            self.game = GameUI.Game("shan", self.fpgaInstance)
                            pygame.mixer.music.stop()
                            self.game.round_start()
                            return
            self.formattedText = [None]*len(self.tracker)
            self.rectText = [None]*len(self.tracker)
            pos=self.width/2
            for textIndex in range(len(self.tracker)):
                self.formattedText[textIndex] = self.highlightText(self.tracker[textIndex], textIndex==self.pointer, self.font, self.font_size)
                self.rectText[textIndex] =  self.formattedText[textIndex].get_rect()
                self.display.blit(self.formattedText[textIndex], ((int(pos - (self.rectText[textIndex][2]/2)), 80+textIndex*40)))
            pygame.display.update()
            self.clock.tick(10)

    def highlightText(self, message, highlight, font, size):
        new_font = pygame.font.Font(font, size)
        if highlight:
            edited = new_font.render(message, 0, self.white)
        else:
            edited = new_font.render(message, 0, self.black)
        return edited
    
    def getGame(self):
        return self.game

if __name__ == "__main__":
    menu = mainMenu()
        