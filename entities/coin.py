from utils.resource_manager import ResourceManager

class Coin: # clase de moneda
    def __init__(self, x, y, resources: ResourceManager):
        self.image = resources.get_image("coin")
        self.rect = self.image.get_rect(midbottom=(x + 48, y - 1))

    def draw(self, surface): #dibujar moneda
        surface.blit(self.image, self.rect)