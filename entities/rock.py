from utils.resource_manager import ResourceManager

class Rock: # clase de roca
    def __init__(self, x, y, speed, resources: ResourceManager, size=30):
        self.image = resources.get_image("rock")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self): # mover hacia abajo
        self.rect.y += self.speed

    def draw(self, surface): # dibujar roca
        surface.blit(self.image, self.rect)