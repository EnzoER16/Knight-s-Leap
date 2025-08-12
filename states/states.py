class GameState: # patron state
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self): # dibujo en pantalla
        raise NotImplementedError