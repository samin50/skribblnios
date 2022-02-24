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
        self.background = pygame.image.load("assets/sky_background.png")

    def redraw_window(self):
        print(self.colours)
        self.display.fill((255, 255, 255))

    def round_start(self, x,y):
        pygame.draw.circle()
        


game = Game("shan")
run = True
pygame.display.set_caption("player")
 
game.background=pygame.transform.scale(game.background,(game.width,game.height))

while run == True:
    game.events = pygame.event.get()
    game.clock.tick(60)
    game.redraw_window()
    game.display.blit(game.background,(400,-300))
    pygame.display.update()

    for event in game.events:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    