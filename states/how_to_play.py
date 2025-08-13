from states.states import GameState
from config import WIDTH, HEIGHT, ORANGE, BLACK, LIGHT_YELLOW
import pygame

class HowToState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.rect_back = pygame.Rect(0,0,0,0)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect_back.collidepoint(event.pos):
                    self.game.change_state("menu")

    def update(self):
        pass

    def draw(self): # dibujar en pantalla
        self.game.screen.blit(self.game.resources.get_image("howto_bg"), (0, 0)) # imagen de fondo

        title = self.game.title_font.render("How to Play", True, ORANGE) # titulo
        self.game.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 175))

        #instrucciones
        instructions = ["Use LEFT and RIGHT arrows to move.",
                        "Press UP arrow to jump.",
                        "Avoid falling or hitting rocks.",
                        "Collect coins for extra points.",
                        "Reach as high as you can."]
        
        y_offset = 350
        for line in instructions:
            text = self.game.text_font.render(line, True, BLACK)
            self.game.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 50

        # botones
        button_back = self.game.menu_font.render("Back", True, LIGHT_YELLOW)
        position_back = (WIDTH // 2 - button_back.get_width() // 2, HEIGHT - 100)
        self.game.screen.blit(button_back, position_back)

        self.rect_back = pygame.Rect(position_back[0], position_back[1], button_back.get_width(), button_back.get_height())

        # cursor
        cursor_image = self.game.resources.get_image("cursor")
        mouse_position = pygame.mouse.get_pos()
        self.game.screen.blit(cursor_image, mouse_position)

        pygame.display.flip()