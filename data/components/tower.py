import math
import pygame as pg

from .. import prepare
from ..components.data import tower_kinds
from ..components.tower_button import TowerButton
from ..components.foundation import Foundation
from ..components.bullet import Bullet


class Tower(pg.sprite.Sprite):
    """
    Towers are what this all about.
    """
    def __init__(self, rect, kind):
        """
        We need to know its rect and its kind.
        """
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(rect)
        self.kind = kind
        self.level = 1
        self.level_cap = tower_kinds[self.kind]['level_cap']
        self.role = tower_kinds[self.kind]['role']
        self.name = tower_kinds[self.kind]['name']
        self.timer = 0.0
        self.ready = True
        self.kickstart()

    def kickstart(self):
        """
        Call this when just built or just upgraded.
        """
        self.image = prepare.GFX['towers'][
            tower_kinds[self.kind]['image_name'][self.level-1]]
        self.description = tower_kinds[self.kind]['description'][self.level-1]
        if self.role == 'attack':
            self.damage = tower_kinds[self.kind]['damage'][self.level-1]
            self.bonus_damage = 0
            self.actual_damage = self.damage
            self.cooldown = tower_kinds[self.kind]['cooldown']
            self.range = tower_kinds[self.kind]['range']
            self.effects = tower_kinds[self.kind]['effects'][self.level-1]
            self.color_range = pg.Color('black')
        elif self.role == 'support':
            self.range = tower_kinds[self.kind]['range']
            self.bonus_damage = \
                tower_kinds[self.kind]['bonus_damage'][self.level-1]
            self.color_range = pg.Color('#9E7EFF')

    def check_damage(self, game):
        """
        Checks if there is any bonus damage.
        """
        # a little ambiguity because bonus_damage is both on support and attack
        # and means different things there
        bonus_damage = 0
        for tower in game.towers:
            if tower.role == 'support':
                if (distance(self.rect.center, tower.rect.center) <=
                        tower.range):
                    bonus_damage += tower.bonus_damage
        self.bonus_damage = bonus_damage
        self.actual_damage = self.damage + self.bonus_damage

    def get_upgrade(self, game):
        """
        Upgrades the tower if level_cap is not reached.
        """
        if (self.level < self.level_cap and
                game.gold >= tower_kinds[self.kind]['price'][self.level]):
            game.change_selection()
            game.gold -= tower_kinds[self.kind]['price'][self.level]
            game.sidebar.update_gold(game.gold)
            self.level += 1
            if self.role == 'attack':
                self.damage = tower_kinds[self.kind]['damage'][self.level-1]
            elif self.role == 'support':
                self.bonus_damage = \
                    tower_kinds[self.kind]['bonus_damage'][self.level-1]
            self.kickstart()

    def sell(self, game):
        """
        Sells the tower and gives money.
        """
        game.gold += tower_kinds[self.kind]['price'][self.level-1] // 2
        game.sidebar.update_gold(game.gold)
        game.change_selection()
        rect = self.rect
        self.kill()
        game.foundations.add(Foundation(rect.topleft))

    def select(self, game):
        """
        Creates tower_button for upgrade on top and for sell on bottom.
        """
        if self.level < self.level_cap:
            top_rect = game.get_tower_button_rects(self.rect, 1, 'top')[0]
            game.tower_buttons.add(TowerButton(
                top_rect, 'upgrade', tower=self, game=game,
                image_name='tower_button_upgrade'))
        bottom_rect = game.get_tower_button_rects(self.rect, 1, 'bottom')[0]
        game.tower_buttons.add(TowerButton(
            bottom_rect, 'sell', tower=self, game=game,
            image_name='tower_button_sell'))

    def unselect(self, game):
        """
        Removes tower_buttons when unselected.
        """
        game.tower_buttons.empty()

    def update(self, game):
        """
        Shoots monsters if any are near and cooldown is off.
        """
        if self.role == 'attack':
            self.check_damage(game)
            now = game.actual_time
            if self.ready:
                for monster in game.monsters:
                    if (distance(monster.rect.center, self.rect.center) <
                            self.range):
                        game.bullets.add(Bullet(self, monster))
                        self.ready = False
                        self.timer = now
                        break
            else:
                if now - self.timer > self.cooldown:
                    self.ready = True

    def draw(self, surface, game):
        """
        Draws tower and if it's selected then tower info too.
        """
        surface.blit(self.image, self.rect)
        if game.selected == self:
            pg.draw.circle(
                surface, self.color_range, self.rect.center, self.range, 2)


def distance(p0, p1):
    """
    Returns distance between two points.
    """
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
