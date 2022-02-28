import pygame

def menu(start):

    pygame.init()

    width = 900
    height = 550
    display = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    background = pygame.image.load("Game/assets/sky_background.png")

    white=(255, 255, 255)
    black=(0, 0, 0)
    brown=(150,75,0)
    red=(255, 0, 0)
    yellow=(255, 255, 0)
    blue=(0, 0, 255)
    green=(0, 255, 0)
    grey=(128, 128, 128)
    turquoise = (0,255,239)

    music=pygame.mixer.music.load("Game/assets/music_main.wav")
    pygame.mixer.music.play(-1)

    n=0
    font = "Game/assets/arcade.TTF"
    

    def main_menu(n,start):


        tracker=["start","Create Server","instructions","highscores","quit"]
        pointer=0

        menu=True
        selected="start"
        while menu:
            if n>6:
                n=0
            else:
                n+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        selected="start"
                        if pointer>0:
                            pointer-=1
                        selected=tracker[pointer]

                    if event.key==pygame.K_DOWN:
                        if pointer<4:
                            pointer+=1
                        selected=tracker[pointer]

                    if event.key==pygame.K_RETURN:
                        if selected=="quit":
                            pygame.quit()
                            quit()
                        #if selected =="start":
                            #result=server_screen(server_address)
                            #if result != None:
                                #return [True,result]

                        #if selected == "highscores":
                            #start_new_thread(run_table,())

                        '''if selected =="Create Server":
                            name = run_textbox(display,"ENTER  SERVER  NAME")
                            time_limit = run_textbox(display, "ENTER  MATCH  TIME ")
                            while True:
                                try:
                                    print(int(time_limit))
                                except:
                                    time_limit = run_textbox(display, "ENTER  INTEGERS  ONLY ")
                                else:
                                    break

                            if server_started == False:
                                server_started = True
                                start_new_thread(run,(name,int(time_limit)))
                            else:
                                text_font = pygame.font.Font(font, 50)
                                message = "SERVER  ALREADY  STARTED"
                                text = text_font.render(message, 0, white)
                                display.fill(black)
                                display.blit(text,(200,275))
                                pygame.display.update()
                                time.sleep(2)
                                print("Server already started")'''

            display.fill(white)
            display.blit(background,(0,0))
            
            font_size=32

            if selected=="start":
                text_start=process_text("JOIN GAME", font, font_size, white)
            else:
                text_start = process_text("JOIN GAME", font, font_size, yellow)
            if selected=="quit":
                text_quit=process_text("QUIT", font, font_size, white)
            else:
                text_quit = process_text("QUIT", font, font_size, yellow)
            if selected == "highscores":
                text_highscores=process_text("HIGHSCORES", font, font_size, white)

            else:
                text_highscores =process_text("HIGHSCORES", font, font_size, yellow)

            if selected =="instructions":
                text_instructions = process_text("INSTRUCTIONS",font,font_size,white)
            else:
                text_instructions = process_text("INSTRUCTIONS",font,font_size,yellow)

            if selected == "Create Server":
                text_createserver = process_text("HOST MATCH",font,font_size,white)
            else:
                text_createserver = process_text("HOST MATCH",font,font_size,yellow)


        #title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        highscores_rect=text_highscores.get_rect()
        instruct_rect=text_instructions.get_rect()
        create_rect = text_createserver.get_rect()
        pos=width/2
        #display.blit(title, (450 - (title_rect[2]/2), 80))
        display.blit(text_start, (pos - (start_rect[2]/2), 80))
        display.blit(text_createserver,(pos - (create_rect[2]/2),120))
        display.blit(text_instructions, ( pos- (instruct_rect[2]/2), 160))
        display.blit(text_highscores, (pos - (highscores_rect[2]/2),200))
        display.blit(text_quit, (pos -(quit_rect[2]/2),240))
        pygame.display.update()
        clock.tick(5)
        pygame.display.set_caption("Main Menu")
        
    def process_text(message, font, size, color):
        new_font = pygame.font.Font(font, size)
        edited = new_font.render(message, 0, color)
        return edited




    main_menu(n,start)
    pygame.quit()
menu(True)