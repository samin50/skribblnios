import pygame
import player
import random
from Client_side import Client_side

class Game():
    def __init__(self,username):
        self.run = True
        self.username = username
        self.width = 1300
        self.height = 800
        self.pad_width = int(self.width/1.4)
        self.pad_height = int(self.height/1.3)
        self.centre = (self.width/2,self.height/2)
        self.display = pygame.display.set_mode((self.width, self.height))
        self.colours = {"black": (0, 0, 0), "white": (255, 255, 255)}
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.events = pygame.event.get()
        self.brushes = []
        self.colours = []
        self.timer = 100
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.brush_size = 20


    def redraw_window(self):
        print(self.colours)
        self.display.fill((255, 255, 255))

    def return_xy(self):
        x = random.randint(0,game.width+100)
        y = random.randint(0, game.height+100)
        xy =(x,y)
        return xy

    def round_start(self):
        game.background=pygame.transform.scale(game.background,(game.width,game.height))
        game.redraw_window()
        game.display.blit(game.background,(0,0))
        canvas = pygame.Rect(self.width/2,self.height/2,self.pad_width,self.pad_height)
        canvas.center = self.centre
        pygame.draw.rect(game.display,(255,255,245),(canvas))
        while self.run == True:
            position2 = n.sed()
            game.events = pygame.event.get()
            game.clock.tick(800)
            game.brush_size = 5 #random.randint(0,50)
            #xy = self.return_xy()
            xy = pygame.mouse.get_pos()
            #if (((self.centre[0]-self.pad_width/2)<xy[0]>(self.centre[0]+self.pad_width/2)) or ((self.centre[1]-self.pad_height/2)<xy[1]>(self.centre[1]+self.pad_height/2))):
            collide = canvas.collidepoint(xy) #ARYAN ADDED
            client_section = Client_side()    #ARYAN ADDED
            position = client_section.getposition() #ARYAN ADDED
            pos_data_reply_from_host = client_section.send(position) #ARYAN ADDED
            if collide!=True:
                xy = (-300,0)

            pygame.display.update()

            #pygame.draw.rect(game.display,(0,0,0),(self.height/2,100,self.pad_width,self.pad_height))

            pygame.draw.circle(game.display,(50,200,50),(xy[0],xy[1]),10)

            #self.display.blit(canvas)
            #pygame.draw(self.display, (255,255,255), canvas)
            pygame.display.update()
            for event in game.events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            
            position.move() #ARYAN ADDED

    def load_sprites(self):
        None

game = Game("shan")
pygame.display.set_caption("player")
game.round_start()
