import pygame
from client import Game

def main_menu(n,display):
    gif_track = 0
    menu = True

    tracker=["start","create_char","instructions","highscores","quit"]
    pointer=0

    selected="start"
    while menu:
        if gif_track>20:
            gif_track = 0
        else:
            gif_track+=1
        
        pygame.display.update()
        display.fill(white)
        display.blit(backgrounds[gif_track],(0,0))

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

                    if selected =="start":
                        game = Game("shan")
                        pygame.display.set_caption("player")
                        game.round_start()


        font_size=32
        text_start = ""

        if selected=="start":
            text_start=process_text("JOIN GAME", font, font_size, white)
        else:
            text_start = process_text("JOIN GAME", font, font_size, black)
        if selected=="quit":
            text_quit=process_text("QUIT", font, font_size, white)
        else:
            text_quit = process_text("QUIT", font, font_size, black)
        if selected == "highscores":
            text_highscores=process_text("HIGHSCORES", font, font_size, white)

        else:
            text_highscores =process_text("HIGHSCORES", font, font_size, black)

        if selected =="instructions":
            text_instructions = process_text("INSTRUCTIONS",font,font_size,white)
        else:
            text_instructions = process_text("INSTRUCTIONS",font,font_size,black)

        if selected == "create_char":
            text_createserver = process_text("CREATE CHARACTER",font,font_size,white)
        else:
            text_createserver = process_text("CREATE CHARACTER",font,font_size,black)


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
        clock.tick(10)
        pygame.display.set_caption("Main Menu")
    
    

def process_text(message, font, size, color):
    new_font = pygame.font.Font(font, size)
    edited = new_font.render(message, 0, color)
    return edited
    
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    white=(205, 205, 205)
    black=(0, 0, 0)
    brown=(150,75,0)
    red=(255, 0, 0)
    yellow=(255, 255, 0)
    blue=(0, 0, 255)
    green=(0, 255, 0)
    grey=(128, 128, 128)
    turquoise = (0,255,239)
    background = pygame.image.load("Game/assets/sky_background.png")
    width = 900
    height = 550
    background=pygame.transform.scale(background,(width,height))
    display = pygame.display.set_mode((width, height))
    display.fill(white)
    clock = pygame.time.Clock()
    pygame.init()   
    music=pygame.mixer.music.load("Game/assets/music_main.wav")
    pygame.mixer.music.play(-1)
    backgrounds = []
    for i in range(100):
        dir = f"Game/assets/backgrounds/{i}.gif"
        img = pygame.image.load(dir)
        img = pygame.transform.scale(img,(width,height))
        backgrounds.append(img)
    font = "Game/assets/arcade.TTF"
    menu = True
    main_menu(0,display)
