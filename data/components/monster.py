import pygame as pg

from ..components.data import monsters_kinds


class Monster(pg.sprite.Sprite):
    """
    Monsters are coming in waves and we need to shoot them.
    """
    def __init__(self, points, kind):
        """
        Points are points where monster changes its direction.
        """
        pg.sprite.Sprite.__init__(self)
        self.kind = kind
        self.name = monsters_kinds[self.kind]['name']
        self.image_right = monsters_kinds[self.kind]['image_right']
        self.image_left = monsters_kinds[self.kind]['image_left']
        self.image = self.image_right
        self.rect = self.image.get_rect(center=points[0])
        self.speed = monsters_kinds[self.kind]['speed']
        self.bonus_speed = 0
        self.actual_speed = self.speed
        self.health = monsters_kinds[self.kind]['health']
        self.current_health = self.health
        self.bounty = monsters_kinds[self.kind]['bounty']
        self.points = points
        self.status = []
        self.slow_timer = 0.0
        self.slow_duration = 0
        self.point_number = 0
        self.last_point = None
        self.next_point = None

    def check_speed(self, game):
        """
        Check if slowed.
        """
        if 'slowed' in self.status:
            now = game.actual_time
            if now - self.slow_timer > self.slow_duration:
                self.bonus_speed = 0
                self.status.remove('slowed')
                self.actual_speed = self.speed + self.bonus_speed
        if self.dx < 0:
            self.dx = -self.actual_speed
        elif self.dx > 0:
            self.dx = self.actual_speed
        if self.dy < 0:
            self.dy = -self.actual_speed
        elif self.dy > 0:
            self.dy = self.actual_speed

    def get_slowed(self, game, speed_reduction, slow_duration):
        """
        Add 'slowed' to status + change speed.
        """
        if 'slowed' not in self.status:
            self.status.append('slowed')
        self.bonus_speed = -speed_reduction
        self.slow_duration = slow_duration * 1000
        self.slow_timer = game.actual_time
        self.actual_speed = self.speed + self.bonus_speed
        if self.actual_speed < 1:
            self.actual_speed = 1
        self.check_speed(game)

    def get_next_point(self, game):
        """
        Called when monster reaches his point and is ready to change direction.
        """
        self.point_number += 1
        if self.point_number >= len(self.points):
            game.lives -= 1
            game.sidebar.update_lives(game.lives)
            if game.selected == self:
                game.selected = None
            self.kill()
        else:
            self.last_point = self.points[self.point_number - 1]
            next_point = self.points[self.point_number]
            if next_point[0] > self.last_point[0]:
                self.dx = self.actual_speed
                self.dy = 0
                self.image = self.image_right
            elif next_point[0] < self.last_point[0]:
                self.dx = -self.actual_speed
                self.dy = 0
                self.image = self.image_left
            elif next_point[1] > self.last_point[1]:
                self.dx = 0
                self.dy = self.actual_speed
            elif next_point[1] < self.last_point[1]:
                self.dx = 0
                self.dy = -self.actual_speed
            return next_point

    def select(self, game):
        pass

    def unselect(self, game):
        pass

    def update(self, game):
        """
        Check if point of changing direction is reached + moving.
        """
        if not self.next_point:
            self.last_point = self.points[0]
            self.next_point = self.get_next_point(game)
        self.check_speed(game)
        if self.rect.collidepoint(self.next_point):
            self.next_point = self.get_next_point(game)
        else:
            self.rect.x += self.dx
            self.rect.y += self.dy
