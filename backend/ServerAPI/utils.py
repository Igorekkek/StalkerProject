import pygame as pg
import os
from pygame.colordict import THECOLORS
from random import randint
from collections import deque
from random import random
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

class SwansVisualization():
    part = 20 * 15
    ceil = part // 10
    K = 2
    ceil_of_way = ceil // K
    W, H = part * 4, part * 3
    cols, rows = 40 * K, 30 * K
    count = 0

    def __init__(self, swans, detectors, start=None, goal=None):
        self.swans = swans
        self.detectors = detectors
        self.start = start
        self.goal = goal
    
    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return queue, visited
    
    def get_next_nodes(self, x, y, grid):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and not grid[y][x] else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def get_rect(self, x, y):
        return (x * self.ceil_of_way + 1, y * self.ceil_of_way + 1, 
                self.ceil_of_way - self.ceil_of_way // 4,
                self.ceil_of_way - self.ceil_of_way // 4)


    def parse_objects(self):
        # обработка объектов для последующий работы
        f4 = lambda swan : 5 if swan.int0 < 2 else (swan.int0 / 2) ** 0.5 * self.ceil
        anoms = [[(int(swan.x * self.ceil), int(swan.y * self.ceil)), f4(swan), swan.idd] for swan in self.swans]
        detects = [[(int(det.x * self.ceil), int(det.y * self.ceil)), det.idd] for det in self.detectors]

        return anoms, detects

    def get_font_and_image(self):
        img = pg.image.load('media/map.png').convert()
        img_rect = pg.transform.scale(img, (self.W, self.H))
        font_obj = pg.font.SysFont('arial', self.ceil // 3 * 2)

        return img_rect, font_obj

    def get_danger_zone_radius(self, int0):
        return (int0 / 2) ** 0.5 * self.ceil

    def is_square_in_danger_zone(self, x, y, swans):
        x, y = x * self.ceil_of_way, y * self.ceil_of_way
        angles = [(x, y), (x + self.ceil_of_way, y), (x, y + self.ceil_of_way), (x + self.ceil_of_way, y + self.ceil_of_way)]
        for swan in swans:
            x0, y0, int0 = swan.x * self.ceil, swan.y * self.ceil, swan.int0
            for angle in angles:
                xs, ys = angle
                if (xs - x0) ** 2 + (ys - y0) ** 2 <= self.get_danger_zone_radius(int0) ** 2:
                    # print()
                    return True
            
        return False

    def draw_way(self, screen):
        # print(self.start, self.goal)

        surface = screen.convert_alpha()

        grid = [
            [1 if self.is_square_in_danger_zone(col, row, self.swans) else 0 for col in range(self.cols)]
            for row in range(self.rows)
        ]

        graph = {}
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if not col:
                    graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y, grid)
        
        # BFS settings
        start = (int(self.start[0]) * self.K, int(self.start[1]) * self.K)
        goal = (int(self.goal[0]) * self.K, int(self.goal[1]) * self.K)
        queue, visited = self.bfs(start, goal, graph)

        for swan in self.swans:
            pg.draw.circle(surface,
                        (255, 0, 0, 128),
                        (swan.x * self.ceil, swan.y * self.ceil), 
                        self.get_danger_zone_radius(swan.int0))

        
        path_head, path_segment = goal, goal
        while path_segment and path_segment in visited:
            pg.draw.rect(surface, (255, 255, 255, 200), self.get_rect(*path_segment), self.ceil_of_way, border_radius=self.ceil_of_way // 3)
            path_segment = visited[path_segment]
            
        
        pg.draw.rect(surface, (0, 0, 255, 128), self.get_rect(*start), border_radius=self.ceil_of_way // 3)
        pg.draw.rect(surface, (255, 0, 255), self.get_rect(*path_head), border_radius=self.ceil_of_way // 3)

        return surface

    def run(self):
        SwansVisualization.count += 1

        pg.init()
        screen = pg.display.set_mode((self.W, self.H))
        
        img, font = self.get_font_and_image()
        swans, locators = self.parse_objects()

        # blit image
        screen.blit(img, (0, 0))

        # blit swans danger zone
        surface1 = screen.convert_alpha()
        surface1.fill([0,0,0,0])
        [pg.draw.circle(surface1, (255, 0, 0, 128), cords, r) for cords, r, idd in swans]
        screen.blit(surface1, (0, 0))


        # blit detectors ans swans
        radius = self.ceil / 3
        def draw_object_id(cords, id):
            surf_text = font.render(f'{idd}', 1, (255, 255, 255))
            screen.blit(surf_text, cords)

        for cords, idd in locators:
            pg.draw.circle(screen, (0, 0, 255), cords, radius)
            draw_object_id(cords, idd)

        for cords, r, idd in swans:
            pg.draw.circle(screen, (255, 0, 255), cords, radius) 
            draw_object_id(cords, idd)
        
        if self.start != None and self.goal != None:
            try:
                surf = self.draw_way(screen)
                screen.blit(surf, (0, 0))
            except:
                return 'Маршрут невозможно постороить', 400

        pg.image.save(screen, f'media/map_with_swans{SwansVisualization.count}.png')

        return f'http://localhost:8000/media/map_with_swans{SwansVisualization.count}.png', 200

