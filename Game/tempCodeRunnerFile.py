disp_word_rect = disp_word.get_rect(x=self.width/2-100,y=35)
            pygame.draw.rect(self.display,(255,255,255),disp_word_rect)
            self.display.blit(disp_word,(self.width/2-100,35))