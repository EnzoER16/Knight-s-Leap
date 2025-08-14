import pygame

class ResourceManager: # patron singleton
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.images = {}
            cls._instance.sounds = {}
            cls._instance.fonts = {}
        return cls._instance

    def load_image(self, key, path, size=None): # carga las imagenes
        if key in self.images:
            return self.images[key]
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        self.images[key] = image
        return image

    def get_image(self, key):
        return self.images.get(key)

    def load_sound(self, key, path): # carga los sonidos
        if key in self.sounds:
            return self.sounds[key]
        sound = pygame.mixer.Sound(path)
        self.sounds[key] = sound
        return sound

    def get_sound(self, key):
        return self.sounds.get(key)

    def load_font(self, key, path, size):  # carga las fuentes
        if key in self.fonts:
            return self.fonts[key]
        f = pygame.font.Font(path, size)
        self.fonts[key] = f
        return f

    def get_font(self, key):
        return self.fonts.get(key)