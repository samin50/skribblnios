import pygame
import player

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

    def redraw_window(self):
        print(self.colours)
        #self.display.fill(self.colours["white"])

    def round_start(self, x,y):
        pygame.draw.circle()
        

game = Game("shan")
run = True
pygame.display.set_caption("player")
game.redraw_window() 
background=pygame.image.load("assets/sky_background.png")
#background=pygame.transform.scale(background,(game.width,game.height))

while run == True:
    
    for event in game.events:
        game.display.blit(background,(400,-300))
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    pygame.display.update()
    game.clock.tick(60)