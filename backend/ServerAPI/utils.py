import pygame as pg
import os
from pygame.colordict import THECOLORS
from random import randint
os.environ["SDL_VIDEODRIVER"] = "dummy"


def find_anomally(int1, x1, y1, int2, x2, y2, int3, x3, y3):
    pif = lambda x, y, x1, y1 : ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
    int_anom = lambda int1, xa, ya, x1, y1 : int1 * pif(xa, ya, x1, y1) ** 2
    def dispersion(a, b, c):
        mean = (a + b + c) / 3
        return (a - mean) ** 2 + (b - mean) ** 2 + (c - mean) ** 2 

    # Простой перебор всех клеток поля. Решает в целых числах.
    min_d, best_xa, best_ya = 10e9, None, None
    for x in range(0, 40):
        for y in range(0, 30):
            # Дисперсия
            d = dispersion(int_anom(int1, x1, y1, x, y),
                        int_anom(int2, x2, y2, x, y),
                        int_anom(int3, x3, y3, x, y))
            if d < min_d:
                min_d = d
                best_xa, best_ya = x, y
    int0 = int1 * pif(best_xa, best_ya, x1, y1) ** 2
    return best_xa, best_ya, int0

def swans_visualization(swans):
    pg.init()

    part_size = 500
    ceil_size = part_size / 10
    W, H = part_size * 4, part_size * 3 
    sc = pg.display.set_mode((W, H))

    img = pg.image.load('backend/media/map.png').convert()
    img = pg.transform.scale(img, (W, H))

    f4 = lambda swan : 5 if swan.int0 < 2 else (swan.int0 / 2) ** 0.5 * ceil_size
    anoms = [[(int((swan.x) * ceil_size), int((swan.y) * ceil_size)), f4(swan)] for swan in swans]

    sc.blit(img, (0, 0))

    surface1 = sc.convert_alpha()
    surface1.fill([0,0,0,0])
    [pg.draw.circle(surface1, (255, 0, 0, 128), n, k) for n, k in anoms]
    sc.blit(surface1, (0, 0))

    pg.image.save(sc, 'backend/media/map_with_swans.png')


