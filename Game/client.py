import pygame
import player
import random
class Game():
    def __init__(self,username):
        self.username = username
        self.width = 1300
        self.height = 700
        self.display = pygame.display.set_mode((self.width, self.height))
        self.colours = {"black": (0, 0, 0), "white": (255, 255, 255)}
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.events = pygame.event.get()
        self.brushes = []
        self.colours = []
        self.timer = 100
        self.background = pygame.image.load("assets/sky_background.png")
        self.brush_size = 20

    def redraw_window(self):
        print(self.colours)
        self.display.fill((255, 255, 255))

    def round_start(self, x,y,size):
        pygame.draw.circle(game.display,(0,0,0),(x,y),size)

game = Game("shan")
run = True
pygame.display.set_caption("player")

def return_x():
    x = random.randint(0,game.width)
    return x

def return_y():
    y = random.randint(0, game.height)
    return y

game.background=pygame.transform.scale(game.background,(game.width,game.height))
game.redraw_window()
game.display.blit(game.background,(0,0))
y = 0
x = 0
while run == True:
    game.events = pygame.event.get()

    game.clock.tick(144)
    game.brush_size = 5 #random.randint(0,50)
    y +=1
    x +=1
    game.round_start(x,y,game.brush_size)
    pygame.display.update()

    for event in game.events:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()