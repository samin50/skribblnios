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
        pygame.init()
        self.font = pygame.font.Font("Game/assets/pencil.TTF", 20)
        self.FPGA = FPGAinstance
        self.Client = clientInstance
        
        self.run = False
        self.round_end = False
        self.game_end = False
        self.username = username
        self.width = 1200
        self.height = 700
        self.display = pygame.display.set_mode((self.width, self.height))
        self.cursor = pygame.image.load("Game/assets/cursor.png")
        self.cursor.convert()
        self.cursorRect = self.cursor.get_rect()

        #self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.xy = (0,0)

#canvas:
        self.canvas_width = int(self.width/1.6)
        self.canvas_height = int(self.height/1.3)
        self.canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.centre = (self.width/2,self.height/2)
        self.canvas.center = (self.width/2.7,self.height/2)

        self.clock = pygame.time.Clock()
        self.fps = 200
        self.colour_string = ""
        self.timer = 200
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.brush_size = 20
        self.game_music = pygame.mixer.music.load("Game/assets/menu_music.mp3")
        self.draw_timer = 0
        self.frame_counter = 0

#colours:
        self.colour_list = {"black": (0, 0, 0), "white": (255, 255, 255)}
        self.colours= [[0,0,0],[0,0,0],[0,0,0]] # 3-bit binary value representing colour switch state
        #each bit represents the rgb value 64
        
        self.brush_colour = self.colour_list["black"]
        self.colour_change = False
        self.draw_blit = False
        self.erase = False

#switches:
        self.switches = [1,1,0,0,0,0,0,1,1]
        self.switch_size = (40,70)
        self.off_switch = [
            (pygame.image.load("Game/assets/switches/1.png")),(pygame.image.load("Game/assets/switches/2.png")),
            (pygame.image.load("Game/assets/switches/3.png")), (pygame.image.load("Game/assets/switches/7.png")),
            (pygame.image.load("Game/assets/switches/8.png")), (pygame.image.load("Game/assets/switches/9.png")),
            (pygame.image.load("Game/assets/switches/13.png")), (pygame.image.load("Game/assets/switches/14.png")),
            (pygame.image.load("Game/assets/switches/15.png"))
        ]


        self.on_switch= [
            (pygame.image.load("Game/assets/switches/4.png")),(pygame.image.load("Game/assets/switches/5.png")),
            (pygame.image.load("Game/assets/switches/6.png")), (pygame.image.load("Game/assets/switches/10.png")),
            (pygame.image.load("Game/assets/switches/11.png")), (pygame.image.load("Game/assets/switches/12.png")),
            (pygame.image.load("Game/assets/switches/16.png")), (pygame.image.load("Game/assets/switches/17.png")),
            (pygame.image.load("Game/assets/switches/18.png")) 
        ]

#chatbox:
        self.chatbox = pygame.Rect(self.width/5,self.height/2,self.canvas_width/2.3,self.canvas_height)
        self.messages = []
        self.received_msgs = []
        self.msg_limit = 13
        self.max_char_len = 26
    
    def mouseTracker(self):
        while self.FPGA is None:
            mousePos = pygame.mouse.get_pos()
            self.draw_check(mousePos[0], mousePos[1])
    
    def size_update(self, is_increasing):
        if self.brush_size>=1:
            if is_increasing:
                self.brush_size+=2
            else:
                self.brush_size-=2


    def switch_update(self,switches):
        temp =([int(i) for i in switches])
        self.switches = temp[:8]


    def switch_img_scale(self):
        for i in range(9):
            self.off_switch[i] = pygame.transform.scale(self.off_switch[i],(self.switch_size))
            self.on_switch[i] = pygame.transform.scale(self.on_switch[i],(self.switch_size))
    
    def disp_switches(self):
        for i in range (9):
            if self.switches[i]:
                self.display.blit(self.on_switch[i],(i*70+100,self.height-5-self.switch_size[1]))
            else:
                self.display.blit(self.off_switch[i],(i*70+100,self.height-5-self.switch_size[1]))

    def redraw_window(self):
        self.display.fill(self.colour_list["white"])

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
        self.colours[0] =self.switches[:3]
        self.colours[1] =self.switches[3:6]
        self.colours[2] =self.switches[6:9]
        self.brush_colour = ((self.blti(self.colours[0])<<5),(self.blti(self.colours[1])<<5),(self.blti(self.colours[2])<<5)) #RGB
    def switch_update(self):
        for i in range(len(self.colours)):
            for j in range(len(self.colours[i])):
                self.colours[i][j] = random.randint(0,1)
    """REDUNDANT
    def mouse_down(self,draw):
        self.xy = pygame.mouse.get_pos()
        if draw == True:
            for event in self.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.draw_blit = True
                elif event.type == pygame.KEYUP:
                    self.draw_blit = False
                        
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.draw_blit = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.draw_blit = False
    """
    
    def msg_limiter(self):
        if len(self.received_msgs)>=self.msg_limit:
            self.received_msgs.pop(0)
    
    def redraw_chat(self,textbox):
        pygame.draw.rect(self.display,(245,245,240),(self.chatbox))
        self.display.blit(textbox.message, textbox.rect)

    def refresh_textbox(self):
        self.msg_limiter()
        for i in range (len(self.received_msgs)):
            #pygame.display.blit
            text_surface = self.font.render(self.received_msgs[i],False,(0, 0, 0))
            self.display.blit(text_surface, dest=(self.width-300,100+(30*i)))
            #textbox = Textbox(self.received_msgs[i])
            #textbox.rect.center = (self.width-170,100+(30*i))
            #self.display.blit(textbox.message, textbox.rect)

    def addtext(self,textbox):
        if len(textbox.text)<self.max_char_len:
            textbox.text += " "
            textbox.update()
        else:
            print("Text too long")
        return textbox


    def typing(self):
        pygame.init()
        chat_clock = pygame.time.Clock()
        textbox = Textbox("Type to chat")
        textbox.upper_case = False
        textbox.rect.center = (self.width-170,self.height-100)
        self.chatbox.center = (self.width/1.18,self.height/2)
        self.redraw_chat(textbox)
        while True:
            chat_clock.tick(self.fps)
            self.refresh_textbox()
            if not self.chatbox.collidepoint(pygame.mouse.get_pos()):
                continue
            for event in self.events:
                self.redraw_chat(textbox)
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        textbox.upper_case = False
                if event.type == pygame.KEYDOWN:
                    if len(self.username+textbox.text)<26:
                        self.redraw_chat(textbox)
                        textbox.add_chr(pygame.key.name(event.key))
                        if event.key == pygame.K_SPACE:
                            if len(textbox.text)<20:
                                textbox.text += " "
                                textbox.update()
                            else:
                                print("Text too long")
                        if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                            textbox.upper_case = True
                        if event.key == pygame.K_BACKSPACE:
                            textbox.text = textbox.text[:-1]
                            textbox.update()
                    if event.key == pygame.K_RETURN:
                        if len(textbox.text) > 0:
                            pygame.display.update(textbox.rect)
                            self.messages.append(textbox.text)
                            self.received_msgs.append((self.username+":  "+textbox.text))
                            print(self.messages)
                            textbox = Textbox("Type to chat")
                            textbox.rect.center = (self.width-170,self.height-100)
                            self.refresh_textbox()
                    if event.type == pygame.QUIT:
                        pygame.quit()



    def random_draw(self):
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)
        self.draw_blit = True
        return (self.x,self.y)

    def draw_check(self, x, y, useFPGA=False):
        FACTOR = 6.6
        print(x, y)
        if not self.draw_blit:
            print("cant' draw")
            return
        # Add offsets for coordinates
        if useFPGA:
            #Bound angles
            if abs(x) > 25 or abs(y) > 35:
                return
            x+=self.width//2.7*FACTOR
            y+=self.height//2*FACTOR
        else:
            print("Coords:", x, y)
        # returns true if coordinates are within the canvas
        canvas_collide = self.canvas.collidepoint((x,y))

        if canvas_collide==True:
            print("should_print")
            pygame.draw.circle(self.display,(self.brush_colour),(int(x),int(y)),5)

        #if self.draw_blit:
            #self.draw(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

    def draw(self,x,y):

        #xy = pygame.mouse.get_pos()
        pygame.draw.circle(self.display,(self.brush_colour),(x,y),5)
        #pygame.draw.rect(self.display,(self.brush_colour),pygame.Rect(xy[0],xy[1],5,5))


    def round_start(self):
        self.run = True
        self.redraw_window()
        #pygame.mixer.music.play(-1)
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
        self.display.blit(self.background,(0,0))
#switches:
        self.switch_img_scale()
        #self. display.blit(self.off_switch[0],(0,0))
        
        pygame.draw.rect(self.display,(255,255,245),(self.canvas))
        
        chat_thread = threading.Thread(target=self.typing, daemon=True) #daemon thread so it will terminate when master thread quits
        chat_thread.start() #starts a new thread for the chat window
        
        #start_new_thread(self.typing,(self.display,)) old threading function - outdated
        #Mouse thread 
        self.mouseThread = threading.Thread(target=self.mouseTracker, daemon=True)
        self.mouseThread.start()
        while self.run == True:
            self.events = pygame.event.get()

            self.frame_counter+=1
            if (self.frame_counter % self.fps): #counts number of seconds player is drawing using the frame rate of the game
                self.draw_timer+=1
            if self.draw_timer == 1:
                self.music_change()

            self.disp_switches()
            self.clock.tick(self.fps)
            self.brush_size = 5
            self.colour_update()
            #self.switch_update()

            #self.random_draw()
            #if (((self.centre[0]-self.canvas_width/2)<xy[0]>(self.centre[0]+self.canvas_width/2)) or ((self.centre[1]-self.canvas_height/2)<xy[1]>(self.centre[1]+self.canvas_height/2))):

             # returns true if mouse is being held down which enables draw



            #self.display.blit(self.canvas)
            #pygame.draw(self.display, (255,255,255), canvas)
            pygame.display.update()

            for event in self.events:
                if event.type == pygame.QUIT:
                    print("quit")
                    self.run = False
                    pygame.quit()
                #Mouse usage only
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.draw_blit = True
                if event.type == pygame.KEYUP:
                    self.draw_blit = False

    def load_sprites(self):
        None

if __name__ == "__main__":
    GameTest = Game("test")
    GameTest.round_start()
