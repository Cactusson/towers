import pygame as pg

from .. import prepare
from ..components.tower_button import TowerButton


class Foundation(pg.sprite.Sprite):
    """
    Foundations are what we're gonna build towers on.
    """
    def __init__(self, location):
        """
        We should only want to know its location.
        """
        pg.sprite.Sprite.__init__(self)
        self.width = self.height = 50
        self.rect = pg.Rect(location, (self.width, self.height))
        self.image = prepare.GFX['towers']['foundation']

    def hover(self, game):
        self.image = prepare.GFX['towers']['foundation_big']

    def unhover(self, game):
        if game.selected != self:
            self.image = prepare.GFX['towers']['foundation']

    def select(self, game):
        """
        Creates tower_buttons like 'attack' and 'support'
        when you click on foundation.
        """
        rects = game.get_tower_button_rects(self.rect, 2, 'top')
        kinds_list = [('regular', 'sniper', 'slower'), ('support',)]
        images_list = ['tower_button_role_attack', 'tower_button_role_support']
        for rect, kinds, image_name in zip(rects, kinds_list, images_list):
            game.tower_buttons.add(TowerButton(
                rect, 'show', kinds=kinds, foundation=self,
                image_name=image_name))

    def unselect(self, game):
        """
        Removes tower_buttons.
        """
        game.tower_buttons.empty()
        self.image = prepare.GFX['towers']['foundation']
