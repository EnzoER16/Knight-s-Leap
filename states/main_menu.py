from states.states import GameState
from config import WIDTH, DARK_BLUE, LIGHT_BLUE
import pygame

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.rect_play = pygame.Rect(0,0,0,0)
        self.rect_howto = pygame.Rect(0,0,0,0)
        self.rect_exit = pygame.Rect(0,0,0,0)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect_play.collidepoint(event.pos):
                    self.game.start_new_game()
                elif self.rect_howto.collidepoint(event.pos):
                    self.game.change_state("howto")
                elif self.rect_exit.collidepoint(event.pos):
                    self.game.quit()

    def update(self):
        pass

    def draw(self): # dibujar en pantalla
        self.game.screen.blit(self.game.resources.get_image("menu_bg"), (0, 0)) # imagen de fondo

        title = self.game.title_font.render("Knight's Leap", True, DARK_BLUE) # titulo
        self.game.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 175))

        # botones
        button_play = self.game.menu_font.render("Play", True, LIGHT_BLUE)
        button_howto = self.game.menu_font.render("How to play", True, LIGHT_BLUE)
        button_exit = self.game.menu_font.render("Exit", True, LIGHT_BLUE)

        position_play = (WIDTH // 2 - button_play.get_width() // 2, 395)
        position_howto = (WIDTH // 2 - button_howto.get_width() // 2, 470)
        position_exit = (WIDTH // 2 - button_exit.get_width() // 2, 545)

        self.game.screen.blit(button_play, position_play)
        self.game.screen.blit(button_howto, position_howto)
        self.game.screen.blit(button_exit, position_exit)

        self.rect_play = pygame.Rect(position_play[0], position_play[1], button_play.get_width(), button_play.get_height())
        self.rect_howto = pygame.Rect(position_howto[0], position_howto[1], button_howto.get_width(), button_howto.get_height())
        self.rect_exit = pygame.Rect(position_exit[0], position_exit[1], button_exit.get_width(), button_exit.get_height())

        # cursor
        cursor_image = self.game.resources.get_image("cursor")
        mouse_position = pygame.mouse.get_pos()
        self.game.screen.blit(cursor_image, mouse_position)

        pygame.display.flip()