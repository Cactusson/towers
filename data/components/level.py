import pygame as pg

from .. import prepare
from ..components.foundation import Foundation
from ..components.wave import Wave


class Level():
    """
    Level is a collection of waves.
    """
    def __init__(self, number, points, waves_list,
                 foundations_list, decor_dict, starting_gold,
                 unlocked_towers, new_tower=None):
        """
        points is a list of change-direction points.
        waves_list is just a list of monsters in those waves.
        foundations_list is a list of coords for foundations.
        """
        self.number = number
        self.points = points
        self.waves_list = waves_list
        self.foundations_list = foundations_list
        self.decor_dict = decor_dict
        self.starting_gold = starting_gold
        self.unlocked_towers = unlocked_towers
        self.new_tower = new_tower
        self.road_tiles = pg.sprite.Group()
        self.set_road_tiles()
        self.set_decorations()

    def set_decorations(self):
        """
        Well, there's some messy code that adds all the decorations
        to the self.decorations. Also it makes sure that they are in
        right order (sorted by y coordinate).
        For every tree_top it creates tree_bottom, cause they're
        different files and there are only tops in components.data.
        """
        self.decorations = []
        decorations = []
        for decor_type in self.decor_dict:
            for pos in self.decor_dict[decor_type]:
                decorations.append((pos[1], pos[0], decor_type))
        decorations.sort()
        for (y, x, name) in decorations:
            image = prepare.GFX['decor']['decor_' + name]
            rect = image.get_rect(topleft=(x, y))
            self.decorations.append((image, rect))
            if name.endswith('top'):
                *start, end = name.split('_')
                pos = x, y + 64
                image = prepare.GFX['decor'][
                    'decor_' + '_'.join(start) + '_bottom']
                rect = image.get_rect(topleft=pos)
                self.decorations.append((image, rect))

    def set_road_tiles(self):
        """
        This code was written a long time ago and I am not sure how it works
        but it creates road_tiles to draw them.
        """
        road_image = prepare.GFX['terrain']['road']
        road_horizontal = prepare.GFX['terrain']['road_horizontal']
        road_vertical = prepare.GFX['terrain']['road_vertical']
        road_topleft_image = prepare.GFX['terrain']['road_topleft']
        road_topright_image = prepare.GFX['terrain']['road_topright']
        road_bottomleft_image = prepare.GFX['terrain']['road_bottomleft']
        road_bottomright_image = prepare.GFX['terrain']['road_bottomright']
        next_image = road_horizontal
        direction = 'right'
        for i in range(len(self.points)):
            if i == len(self.points) - 1:
                break
            if i == 0:
                point1 = [self.points[i][0], self.points[i][1] - 25]
            else:
                point1 = [self.points[i][0] - 25, self.points[i][1] - 25]
            if i == len(self.points) - 2:
                point2 = [self.points[i+1][0], self.points[i+1][1] - 25]
            else:
                point2 = [self.points[i+1][0] - 25, self.points[i+1][1] - 25]
            while point1 != point2:
                road = pg.sprite.Sprite(self.road_tiles)
                if next_image:
                    road.image = next_image
                    next_image = None
                else:
                    road.image = road_image
                road.rect = road.image.get_rect(topleft=point1)
                if point1[0] < point2[0]:
                    point1[0] += 50
                    direction = 'right'
                    next_image = road_horizontal
                elif point1[0] > point2[0]:
                    point1[0] -= 50
                    direction = 'left'
                    next_image = road_horizontal
                elif point1[1] < point2[1]:
                    point1[1] += 50
                    direction = 'down'
                    next_image = road_vertical
                elif point1[1] > point2[1]:
                    point1[1] -= 50
                    direction = 'up'
                    next_image = road_vertical
                if point1 == point2:
                    if i < len(self.points) - 2:
                        next_point = (self.points[i+2][0] - 25,
                                      self.points[i+2][1] - 25)
                        if direction == 'right':
                            if next_point[1] < point2[1]:
                                next_image = road_bottomright_image
                            elif next_point[1] > point2[1]:
                                next_image = road_topright_image
                        elif direction == 'left':
                            if next_point[1] < point2[1]:
                                next_image = road_bottomleft_image
                            elif next_point[1] > point2[1]:
                                next_image = road_topleft_image
                        elif direction == 'down':
                            if next_point[0] < point2[0]:
                                next_image = road_bottomright_image
                            elif next_point[0] > point2[0]:
                                next_image = road_bottomleft_image
                        elif direction == 'up':
                            if next_point[0] < point2[0]:
                                next_image = road_topright_image
                            elif next_point[0] > point2[0]:
                                next_image = road_topleft_image

    def kickstart(self, game):
        """
        Creates waves and foundations. Calls self.next_wave.
        """
        self.done = False
        self.waves = []
        for wave_number, monsters_list in enumerate(self.waves_list):
            self.waves.append(Wave(self, wave_number+1, monsters_list))
        for location in self.foundations_list:
            game.foundations.add(Foundation(location))
        self.next_wave(game)

    def next_wave(self, game):
        """
        Kickstars a new wave.
        If there are no waves left, level is done.
        """
        if self.waves:
            game.wave_in_progress = self.waves.pop(0)
            game.wave_in_progress.kickstart(game)
        else:
            game.wave_in_progress = None
            self.done = True

    def draw(self, screen):
        """
        Draws road and decorations.
        """
        self.road_tiles.draw(screen)
        for (image, rect) in self.decorations:
            screen.blit(image, rect)

    def update(self, game):
        """
        Checking if we should start the next wave.
        Well, not the best way to do it, I guess, but it works.

        """
        if game.wave_in_progress:
            if game.wave_in_progress.done:
                self.next_wave(game)
