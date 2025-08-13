from utils.resource_manager import ResourceManager
from entities.platform import Platform
from entities.rock import Rock
from entities.coin import Coin
from entities.player import Player

class EntityFactory: # patron factory
    def __init__(self, resources: ResourceManager):
        self.resources = resources

    def create_platform(self, x, y): # crear plataforma
        return Platform(x, y, self.resources)

    def create_rock(self, x, y, speed): # crear roca
        return Rock(x, y, speed, self.resources)

    def create_coin(self, x, y): # crear moneda
        return Coin(x, y, self.resources)

    def create_player(self, initial_platform): # crear jugador
        return Player(initial_platform, self.resources)