from config import WIDTH, HEIGHT
from utils.factory import EntityFactory
import random

def generate_platforms(factory: EntityFactory, rows, include_base=True, difficulty_level=1): # genera plataformas
    platforms = []
    vertical_distance_min = max(80, 120 - difficulty_level * 5)
    vertical_distance_max = max(100, 200 - difficulty_level * 10)
    platforms_by_row = (2, 3)
    if include_base:
        base = factory.create_platform(WIDTH // 2 - 50, HEIGHT - 50)
        platforms.append(base)
        y_before = base.rect.y - random.randint(vertical_distance_min, vertical_distance_max)
    else:
        y_before = HEIGHT - 50

    for _ in range(rows - 1):
        ammount_in_row = random.randint(*platforms_by_row)
        used_x = []

        for _ in range(ammount_in_row):
            tries = 0
            while True:
                x = random.randint(0, WIDTH - 100)
                if all(abs(x - ux) > 100 for ux in used_x) or tries > 10:
                    break
                tries += 1

            used_x.append(x)
            platforms.append(factory.create_platform(x, y_before))

        y_before -= random.randint(vertical_distance_min, vertical_distance_max)

    return platforms

def generate_coins(factory: EntityFactory, platforms, probability=0.15): # genera monedas
    coins = []
    for platform in platforms:
        if random.random() < probability:
            coins.append(factory.create_coin(platform.rect.x, platform.rect.y))
    return coins