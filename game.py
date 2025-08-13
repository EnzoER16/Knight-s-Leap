from config import WIDTH, HEIGHT
from utils.resource_manager import ResourceManager
from utils.factory import EntityFactory
from states.main_menu import MenuState
from states.how_to_play import HowToState
from states.game_over import GameOverState
from states.play import PlayState
import pygame
import sys

class Game:
    def __init__(self):

        # inicializar
        pygame.init()
        pygame.mixer.init()

        # configuracion de pantalla
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Knight's Leap")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        self.clock = pygame.time.Clock()
        self.running = True

        self.resources = ResourceManager() # cargar recursos

        # cargar imagenes
        self.resources.load_image("game_bg", "assets/images/game_background.png", (1000, 800))
        self.resources.load_image("menu_bg", "assets/images/menu_background.png", (1000, 800))
        self.resources.load_image("lost_bg", "assets/images/lost_background.png", (1000, 800))
        self.resources.load_image("howto_bg", "assets/images/howto_background.png", (1000, 800))
        self.resources.load_image("player", "assets/images/player.png", (39, 54))
        self.resources.load_image("player_jump", "assets/images/player_jump.png", (39, 54))
        self.resources.load_image("platform", "assets/images/platform.png", (96, 27))
        self.resources.load_image("rock", "assets/images/rock.png", (30, 30))
        self.resources.load_image("coin", "assets/images/coin.png", (30, 30))

        # cargar fuentes
        self.title_font = self.resources.load_font("title", 'assets/fonts/PixelOperator8-Bold.ttf', 80)
        self.menu_font = self.resources.load_font("menu", 'assets/fonts/PixelOperator8-Bold.ttf', 50)
        self.score_font = self.resources.load_font("score", 'assets/fonts/PixelOperator8-Bold.ttf', 38)
        self.text_font = self.resources.load_font("text", 'assets/fonts/PixelOperator8-Bold.ttf', 28)

        self.menu_font = self.resources.get_font("menu")
        self.title_font = self.resources.get_font("title")
        self.score_font = self.resources.get_font("score")
        self.text_font = self.resources.get_font("text")

        # cargar sonidos
        self.resources.load_sound("jump", "assets/sounds/jump.wav")
        self.resources.load_sound("coin", "assets/sounds/coin.wav")
        self.resources.load_sound("lose", "assets/sounds/lose.wav")

        pygame.mixer.music.load("assets/sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.resources.load_image("cursor", "assets/images/cursor.png", (24, 31)) # cursor personalizado

        pygame.mouse.set_visible(False) # ocultar cursor

        self.factory = EntityFactory(self.resources) # patron factory

        # patron state
        self.states = {"menu": MenuState(self),
                       "howto": HowToState(self),
                       "playing": None,
                       "gameover": GameOverState(self)}
        
        # estado y puntaje
        self.current_state = self.states["menu"]
        self.last_score = 0

    def change_state(self, name): # cambiar estado de juego
        if name == "playing":
            self.states["playing"] = PlayState(self)
            self.current_state = self.states["playing"]
        elif name in self.states:
            self.current_state = self.states[name]
        else:
            print("Unknown state:", name)

    def start_new_game(self): # empezar nuevo juego
        self.change_state("playing")

    def quit(self): # salir
        self.running = False

    def run(self): # ejecutar
        while self.running:
            self.clock.tick(60)
            events = pygame.event.get()
            self.current_state.handle_events(events)
            self.current_state.update()
            self.current_state.draw()

        pygame.quit()
        sys.exit()