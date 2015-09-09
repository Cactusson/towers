"""
The intro screen of the game. The first thing the user sees.
"""

import pygame as pg

from .. import prepare, tools


class Intro(tools._State):
    """
    Nothing happens here, just wait for user to press any button.
    Then we move to CHOOSE_LEVEL.
    """
    def __init__(self):
        tools._State.__init__(self)
        self.next = "CHOOSE_LEVEL"

        self.title_font = pg.font.Font(
            prepare.FONTS['chickweed-titling.regular'], 80)
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 26)

        self.bg_color = pg.Color('#BDD8F1')

        self.frame_image = pg.Surface((600+10*2, 400+10*2)).convert()
        self.frame_image.fill(pg.Color('#214177'))
        self.frame_rect = self.frame_image.get_rect(topleft=(100-10, 100-10))

        self.menu_image = pg.Surface((600, 400)).convert()
        self.menu_image.fill(pg.Color('#82A6CB'))
        self.menu_rect = self.menu_image.get_rect(topleft=(100, 100))

        self.title_frame_image = pg.Surface(
            (600-30*2, 400-30*2-120)).convert()
        self.title_frame_image.fill(pg.Color('#214177'))
        self.title_frame_rect = self.title_frame_image.get_rect(
            topleft=(100+30, 100+30))

        self.title_image = pg.Surface(
            (600-30*2-10*2, 400-30*2-10*2-120)).convert()
        self.title_image.fill(pg.Color('#82A6CB'))
        self.title_rect = self.title_image.get_rect(
            topleft=(100+30+10, 100+30+10))

        title_text = self.title_font.render('Towers', True, pg.Color('black'))
        title_rect = title_text.get_rect(
            center=(prepare.SCREEN_RECT.width // 2, 240))
        self.title = (title_text, title_rect)

        escape_text = self.font.render(
            '< Press any key >', True, pg.Color('black'))
        escape_rect = escape_text.get_rect(
            center=(prepare.SCREEN_RECT.width // 2, 425))
        self.escape = (escape_text, escape_rect)

        self.blink = False
        self.timer = 0.0

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.done = True

    def draw(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.frame_image, self.frame_rect)
        screen.blit(self.menu_image, self.menu_rect)
        screen.blit(self.title_frame_image, self.title_frame_rect)
        screen.blit(self.title_image, self.title_rect)
        screen.blit(*self.title)
        if self.blink:
            screen.blit(*self.escape)

    def update(self, screen, keys, current_time, time_delta):
        self.current_time = current_time
        if self.current_time - self.timer > 2000.0 / 5.0:
            self.blink = not self.blink
            self.timer = self.current_time
        self.draw(screen)
