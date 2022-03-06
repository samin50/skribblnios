import pygame
import player
import random
from text_input import *
class Game():
    def __init__(self,username):
        self.run = True
        self.username = username
        self.width = 1200
        self.height = 600
        self.display = pygame.display.set_mode((self.width, self.height))
        ##self.fpga.send("S " Timelen(s) " 0")
        self.canvas_width = int(self.width/1.6)
        self.canvas_height = int(self.height/1.3)
        self.canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.centre = (self.width/2,self.height/2)
        
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
        
        self.colours= [[0,0,0],[0,0,0],[0,0,0]] # 3-bit binary value representing colour switch state
        #each bit represents the rgb value 64 
        self.switches = [0,0,0,0,0,0,0,0,0]
        self.brush_colour = (0,0,0)
        self.colour_change = False
        self.draw_blit = False
       
        
        self.chatbox = pygame.Rect(self.width/5,self.height/2,self.canvas_width/2.5,self.canvas_height)
        self.is_typing = False
        


    def redraw_window(self):
        self.display.fill((255, 255, 255))

    def return_xy(self):
        x = random.randint(0,self.width+100)
        y = random.randint(0, self.height+100)
        xy =(x,y)
        return xy

    def music_change(self):
        pygame.mixer.music.stop()
        self.game_music = pygame.mixer.music.load("Game/assets/drawing_music.mp3")
        pygame.mixer.music.play(-1)

    def blti(self,binlist): #binary list to int
        return int(''.join(map(str, binlist)), 2)


    def colour_update(self):
        self.brush_colour = ((self.blti(self.colours[0])<<5),(self.blti(self.colours[1])<<5),(self.blti(self.colours[2])<<5)) #RGB

    def switch_update(self):
        for i in range(len(self.colours)):
            for j in range(len(self.colours[i])):
                self.colours[i][j] = random.randint(0,1)
               
    def mouse_down(self,draw):
        for event in self.events:
            if draw == True:
                self.typing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #return True
                    self.draw_blit = True
                    print("DOWN")
                elif event.type == pygame.MOUSEBUTTONUP:
                    #return False
                    self.draw_blit = False
                    print("UP")
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("TYPING")
                    self.typing = True
                else:
                    self.typing = False

    def typing(self):
        text= run_textbox(self.display,"enter text",(self.width/1.16,self.height/2))
        print(text)




    def round_start(self):
        pygame.mixer.music.play(-1)
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
        self.redraw_window()
        self.display.blit(self.background,(0,0))
        ##self.fpga.send("R " Position " " Score)
        

        #canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.canvas.center = (self.width/2.5,self.height/2)
        self.chatbox.center = (self.width/1.16,self.height/2)
        pygame.draw.rect(self.display,(255,255,245),(self.canvas))
        pygame.draw.rect(self.display,(230,230,220),(self.chatbox))

        while self.run == True:
            
            ##self.fpga.send(timeratio) (no longer needed)
            self.frame_counter+=1
            if (self.frame_counter % self.fps): #counts number of seconds player is drawing using the frame rate of the game
                self.draw_timer+=1
            if self.draw_timer == 1:
                self.music_change()
            self.events = pygame.event.get()

            self.clock.tick(self.fps)
            self.brush_size = 5
            self.colour_update()
            self.switch_update()

            xy = pygame.mouse.get_pos()
            #if (((self.centre[0]-self.canvas_width/2)<xy[0]>(self.centre[0]+self.canvas_width/2)) or ((self.centre[1]-self.canvas_height/2)<xy[1]>(self.centre[1]+self.canvas_height/2))):
            


             # returns true if mouse is being held down which enables draw
            

            collide = self.canvas.collidepoint(xy)
            chat_collide = self.chatbox.collidepoint(xy)
            if collide==False:
                self.draw_blit = False
                if chat_collide:
                    self.mouse_down(False)
            else:
                self.mouse_down(True)
            
            if self.draw_blit:
                pygame.draw.circle(self.display,(self.brush_colour),(xy[0],xy[1]),10)
            
            if self.is_typing == True:
                self.typing()
            

            #self.display.blit(self.canvas)
            #pygame.draw(self.display, (255,255,255), canvas)
            pygame.display.update()
            for event in self.events:
                if event.type == pygame.QUIT:
                    run = False
                    ##self.fpga.send("E 0 0")
                    pygame.quit()

    def load_sprites(self):
        None