import pygame as pg

from .. import prepare


class Subtitle(pg.sprite.Sprite):
    """
    The class for this floating subtitle that says 'Level 1' and so on.
    """
    def __init__(self, number):
        pg.sprite.Sprite.__init__(self)
        self.text = 'Level {}'.format(number)
        self.font = pg.font.Font(
            prepare.FONTS['collegiateHeavyOutline Medium'], 64)
        self.image = self.font.render(self.text, True, pg.Color('#214177'))
        self.rect = self.image.get_rect(
            topleft=(-300, prepare.SCREEN_RECT.height // 2))
        self.speed = 10
        self.dx = self.speed
        self.timer = 0.0
        self.delay = 1200
        self.phase = 'float'

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, game):
        """
        Two states = 'float' when floating and 'wait' when freezing
        in the center for a second or so.
        """
        now = game.actual_time
        if self.phase == 'float':
            x, y = self.rect.topleft
            self.rect = self.image.get_rect(topleft=(x+self.dx, y))
            if (abs(self.rect.centerx - prepare.SCREEN_RECT.centerx) < 20 and
                    not self.timer):
                self.phase = 'wait'
                self.timer = now
            elif self.rect.x > prepare.SCREEN_RECT.width:
                game.subtitle = None
                self.kill()
        elif self.phase == 'wait':
            if now - self.timer > self.delay:
                self.phase = 'float'
