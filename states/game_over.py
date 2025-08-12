from states.states import GameState
from config import WIDTH, HEIGHT, PURPLE, CREAM
import pygame

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.rect_restart = pygame.Rect(0,0,0,0)
        self.rect_menu = pygame.Rect(0,0,0,0)
        self.rect_exit = pygame.Rect(0,0,0,0)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect_restart.collidepoint(event.pos):
                    self.game.start_new_game()
                elif self.rect_menu.collidepoint(event.pos):
                    self.game.change_state("menu")
                elif self.rect_exit.collidepoint(event.pos):
                    self.game.quit()

    def update(self):
        pass

    def draw(self): # dibujar en pantalla
        self.game.screen.blit(self.game.resources.get_image("lost_bg"), (0,0)) # imagen de fondo

        title = self.game.title_font.render("Game over", True, PURPLE) #titulo
        self.game.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 135))

        text_score = self.game.menu_font.render(f"Score: {int(self.game.last_score)}", True, PURPLE) # puntaje
        self.game.screen.blit(text_score, (WIDTH // 2 - text_score.get_width() // 2, HEIGHT // 2 - 175))

        # botones
        button_restart = self.game.menu_font.render("Restart", True, CREAM)
        button_menu = self.game.menu_font.render("Back to menu", True, CREAM)
        button_exit = self.game.menu_font.render("Exit", True, CREAM)

        position_restart = (WIDTH // 2 - button_restart.get_width() // 2, 395)
        position_menu = (WIDTH // 2 - button_menu.get_width() // 2, 470)
        position_exit = (WIDTH // 2 - button_exit.get_width() // 2, 545)

        self.game.screen.blit(button_restart, position_restart)
        self.game.screen.blit(button_menu, position_menu)
        self.game.screen.blit(button_exit, position_exit)

        self.rect_restart = pygame.Rect(position_restart[0], position_restart[1], button_restart.get_width(), button_restart.get_height())
        self.rect_menu = pygame.Rect(position_menu[0], position_menu[1], button_menu.get_width(), button_menu.get_height())
        self.rect_exit = pygame.Rect(position_exit[0], position_exit[1], button_exit.get_width(), button_exit.get_height())

        # cursor
        cursor_image = self.game.resources.get_image("cursor")
        mouse_position = pygame.mouse.get_pos()
        self.game.screen.blit(cursor_image, mouse_position)

        pygame.display.flip()