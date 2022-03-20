import pygame
import random
import threading
import time  

class Textbox(pygame.sprite.Sprite):
  def __init__(self,message):
    pygame.sprite.Sprite.__init__(self)
    self.text = ""
    self.font = pygame.font.Font("Game/assets/Gameplay.TTF", 15)
    self.smallfont = pygame.font.Font("Game/assets/Gameplay.TTF", 13) #Shan: you need to make this the smaller font of the IP port no etc
    
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
    self.rect = pygame.Rect(600,600,100,26)
    self.rect.center = old_rect_pos
class Game():
    def __init__(self,username, FPGAinstance=None, clientInstance=None, avatar=0):
        pygame.init()
        #Username, avatar, score, position
        self.players = [[username, avatar, 0, 0], ["twat", 3, 53, 0]]
        self.font = pygame.font.Font("Game/assets/Gameplay.TTF", 12)
        self.large_font =  pygame.font.Font("Game/assets/Gameplay.TTF", 16)
        self.paint_font = pygame.font.Font("Game/assets/paint.TTF", 35)
        self.FPGA = FPGAinstance
        self.Client = clientInstance
        self.username = username
        self.sendServer("!SETNAME " + username + " " + str(avatar), False)
        self.drawPoints = [(None, None), (None, None), 0]
        pygame.init()
        self.run = False
        self.round_not_started = True
        self.round_end = False
        self.game_end = False
        self.width = 1400
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((self.width, self.height))
        self.pointer = pygame.image.load("Game/assets/cursor.png")
        self.pointer_pos =(359, 190)

        self.words = []
        self.word_choice = []
        self.word = ""

        self.score = 0
        #self.pointer.convert()
        #self.pointerRect = self.pointer.get_rect()
        #self.pointer_img = pygame.image.load("Game/assets/cursor.png")
        self.pointer = pygame.transform.scale(self.pointer, (20, 20))
        self.FPGAX = 0
        self.FPGAY = 0

        #self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.xy = (0,0)
        #self.mouseSurface = pygame.Surface((self.height. self.width))

        self.pointer_surface = pygame.surface.Surface((self.width,self.height))

#canvas:
        self.canvas_width = int(self.width/1.6)
        self.canvas_height = int(self.height/1.3)
        self.canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.centre = (self.width/2,self.height/2)
        self.canvas.center = (self.width/2.6,self.height/2)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.colour_string = ""
        self.background = pygame.image.load("Game/assets/sky_background.png")
        self.brush_size = 5
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
        self.time_limit = 20
        self.time = self.time_limit
        self.timer_img = pygame.transform.scale(pygame.image.load("Game/assets/timer.png"),(250,100))
        self.timer_img =pygame.image.load("Game/assets/timer.png")
#switches:
        self.switches = [0,0,0,0,0,0,0,0,0,0]
        self.switch_size = (40,70)
        self.reset_size = (50,60)
        self.off_switch = [
            (pygame.image.load("Game/assets/switches/1.png")),(pygame.image.load("Game/assets/switches/14.png")),
            (pygame.image.load("Game/assets/switches/15.png")), (pygame.image.load("Game/assets/switches/7.png")),
            (pygame.image.load("Game/assets/switches/8.png")), (pygame.image.load("Game/assets/switches/9.png")),
            (pygame.image.load("Game/assets/switches/13.png")), (pygame.image.load("Game/assets/switches/2.png")),
            (pygame.image.load("Game/assets/switches/3.png")),(pygame.image.load("Game/assets/switches/19.png"))
        ]


        self.on_switch= [
            (pygame.image.load("Game/assets/switches/4.png")),(pygame.image.load("Game/assets/switches/5.png")),
            (pygame.image.load("Game/assets/switches/6.png")), (pygame.image.load("Game/assets/switches/10.png")),
            (pygame.image.load("Game/assets/switches/11.png")), (pygame.image.load("Game/assets/switches/12.png")),
            (pygame.image.load("Game/assets/switches/16.png")), (pygame.image.load("Game/assets/switches/17.png")),
            (pygame.image.load("Game/assets/switches/18.png")), (pygame.image.load("Game/assets/switches/20.png")) 
        ]

        #self.reset_button = pygame.transform.scale(pygame.image.load("Game/assets/reset.png"),(self.reset_size))
        self.reset_button = pygame.image.load("Game/assets/reset.png")

  

#avatars:
        self.avatar = 7
        self.avatar_list = [
            pygame.image.load("Game/assets/avatars/1.png"),
            pygame.image.load("Game/assets/avatars/2.png"),
            pygame.image.load("Game/assets/avatars/3.png"),
            pygame.image.load("Game/assets/avatars/4.png"),
            pygame.image.load("Game/assets/avatars/5.png"),
            pygame.image.load("Game/assets/avatars/6.png"),
            pygame.image.load("Game/assets/avatars/7.png"),
            pygame.image.load("Game/assets/avatars/8.png")
            ]

        self.lobby_background = []

#chatbox:
        self.chatbox = pygame.Rect(self.width/5,self.height/2,self.canvas_width/2.3,self.canvas_height)
        self.received_msgs = []
        self.msg_limit = 17
        self.max_char_len = 32

        self.window_pos = (360,160)
        self.avatar_scale()
        self.load_backgrounds()
    
    def addPlayer(self, playerName, avatar):
        self.players.append([playerName, int(avatar), 0, 0])
    
    def cursor(self):
        self.screen.blit(self.display, (0, 0))

#***METHODS***#

    def word_reveal(self,timeratio):
        timeratio = 0.3  #will receive value
        space = self.word(" ")

        wordlength = len(self.word)
        wordtoguessarray = ['_']
        for x in range(wordlength-1):
            wordtoguessarray.insert(1,'_')
        if space != -1:
            wordtoguessarray[space] = " "

        if timeratio == 0.45:
            y = random.randint(0,wordlength-1)
            while y == space:
                y = random.randint(0,wordlength-1)
            z = self.word[y]
            wordtoguessarray[y] = z


        if timeratio == 0.7 and wordlength > 3 :
            w = random.randint(0,wordlength-1)
            while w == y or w == space:
                w = random.randint(0,wordlength-1)
            z = self.word[w]
            wordtoguessarray[w] = z


#Words from text file
    def getword(self):
        with open('Game/assets/words.txt') as words:
            self.words = words.read().splitlines()

    #chose_word
    def choose_word(self):
        self.words_chosen = []
        while len(self.words_chosen)<3:
            word = random.choice(self.words)
            if word not in self.words_chosen:
                self.words_chosen.append(word)

    def display_word_choices(self):
        for i in range(len(self.words_chosen)):
            self.events = pygame.event.get()
            #print(self.words_chosen)
            word = self.large_font.render(self.words_chosen[i], True, (100,150,255))
            word_rect = word.get_rect(x =(self.width/2-200)+(i*150),y =(self.height/2+180))
            self.display.blit(word,word_rect)  
            self.word_collision(word,word_rect,i)
    
    def word_collision(self,word,word_rect,index):

        word0 = self.large_font.render(self.words_chosen[0], True, (100,150,255))
        word0_rect = word.get_rect(x =(self.width/2-200)+(0*150),y =(self.height/2+180))
        word1 = self.large_font.render(self.words_chosen[1], True, (100,150,255))
        word1_rect = word.get_rect(x =(self.width/2-200)+(1*150),y =(self.height/2+180))
        word2 = self.large_font.render(self.words_chosen[2], True, (100,150,255))
        word2_rect = word.get_rect(x =(self.width/2-200)+(2*150),y =(self.height/2+180))

        mouse  = pygame.mouse.get_pos()
        #pygame.draw.rect(self.display,(255,255,255),word_rect)
        for event in self.events:

            if word0_rect.collidepoint(mouse[0],mouse[1]) and event.type == pygame.MOUSEBUTTONDOWN:
                self.word = self.words_chosen[0]
                self.round_not_started = False
            if word1_rect.collidepoint(mouse[0],mouse[1]) and event.type == pygame.MOUSEBUTTONDOWN:
                self.word = self.words_chosen[1]
                self.round_not_started = False
            if word2_rect.collidepoint(mouse[0],mouse[1]) and event.type == pygame.MOUSEBUTTONDOWN:
                self.word = self.words_chosen[2]
                self.round_not_started = False
                '''for event in self.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.word = self.words_chosen[index]
                        self.round_not_started = False
                        self.sendServer("SERVERCMD: !STARTROUND " + self.word)'''
            if event.type == pygame.QUIT:
                pygame.quit()
            #

#mousetracker:    
    def mouseTracker(self):
        mousePos = pygame.mouse.get_pos()
        self.screen.blit(self.display, (0,0))
        if self.FPGA is None:
            self.screen.blit(self.pointer, (mousePos[0]-10, mousePos[1]-10))
            self.draw_check(mousePos[0], mousePos[1])
        else:
            self.screen.blit(self.pointer, (self.FPGAX-10, self.FPGAY-10))
        self.switch_collisions(mousePos)

#countdown timer:
    def timer(self):
        while True:
            self.time= self.time_limit
            while self.time or self.round_not_started == False:
                mins, secs = divmod(self.time, 60)
                self.round_time = secs
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                self.time -= 1
                if self.time <= 0:
                    self.round_not_started = True
                    #self.run = False
#Display timer
    def display_timer(self):
        self.display.blit(self.timer_img,(8,10))
        timer_disp = self.paint_font.render(str(self.time),True,(255,255,255))
        self.display.blit(timer_disp,(37,60))
        #timer_rect = pygame.Rect(10,10,100,100)
        #pygame.draw.rect(self.display,(random.randint(0,255),0,0),timer_rect)
        pygame.display.update()

#update brush size

    def size_update(self, is_increasing):
        print("Brush size:", self.brush_size)
        if is_increasing:
            self.brush_size+=2
        else:
            if self.brush_size>=3: 
                self.brush_size-=2
        print("New size:", self.brush_size)

#scaling avatars:
    def avatar_scale(self):
        for i in range(len(self.avatar_list)):
            self.avatar_list[i] = pygame.transform.scale(self.avatar_list[i],((85,115)))

#scaling switch sizes on screen
    def switch_img_scale(self):
        for i in range(len(self.off_switch)):
            self.off_switch[i] = pygame.transform.scale(self.off_switch[i],(self.switch_size))
            self.on_switch[i] = pygame.transform.scale(self.on_switch[i],(self.switch_size))


    def redraw_window(self):
        self.display.fill(self.colour_list["white"])

    '''def return_xy(self):
        x = random.randint(0,self.width+100)
        y = random.randint(0, self.height+100)
        xy =(x,y)
        return xy'''
#updates music:

    def music_change(self):
        pygame.mixer.music.stop()
        self.game_music = pygame.mixer.music.load("Game/assets/drawing_music.mp3")
        pygame.mixer.music.play(-1)

#binary list to int convertor:

    def blti(self,binlist): #binary list to int
        return int(''.join(map(str, binlist)), 2)
#checks and updates switch state:        

    def switch_update(self, switchesNew, override=False):

        #Only drawers can update switch if connected to server
        if self.Client is not None:
            if not (self.Client.isDrawing() or override):
                return
        switches = str(bin(int(switchesNew)))[2:].zfill(10)
        tempSwitch = [int(i) for i in switches]
        if (tempSwitch == self.switches) and self.FPGA is not None:
            return
        #Update to server any changes
        self.sendServer("SERVERCMD: !SETSWITCH " + str(switchesNew), True)
        self.switches = tempSwitch
        self.colours[0] = self.blti(self.switches[0:3])*32
        self.colours[1] = self.blti(self.switches[3:6])*32
        self.colours[2] = self.blti(self.switches[6:9])*32
        print("New colours:", self.colours)
        if self.switches[9] == 0:
            self.brush_colour = (self.colours[0],self.colours[1],self.colours[2]) #RGB
        else: #Eraser mode
            self.brush_colour = self.colour_list["white"]
        self.renderSwitch()

#displays switches
    def renderSwitch(self):
        self.display.blit(self.reset_button,(10*70+100,self.height-5-self.switch_size[1]))
        for i in range (len(self.off_switch)):
            if self.switches[i] and self.switches[9] == 0:
                self.display.blit(self.on_switch[i],(i*70+100,self.height-5-self.switch_size[1]))
            else:
                self.display.blit(self.off_switch[i],(i*70+100,self.height-5-self.switch_size[1]))

        if self.switches[9]:
            self.display.blit(self.on_switch[9],(9*70+100,self.height-5-self.switch_size[1]))
        else:
            self.display.blit(self.off_switch[9],(9*70+100,self.height-5-self.switch_size[1])) 

#lobby screen
    def startRound(self):
        self.round_not_started = False

    def wait_screen(self):
        self.events = pygame.event.get()
        self.getword()
        self.choose_word()
        #pygame.clock.clock
        count = 1
        self.display.fill((255,255,255))
        while self.round_not_started:
            
            pygame.time.Clock().tick(6)
            if count>5:
                count = 0
            else:
                count += 1
            self.display.blit(self.lobby_background[count],(0,0))
            #start_rect  = pygame.Rect(200,413,210,50)
            pygame.draw.rect(self.display,(0,0,0),(self.width/2-75,self.height-100,150,40),2)
            for user in range(len(self.players)):
                username = self.large_font.render(self.players[user][0], True, (255,255,255))
                avatar = (self.avatar_list[self.players[user][1]]).convert()
                score = self.large_font.render("Score: "+str(self.players[user][2]), True, (255,255,255))
                self.display.blit(avatar,((self.width/2-500)+user*200,self.height/2-130))
                self.display.blit(username,((self.width/2-500)+user*200,self.height/2+20))
                self.display.blit(score,((self.width/2-500)+user*200,self.height/2+50))
                if self.Client is not None:
                    if self.Client.isDrawing():
                        self.display_word_choices()
                        
                else:
                    self.display_word_choices()
                    
            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
        self.round_start()

# lobby screen background
    def load_backgrounds(self):
        for i in range(7):
            dir = f"Game/assets/lobby_background/{i}.gif"
            img = pygame.image.load(dir)
            img = pygame.transform.scale(img,(self.width,self.height))
            self.lobby_background.append(img)     

#resets the canvas
    def reset_canvas(self, override=False):
        if self.Client is not None:
            if not (self.Client.isDrawing() or override):
                return
        pygame.draw.rect(self.display,(255,255,255),(self.canvas))
        pygame.draw.rect(self.display,(0,0,0),(self.canvas),3)

#checks if switches have been clicked:
    def switch_collisions(self,mouse_pos):
        reset_rect = self.reset_button.get_rect() #reset button rect
        reset_rect.x = 10*70+100
        reset_rect.y = self.height-5-self.switch_size[1]

        #reset_rect.center = (9*70+100,self.height-5-self.switch_size[1])
        #pygame.draw.rect(self.display,(0,0,0),reset_rect)
        if (self.Client is not None):
            if not self.Client.isDrawing():
                return
        if reset_rect.collidepoint(mouse_pos):
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                        self.sendServer("!SERVERCMD: !CLEAR", True)
                        self.reset_canvas(True)

        switch_rect = self.off_switch[0].get_rect()
        for i in range(len(self.off_switch)):
            number =  0
            #switch_rect.center = (i*70+100,self.height-5-self.switch_size[1])
            switch_rect.x =i*70+100
            switch_rect.y =self.height-5-self.switch_size[1]
            #pygame.draw.rect(self.display,(0,0,0),switch_rect)
            collide = switch_rect.collidepoint(mouse_pos)
            if collide:
                for event in self.events:
                    if event.type ==pygame.MOUSEBUTTONDOWN:
                        temp_switch = self.switches
                        if temp_switch[i] == 0:
                            temp_switch[i] = 1
                        else:
                            temp_switch[i] = 0

                        number = int("".join(str(i) for i in temp_switch), base=2)
                        self.switch_update(number)
                        return

#limits message length to fit into textbox 
     
    def msg_limiter(self):
        if len(self.received_msgs)>=self.msg_limit:
            self.received_msgs.pop(0)

#drawing chatbox    

    def redraw_chat(self,textbox):
        pygame.draw.rect(self.display,(204,255,204),(self.chatbox))
        pygame.draw.rect(self.display,(0,0,0),(self.chatbox),3)
        self.display.blit(textbox.message, textbox.rect)

#refreshig main chatbox

    def refresh_textbox(self):
        self.msg_limiter()
        for i in range (len(self.received_msgs)):
            #pygame.display.blit
            text_surface = self.font.render(self.received_msgs[i],False,(0, 0, 0))
            self.display.blit(text_surface, dest=(self.width-300,100+(30*i)))
            #textbox = Textbox(self.received_msgs[i])
            #textbox.rect.center = (self.width-170,100+(30*i))
            #self.display.blit(textbox.message, textbox.rect)

    '''def addtext(self,textbox):
        if len(textbox.text)<self.max_char_len:
            textbox.text += " "
            textbox.update()
        else:
            print("Text too long")
        return textbox'''
#adding messages to list  
    def addOtherMessages(self, text):
        print("added message")
        self.received_msgs.append(text)

#typing
    def typing(self):
        pygame.init()
        chat_clock = pygame.time.Clock()
        textbox = Textbox("Type to chat")
        textbox.upper_case = False
        textbox.rect.center = (self.width-260,self.height-100)
        self.chatbox.center = (self.width/1.18,self.height/2)
        self.redraw_chat(textbox)
        while True:
            chat_clock.tick(self.fps)
            self.refresh_textbox()
            if not self.chatbox.collidepoint(pygame.mouse.get_pos()):
                continue
            for event in self.events:
                
                if event.type == pygame.KEYUP:
                    self.redraw_chat(textbox)
                    if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        textbox.upper_case = False
                if event.type == pygame.KEYDOWN:
                    self.redraw_chat(textbox)
                    if event.key == pygame.K_BACKSPACE:
                        textbox.text = textbox.text[:-1]
                        textbox.update()
                    if len(self.username+textbox.text)<self.max_char_len:
                        #self.redraw_chat(textbox)
                        textbox.add_chr(pygame.key.name(event.key))
                        if event.key == pygame.K_SPACE:
                            #if len(textbox.text)<self.max_char_len:
                            textbox.text += " "
                            textbox.update()
                            #else:
                                #print("Text too long")
                        if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                            textbox.upper_case = True
                        
                    if event.key == pygame.K_RETURN:
                        if len(textbox.text) > 0:
                            pygame.display.update(textbox.rect)
                            self.received_msgs.append((self.username+":  "+textbox.text))
                            self.sendServer("SERVERCMD: !BROADCAST "+ self.username + ": " + textbox.text)
                            textbox = Textbox("Type to chat")
                            textbox.rect.center = (self.width-170,self.height-100)
                            self.refresh_textbox()
                    if event.type == pygame.QUIT:
                        pygame.quit()


    '''
    def random_draw(self):
        self.x = random.randint(0,500)
        self.y = random.randint(0,500)
        self.draw_blit = True
        return (self.x,self.y)'''

    def draw_check(self, x, y, useFPGA=False):
        #self.pointer_update(x,y)
        FACTOR = 6.6
        if useFPGA:
            #Bound angles
            if abs(x) > 35 or abs(y) > 25:
                return
            x =(FACTOR*x)+self.width//2.7
            y =(FACTOR*y)+self.height//2
            self.FPGAX = x
            self.FPGAY = y
        if not self.draw_blit:
            return
        # Add offsets for coordinates
            #self.pointer_update(x,y)
        #print("Coords:", x, y)
        # returns true if coordinates are within the canvas
        canvas_collide = self.canvas.collidepoint((x,y))

        if canvas_collide==True:
            self.draw(x,y)

    def draw(self,x,y, override=False):
        #Only drawers can update switch if connected to server
        if self.Client is not None:
            if not (self.Client.isDrawing() or override):
                return
        #Aryan send coordinates here
        Pointer = self.drawPoints[2]
        self.drawPoints[Pointer] = (x, y)
        if self.drawPoints[not Pointer] != (None, None):
             pygame.draw.line(self.display,(self.brush_colour),self.drawPoints[Pointer],self.drawPoints[not Pointer], self.brush_size*2)
        self.drawPoints[2] = not self.drawPoints[2] #Invert pointer
        #xy = pygame.mouse.get_pos()
        if override == False:
            self.sendServer("SERVERCMD: !DRW " +str(x) + " " + str(y), True) #Send data to server
        pygame.draw.circle(self.display,(self.brush_colour),(x,y),self.brush_size)

        #pygame.draw.rect(self.display,(self.brush_colour),pygame.Rect(xy[0],xy[1],5,5))


    def round_start(self):
        self.time = self.time_limit
        self.run = True
        self.redraw_window()
        #pygame.mixer.music.play(-1)
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
        #self.display.blit(self.lobby_background[0],(0,0))
        self.display.blit(self.background,(0,0))
        
#switches:
        self.switch_img_scale()
        #self. display.blit(self.off_switch[0],(0,0))
        self.reset_canvas(True)
        #pygame.draw.rect(self.display,(255,255,255),(self.canvas))
        
        chat_thread = threading.Thread(target=self.typing, daemon=True) #daemon thread so it will terminate when master thread quits
        chat_thread.start() #starts a new thread for the chat window
        
        #start_new_thread(self.typing,(self.display,)) old threading function - outdated
        #Mouse thread 
        #self.mouseThread = threading.Thread(target=self.mouseTracker, daemon=True)
        #self.mouseThread.start()
        self.renderSwitch()
        while self.run:
            self.display_timer()

            pygame.draw.rect(self.display,self.brush_colour,(30,self.height-67,30,60)) #pallet preview
            pygame.draw.rect(self.display,(0,0,0),(30,self.height-67,30,60),2)
            #pygame.draw.circle(self.display, self.brush_colour,(30,30), 30, 15)
            #pygame.draw.circle(self.display, (0,0,0),(30,30), 15, 2)
            #pygame.draw.circle(self.display, (0,0,0),(30,30), 30, 2)
            self.events = pygame.event.get()
            
            self.mouseTracker()
            self.frame_counter+=1
            if (self.frame_counter % self.fps): #counts number of seconds player is drawing using the frame rate of the game
                self.draw_timer+=1
            if self.draw_timer == 1:
                self.music_change()
            self.clock.tick(self.fps)
            #self.switch_update()

            #self.random_draw()
            #if (((self.centre[0]-self.canvas_width/2)<xy[0]>(self.centre[0]+self.canvas_width/2)) or ((self.centre[1]-self.canvas_height/2)<xy[1]>(self.centre[1]+self.canvas_height/2))):

             # returns true if mouse is being held down which enables draw



            #self.display.blit(self.canvas)
            #pygame.draw(self.display, (255,255,255), canvas)
            pygame.display.update()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                #Mouse usage only
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.resetTracker()
                        self.draw_blit = True
                if event.type == pygame.KEYUP:
                    self.sendServer("SERVERCMD: !RESETTRACKER", True)
                    self.draw_blit = False
                    

    def load_sprites(self):
        None
    
    def sendServer(self, data, requiresDrawer=False):
        if self.Client is None:
            return
        self.Client.sendServer(data, requiresDrawer)
    
    def sendFPGA(self, data):
        if self.FPGA is None:
            return
        self.FPGA.send(data)
    
    def resetTracker(self):
        self.drawPoints = [(None, None), (None, None), 0]
    
    def clearPlayers(self):
        self.players = []
    
    def updatePlayers(self, playerdata):
        self.players.append(playerdata)


if __name__ == "__main__":
    GameTest = Game("test")
    GameTest.wait_screen()
    #GameTest.round_start()
