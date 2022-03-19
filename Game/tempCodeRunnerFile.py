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