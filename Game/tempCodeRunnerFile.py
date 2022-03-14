if event.type == pygame.MOUSEBUTTONDOWN:
                        print("MOUSEE")
                        self.draw_blit = True
                        mousePos = pygame.mouse.get_pos()
                        self.draw(mousePos[0], mousePos[1])
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.draw_blit = False