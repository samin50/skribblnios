import pygame
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

black = (0,0,0)
white = (255,255,255)
font = "Game/assets/arcade.TTF"

class TextBox(pygame.sprite.Sprite):
  def __init__(self,message):
    pygame.sprite.Sprite.__init__(self)
    self.text = ""
    self.font = pygame.font.Font(font, 10)
    self.message = self.font.render(message, False, black)
    self.rect = self.message.get_rect()

  def add_chr(self, char):
    global upper_case
    if char in validChars and not upper_case:
        self.text += char
    elif char in validChars and upper_case:
        self.text += shiftChars[validChars.index(char)]
    self.update()

  def update(self):
    old_rect_pos = self.rect.center
    self.message = self.font.render(self.text, False, black)
    self.rect = self.message.get_rect()
    self.rect.center = old_rect_pos

def run_textbox(screen,input_message,pos):
    global upper_case
    textBox = TextBox(input_message)
    upper_case = False
    textBox.rect.center = pos

    running = True
    while running:
      #screen.fill(black)
      screen.blit(textBox.message, textBox.rect)
      pygame.display.flip()
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYUP:
            if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                upper_case = False
        if e.type == pygame.KEYDOWN:
            textBox.add_chr(pygame.key.name(e.key))
            if e.key == pygame.K_SPACE:
                textBox.text += " "
                textBox.update()
            if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                upper_case = True
            if e.key == pygame.K_BACKSPACE:
                textBox.text = textBox.text[:-1]
                textBox.update()
            if e.key == pygame.K_RETURN:
                if len(textBox.text) > 0:
                    return textBox.text
                    running = False
    pygame.quit()