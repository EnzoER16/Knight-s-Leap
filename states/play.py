from states.states import GameState
from utils.generate_entities import generate_platforms, generate_coins
from config import WIDTH, HEIGHT, GREY
import pygame
import random

class PlayState(GameState):
    def __init__(self, game):
        super().__init__(game)

        # dificultad
        self.difficulty_level = 1
        self.interval_increase = 1000
        self.frame_count = 0

        # rocas
        self.rocks = []
        self.rock_spawn_time = 30
        self.rock_size = 40
        self.rock_speed_min = 4
        self.rock_speed_max = 7

        self.factory = self.game.factory # patron factory

        # plataformas, monedas y jugador
        self.platforms = generate_platforms(self.factory, 10, include_base=True, difficulty_level=self.difficulty_level)
        self.coins = generate_coins(self.factory, self.platforms)
        self.player = self.factory.create_player(self.platforms[0])

        self.score = 0 # puntaje

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_w):
                self.player.jump()
                sound = self.game.resources.get_sound("jump")
                if sound:
                    sound.play()

    def update(self):
        self.frame_count += 1

        # incrementar dificultad
        if self.score // self.interval_increase >= self.difficulty_level:
            self.difficulty_level += 1
            self.rock_speed_min += 1
            self.rock_speed_max += 1
            if self.rock_spawn_time > 10:
                self.rock_spawn_time -= 2

        # movimiento lateral, gravedad y salto
        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # colision con plataformas
        self.player.on_ground = False
        if self.player.speed_y > 0:
            for platform in self.platforms:
                if self.player.rect.colliderect(platform.rect) and self.player.rect.bottom <= platform.rect.bottom + 10:
                    self.player.rect.bottom = platform.rect.top
                    self.player.speed_y = 0
                    self.player.on_ground = True

        # scroll vertical
        movement = 0
        if self.player.rect.top <= HEIGHT * 2 // 3.25:
            movement = HEIGHT * 2 // 3.25 - self.player.rect.top
            self.player.rect.top = HEIGHT * 2 // 3.25

            # mover todo hacia abajo
            for platform in self.platforms:
                platform.rect.y += movement
            for moneda in self.coins:
                moneda.rect.y += movement
            for rock in self.rocks:
                rock.rect.y += movement

            self.score += movement // 5 # incrementar puntaje

        # eliminar pataformas y monedas
        self.platforms = [p for p in self.platforms if p.rect.top < HEIGHT]
        self.coins = [c for c in self.coins if c.rect.top < HEIGHT]

        # generar nuevas plataformas
        while len(self.platforms) < 18: # generar nuevas plataformas
            highest_platform = min(self.platforms, key=lambda p: p.rect.top)
            new_y = highest_platform.rect.top - random.randint(120, 200)
            ammount_in_row = random.randint(2, 3)
            used_x = []

            for _ in range(ammount_in_row):
                tries = 0
                while True:
                    x = random.randint(0, WIDTH - 100)
                    if all(abs(x - ux) > 100 for ux in used_x) or tries > 10:
                        break
                    tries += 1
                used_x.append(x)
                self.platforms.append(self.factory.create_platform(x, new_y))

                # agregar moneda
                if random.random() < 0.2:
                    self.coins.append(self.factory.create_coin(x, new_y))

        # perder si el jugador cae
        if self.player.rect.top > HEIGHT:
            lose_sound = self.game.resources.get_sound("lose")
            if lose_sound:
                lose_sound.play()
            self.game.last_score = int(self.score)
            self.game.change_state("gameover")
            return

        # generar nuevas rocas
        if self.frame_count % self.rock_spawn_time == 0: # generar rocas
            x_pos = random.randint(0, WIDTH - self.rock_size)
            speed = random.randint(self.rock_speed_min, self.rock_speed_max)
            self.rocks.append(self.factory.create_rock(x_pos, -self.rock_size, speed))

        # actualizar rocas y detectar colisiones
        for rock in self.rocks[:]:
            rock.update()
            if rock.rect.top > HEIGHT:
                self.rocks.remove(rock)
            elif rock.rect.colliderect(self.player.rect):
                lose_sound = self.game.resources.get_sound("lose")
                if lose_sound:
                    lose_sound.play()
                self.game.last_score = int(self.score)
                self.game.change_state("gameover")
                return
            
        # colisiones de monedas
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                coin_sound = self.game.resources.get_sound("coin")
                if coin_sound:
                    coin_sound.play()
                try:
                    self.coins.remove(coin)
                except ValueError:
                    pass
                self.score += 50

    def draw(self): # dibujar en pantalla
        self.game.screen.blit(self.game.resources.get_image("game_bg"), (0, 0)) # imagen de fondo

        # jugador, plataformas, monedas y rocas
        self.player.draw(self.game.screen)
        for platform in self.platforms:
            platform.draw(self.game.screen)
        for coin in self.coins:
            coin.draw(self.game.screen)
        for rock in self.rocks:
            rock.draw(self.game.screen)

        # mostrar puntaje
        text = self.game.score_font.render(f"Score: {int(self.score)}", True, GREY)
        self.game.screen.blit(text, (10, 10))

        pygame.display.flip()