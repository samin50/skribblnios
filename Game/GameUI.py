import pygame
import random
import threading    

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
    def __init__(self,username, FPGAinstance=None, clientInstance=None):
        pygame.init()
        self.font = pygame.font.Font("Game/assets/Gameplay.TTF", 12)
        self.FPGA = FPGAinstance
        self.Client = clientInstance
        self.drawPoints = [(None, None), (None, None), 0]
        pygame.init()
        self.run = False
        self.round_end = False
        self.game_end = False
        self.username = username
        self.width = 1200
        self.height = 700
        self.display = pygame.display.set_mode((self.width, self.height))
        self.pointer = pygame.image.load("Game/assets/cursor.png")
        self.pointer_pos =(359, 190)
        #self.pointer.convert()
        #self.pointerRect = self.pointer.get_rect()
        #self.pointer_img = pygame.image.load("Game/assets/cursor.png")

        #self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.xy = (0,0)
        #self.mouseSurface = pygame.Surface((self.height. self.width))

        self.pointer_surface = pygame.surface.Surface((self.width,self.height))

#canvas:
        self.canvas_width = int(self.width/1.6)
        self.canvas_height = int(self.height/1.3)
        self.canvas = pygame.Rect(self.width/2,self.height/2,self.canvas_width,self.canvas_height)
        self.centre = (self.width/2,self.height/2)
        self.canvas.center = (self.width/2.7,self.height/2)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.colour_string = ""
        self.timer = 200
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
        #self.colour_preview = 

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

#chatbox:
        self.chatbox = pygame.Rect(self.width/5,self.height/2,self.canvas_width/2.3,self.canvas_height)
        self.received_msgs = []
        self.msg_limit = 13
        self.max_char_len = 26

        self.window_pos = (360,160)

    def pointer_update(self,x,y):
        self.pointer_pos = (x,y)
        mouse.move(self.window_pos[0]+self.pointer_pos[0],self.window_pos[1]+self.pointer_pos[1])
    
    def mouseTracker(self):
        mousePos = pygame.mouse.get_pos()
        if self.FPGA is None:
            #self.tempDisplay = self.display
            #self.display.blit(self.cursor, mousePos)
            #pygame.display.update()
            #self.display = self.tempDisplay.copy()
            #pygame.display.update()
            #self.pointer_update(mousePos[0], mousePos[1])
            self.draw_check(mousePos[0], mousePos[1])
        self.switch_collisions(mousePos)
    
    def size_update(self, is_increasing):
        print("Brush size:", self.brush_size)
        if is_increasing:
            self.brush_size+=2
        else:
            if self.brush_size>=3: 
                self.brush_size-=2
        print("New size:", self.brush_size)

    def switch_img_scale(self):
        for i in range(len(self.off_switch)):
            self.off_switch[i] = pygame.transform.scale(self.off_switch[i],(self.switch_size))
            self.on_switch[i] = pygame.transform.scale(self.on_switch[i],(self.switch_size))

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

    def reset_canvas(self, override=False):
        if self.Client is not None:
            if not (self.Client.isDrawing() or override):
                return
        pygame.draw.rect(self.display,(255,255,255),(self.canvas))
        pygame.draw.rect(self.display,(0,0,0),(self.canvas),3)


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
        
    def msg_limiter(self):
        if len(self.received_msgs)>=self.msg_limit:
            self.received_msgs.pop(0)
    
    def redraw_chat(self,textbox):
        pygame.draw.rect(self.display,(204,255,204),(self.chatbox))
        pygame.draw.rect(self.display,(0,0,0),(self.chatbox),3)
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
    
    def addOtherMessages(self, text):
        print("added message")
        self.received_msgs.append(text)


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
                
                if event.type == pygame.KEYUP:
                    self.redraw_chat(textbox)
                    if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        textbox.upper_case = False
                if event.type == pygame.KEYDOWN:
                    self.redraw_chat(textbox)
                    if len(self.username+textbox.text)<26:
                        #self.redraw_chat(textbox)
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
                            self.received_msgs.append((self.username+":  "+textbox.text))
                            self.sendServer("SERVERCMD: !BROADCAST "+ self.username + ": " + textbox.text)
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
        #self.pointer_update(x,y)
        FACTOR = 6.6
        if not self.draw_blit:
            return
        # Add offsets for coordinates
        if useFPGA:
            #Bound angles
            if abs(x) > 35 or abs(y) > 25:
                return
            x =(FACTOR*x)+self.width//2.7
            y =(FACTOR*y)+self.height//2
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
        self.run = True
        self.redraw_window()
        #pygame.mixer.music.play(-1)
        self.background=pygame.transform.scale(self.background,(self.width,self.height))
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
        while self.run == True:

            pygame.draw.rect(self.display,self.brush_colour,(50,self.height-60,30,50)) #pallet preview
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
    
    def resetTracker(self):
        self.drawPoints = [(None, None), (None, None), 0]

if __name__ == "__main__":
    GameTest = Game("test")
    GameTest.round_start()
