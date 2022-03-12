from _thread import *
import pygame
import random
import threading
class Textbox(pygame.sprite.Sprite):
  def __init__(self,message):
    pygame.sprite.Sprite.__init__(self)
    self.text = ""
    self.font = pygame.font.Font("Game/assets/pencil.TTF", 20)
    self.black = (0,0,0)
    self.white = (255,255,255)
    self.message = self.font.render(message, False, self.black)
    self.rect = self.message.get_rect()
    self.received_messages = []

    self.upper_case = False
    self.validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./" #valid character filter to prevent priting buttons like 'Return'
    self.shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

  def add_chr(self, char):
    if char in self.validChars and not self.upper_case:
      self.text += char
    elif char in self.validChars and self.upper_case:
        self.text += self.shiftChars[self.validChars.index(char)]
    self.update()
    

  def update(self):
    old_rect_pos = self.rect.center
    self.message = self.font.render(self.text, False, self.black)
    self.rect = self.message.get_rect()
    self.rect.center = old_rect_pos
class Game():
    def __init__(self,username, FPGAinstance=None, clientInstance=None):
        self.FPGA = FPGAinstance
        self.Client = clientInstance
        pygame.init()
        self.run = False
        self.round_end = False
        self.game_end = False
        self.username = username
        self.width = 1200
        self.height = 600
        self.display = pygame.display.set_mode((self.width, self.height))

        self.canvas_width = int(self.width/1.6)
        self.canvas_height = int(self.height/1.3)
        self.canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.centre = (self.width/2,self.height/2)

        self.colours = {"black": (0, 0, 0), "white": (255, 255, 255)}

        self.clock = pygame.time.Clock()
        self.fps = 30#800

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


        self.chatbox = pygame.Rect(self.width/5,self.height/2,self.canvas_width/2.3,self.canvas_height)
        self.is_typing = False
        self.messages = []
        self.received_msgs = []
        self.msg_limit = 13
        self.max_char_len = 26


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
            '''
            if draw == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #return True
                    self.draw_blit = True
                    print("DOWN")
                elif event.type == pygame.MOUSEBUTTONUP:
                    #return False
                    self.draw_blit = False
                    print("UP")'''

            #if event.type == pygame.MOUSEBUTTONDOWN:
                #print("TYPING")
               # self.is_typing = True
               # self.typing()
                #else:
                    #self.is_typing = False
                    #print("NOOOOO")
    
    def msg_limiter(self):
        if len(self.received_msgs)>=self.msg_limit:
            self.received_msgs.pop(0)
    
    def redraw_chat(self):
        pygame.draw.rect(self.display,(245,245,240),(self.chatbox))

    def refresh_textbox(self,textbox):
        self.msg_limiter()
        self.redraw_chat()
        self.display.blit(textbox.message, textbox.rect)
        for i in range (len(self.received_msgs)):
            textbox = Textbox(self.received_msgs[i])
            textbox.rect.center = (1030,100+(30*i))
            self.display.blit(textbox.message, textbox.rect)

    def addtext(self,textbox):
        if len(textbox.text)<self.max_char_len:
            textbox.text += " "
            textbox.update()
        else:
            print("Text too long")
        return textbox


    def typing(self):
        textbox = Textbox("Type to chat")
        textbox.upper_case = False
        textbox.rect.center = (1030,500)
        clock = pygame.time.Clock()
        self.chatbox.center = (self.width/1.18,self.height/2)
        self.redraw_chat()
        #self.refresh_textbox(textbox)
        
        while True:
            clock.tick(30)
            #pygame.display.flip()
            
            self.refresh_textbox(textbox)
            #self.display.blit(textbox.message, textbox.rect)
            for e in self.events:
                if e.type == pygame.QUIT:
                    self.run = False
                if e.type == pygame.KEYUP:
                    if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        textbox.upper_case = False
                if e.type == pygame.KEYDOWN:
                    if len(self.username+textbox.text)<26:
                        print("Draw")
                        self.redraw_chat()
                        textbox.add_chr(pygame.key.name(e.key))
                        if e.key == pygame.K_SPACE:
                            if len(textbox.text)<20:
                                textbox.text += " "
                                textbox.update()
                            else:
                                print("Text too long")
                        if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                            textbox.upper_case = True
                        if e.key == pygame.K_BACKSPACE:
                            textbox.text = textbox.text[:-1]
                            textbox.update()
                    if e.key == pygame.K_RETURN:
                        if len(textbox.text) > 0:
                            pygame.display.update(textbox.rect)
                            self.messages.append(textbox.text)
                            self.received_msgs.append((self.username+":  "+textbox.text))
                            print(self.messages)
                            textbox = Textbox("Type to chat")
                            textbox.rect.center = (1030,500)
                            
                            self.refresh_textbox(textbox)

    def random_draw(self):
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)
        self.draw_blit = True
        return (self.x,self.y)

    def round_start(self):
        self.run = True
        #pygame.mixer.music.play(-1)
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
        self.redraw_window()
        self.display.blit(self.background,(0,0))

        #canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.canvas.center = (self.width/2.7,self.height/2)
        
        pygame.draw.rect(self.display,(255,255,245),(self.canvas))


        self.drawThread = threading.Thread(target=self.typing, daemon=True)
        self.drawThread.start()

        while self.run == True:

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

            xy = self.random_draw()#pygame.mouse.get_pos()
            #if (((self.centre[0]-self.canvas_width/2)<xy[0]>(self.centre[0]+self.canvas_width/2)) or ((self.centre[1]-self.canvas_height/2)<xy[1]>(self.centre[1]+self.canvas_height/2))):

             # returns true if mouse is being held down which enables draw

            canvas_collide = self.canvas.collidepoint(pygame.mouse.get_pos())
            chat_collide = self.chatbox.collidepoint(pygame.mouse.get_pos())
            #if canvas_collide==False:
                #self.draw_blit = False

            #else:
                #self.mouse_down(True)
            if chat_collide:
                self.mouse_down(False)

            self.draw_blit = True
            if self.draw_blit:
                pygame.draw.circle(self.display,(self.brush_colour),(xy[0],xy[1]),10)

            if self.is_typing == True:
                self.typing()

            #self.display.blit(self.canvas)
            #pygame.draw(self.display, (255,255,255), canvas)
            pygame.display.update()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()

    def load_sprites(self):
        None

if __name__ == "__main__":
    GameTest = Game("test")
    GameTest.round_start()