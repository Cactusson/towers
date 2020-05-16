import pygame as pg

from .. import prepare
from ..components.button import Button


class MenuScreen():
    """
    This class provides tools for screens such as Pause, Lost and Won.
    They all inherit from this class.
    """
    def __init__(self, buttons_list, text_list=[]):
        """
        Veil is rect that darkens all the screen.
        Frame is slightly bigger rect than main.
        """
        self.text_list = text_list
        self.buttons_list = buttons_list

        veil_rect = pg.rect.Rect(0, 0, 800, 800)
        veil_image = pg.Surface((veil_rect.size)).convert()
        veil_image.fill(pg.Color('black'))
        veil_image.set_alpha(150)
        self.veil = (veil_image, veil_rect)

        frame_image = pg.Surface((320, 340)).convert()
        frame_image.fill(pg.Color('#214177'))
        frame_rect = frame_image.get_rect(center=prepare.SCREEN_RECT.center)
        self.frame = (frame_image, frame_rect)

        main_image = pg.Surface((280, 300)).convert()
        main_image.fill(pg.Color('#82A6CB'))
        main_rect = main_image.get_rect(center=prepare.SCREEN_RECT.center)
        self.main = (main_image, main_rect)

        self.text_font = pg.font.Font(prepare.FONTS['Timeless-Bold'], 29)
        self.button_font = pg.font.Font(prepare.FONTS['Timeless'], 27)

        self.buttons = pg.sprite.Group()
        self.text = []

    def kickstart(self):
        """
        You can kickstart the screen multiple times.
        Buttons and text are created only once.
        """
        if self.buttons:
            if self.hovered_button:
                self.hovered_button.change_color(pg.Color('black'))
        else:
            self.set_text()
            self.set_buttons()
        self.hovered_button = None

    def set_text(self):
        """
        text_list = [(text, offset), ...]
        """
        for (text, offset) in self.text_list:
            image = self.text_font.render(text, True, pg.Color('black'))
            center = (self.main[1].centerx + offset[0],
                      self.main[1].y + offset[1])
            rect = image.get_rect(center=center)
            self.text.append((image, rect))

    def set_buttons(self):
        """
        buttons_list = [(name, offset, action), ...]
        """
        for (name, offset, action) in self.buttons_list:
            center = (self.main[1].centerx + offset[0],
                      self.main[1].y + offset[1])
            button = Button(name, self.button_font, center, action)
            self.buttons.add(button)

    def click(self, pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.action()

    def hover(self, pos):
        if self.hovered_button and not self.hovered_button.rect.collidepoint(pos):
            self.hovered_button.change_color(pg.Color('black'))
            self.hovered_button = None
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                self.hovered_button = button
                button.change_color(pg.Color('orange'))

    def draw(self, screen):
        screen.blit(*self.veil)
        screen.blit(*self.frame)
        screen.blit(*self.main)
        for (image, rect) in self.text:
            screen.blit(image, rect)
        for button in self.buttons:
            screen.blit(button.image, button.rect)
