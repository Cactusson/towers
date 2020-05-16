"""
The win screen of the game. User sees this when he wins the game.
"""

import pygame as pg

from .. import prepare, tools
from ..components.button import Button


class WinScreen(tools._State):
    """
    A simple screen with just one button.
    """
    def __init__(self):
        tools._State.__init__(self)
        self.title_font = pg.font.Font(
            prepare.FONTS['chickweed-titling.regular'], 29)
        self.text_font = pg.font.Font(prepare.FONTS['Timeless-Bold'], 35)
        self.button_font = pg.font.Font(prepare.FONTS['Timeless'], 35)

        self.bg_color = pg.Color('#BDD8F1')

        external_frame_image = pg.Surface((620, 420)).convert()
        external_frame_image.fill(pg.Color('#214177'))
        external_frame_rect = external_frame_image.get_rect(topleft=(90, 90))
        self.external_frame = (external_frame_image, external_frame_rect)

        external_image = pg.Surface((600, 400)).convert()
        external_image.fill(pg.Color('#82A6CB'))
        external_rect = external_image.get_rect(topleft=(100, 100))
        self.external = (external_image, external_rect)

        internal_frame_image = pg.Surface((540, 220)).convert()
        internal_frame_image.fill(pg.Color('#214177'))
        internal_frame_rect = internal_frame_image.get_rect(topleft=(130, 130))
        self.internal_frame = (internal_frame_image, internal_frame_rect)

        internal_image = pg.Surface(
            (600-30*2-10*2, 400-30*2-10*2-120)).convert()
        internal_image.fill(pg.Color('#82A6CB'))
        internal_rect = internal_image.get_rect(
            topleft=(100+30+10, 100+30+10))
        self.internal = (internal_image, internal_rect)

        title_text = self.title_font.render('Towers', True, pg.Color('black'))
        title_rect = title_text.get_rect(
            center=(prepare.SCREEN_RECT.width // 2, 50))
        self.title = (title_text, title_rect)

        self.text = []
        text = [("That's it.", (prepare.SCREEN_RECT.width // 2, 180)),
                ('Congratulations!', (prepare.SCREEN_RECT.width // 2, 260))]
        self.set_text(text)
        self.buttons = pg.sprite.Group()
        self.set_buttons()
        self.hovered_button = None

    def set_text(self, text):
        for (line, center) in text:
            text_image = self.text_font.render(line, True, pg.Color('black'))
            text_rect = text_image.get_rect(center=center)
            self.text.append((text_image, text_rect))

    def set_buttons(self):
        ok = Button('OK', self.button_font, (400, 430), self.action_continue)
        self.buttons.add(ok)

    def action_continue(self):
        self.next = 'CHOOSE_LEVEL'
        self.done = True

    def startup(self, current_time, persistant):
        if self.hovered_button:
            self.hovered_button.change_color(pg.Color('black'))
        self.hovered_button = None
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.action()
                    break
        elif event.type == pg.MOUSEMOTION:
            if self.hovered_button and not self.hovered_button.rect.collidepoint(
                event.pos
            ):
                self.hovered_button.change_color(pg.Color('black'))
                self.hovered_button = None
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    self.hovered_button = button
                    self.hovered_button.change_color(pg.Color('orange'))

    def draw(self, screen):
        screen.fill(self.bg_color)
        screen.blit(*self.external_frame)
        screen.blit(*self.external)
        screen.blit(*self.internal_frame)
        screen.blit(*self.internal)
        screen.blit(*self.title)
        for line in self.text:
            screen.blit(*line)
        for button in self.buttons:
            screen.blit(button.image, button.rect)

    def update(self, screen, keys, current_time, time_delta):
        self.current_time = current_time
        self.draw(screen)
