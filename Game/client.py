import pygame
import player
import random
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
        self.fps = 800

        self.events = pygame.event.get()
        self.colour_string = "" 
        self.timer = 100
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.brush_size = 20
        self.game_music = pygame.mixer.music.load("Game/assets/menu_music.mp3")
        self.draw_timer = 0
        self.frame_counter = 0

    def redraw_window(self):
        print(self.colours)
        self.display.fill((255, 255, 255))

    def return_xy(self):
        x = random.randint(0,game.width+100)
        y = random.randint(0, game.height+100)
        xy =(x,y)
        return xy

<<<<<<< HEAD
    def round_start(self):
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
        self.redraw_window()
        self.display.blit(self.background,(0,0))
        canvas = pygame.Rect(self.width/2,self.height/2,self.pad_width,self.pad_height)
        canvas.center = self.centre
        pygame.draw.rect(self.display,(255,255,245),(canvas))
        while self.run == True:
            self.events = pygame.event.get()

            self.clock.tick(800)
            self.brush_size = 5 #random.randint(0,50)

            #xy = self.return_xy()
            xy = pygame.mouse.get_pos()
            #if (((self.centre[0]-self.pad_width/2)<xy[0]>(self.centre[0]+self.pad_width/2)) or ((self.centre[1]-self.pad_height/2)<xy[1]>(self.centre[1]+self.pad_height/2))):
            collide = canvas.collidepoint(xy)

            if collide!=True:
                xy = (-300,0)

            pygame.display.update()
            #pygame.draw.rect(game.display,(0,0,0),(self.height/2,100,self.pad_width,self.pad_height))

=======
    def music_change(self):
            pygame.mixer.music.stop()
            self.game_music = pygame.mixer.music.load("Game/assets/drawing_music.mp3")
            pygame.mixer.music.play(-1)



    def round_start(self):
        pygame.mixer.music.play(-1)
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
        self.redraw_window()
        self.display.blit(self.background,(0,0))
        canvas = pygame.Rect(self.width/2,self.height/2,self.pad_width,self.pad_height)
        canvas.center = self.centre
        pygame.draw.rect(self.display,(255,255,245),(canvas))

        while self.run == True:
            self.frame_counter+=1
            if (self.frame_counter % self.fps): #counts number of seconds player is drawing using the frame rate of the game
                self.draw_timer+=1
            if self.draw_timer == 1:
                self.music_change()
            self.events = pygame.event.get()

            self.clock.tick(self.fps)
            self.brush_size = 5 #random.randint(0,50)

            #xy = self.return_xy()
            xy = pygame.mouse.get_pos()
            #if (((self.centre[0]-self.pad_width/2)<xy[0]>(self.centre[0]+self.pad_width/2)) or ((self.centre[1]-self.pad_height/2)<xy[1]>(self.centre[1]+self.pad_height/2))):
            collide = canvas.collidepoint(xy)

            if collide!=True:
                xy = (-300,0)

            pygame.display.update()
            #pygame.draw.rect(game.display,(0,0,0),(self.height/2,100,self.pad_width,self.pad_height))

>>>>>>> clientgame
            pygame.draw.circle(self.display,(50,200,50),(xy[0],xy[1]),10)
            #self.display.blit(canvas)
            #pygame.draw(self.display, (255,255,255), canvas)
            pygame.display.update()
            for event in self.events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

    def load_sprites(self):
        None
