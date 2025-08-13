from utils.resource_manager import ResourceManager

class Platform: # clase de plataforma
    def __init__(self, x, y, resources: ResourceManager):
        self.image = resources.get_image("platform")
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface): # dibuja la plataforma
        surface.blit(self.image, self.rect)