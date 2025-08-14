from utils.resource_manager import ResourceManager
from config import WIDTH
import pygame

class Player: # clase del jugador
    def __init__(self, initial_platform, resources: ResourceManager):
        self.resources = resources
        self.image = resources.get_image("player")
        self.jump_image = resources.get_image("player_jump")
        self.rect = self.image.get_rect()
        self.rect.midbottom = initial_platform.rect.midtop
        self.speed_y = 0
        self.on_ground = True
        self.facing_right = True

    def move(self, keys): # mover al jugador
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
            self.facing_right = True

        self.speed_y += 0.5 # controlar la gravedad
        self.rect.y += self.speed_y

        if self.rect.right < 0: # moverse horizontalmente
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0

    def jump(self): # saltar
        if self.on_ground:
            self.speed_y = -15
            self.on_ground = False

    def draw(self, surface): # dibujar al jugador
        image = self.jump_image if not self.on_ground else self.image
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, self.rect)