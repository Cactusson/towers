import pygame as pg


class Button(pg.sprite.Sprite):
    """
    Class for buttons. They have some text on them, can change color.
    Action is a function that needs to be called when button is clicked.
    """
    def __init__(self, text, font, location, action):
        pg.sprite.Sprite.__init__(self)
        self.color = pg.Color('black')
        self.font = font
        self.text = text
        self.action = action
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=location)

    def change_color(self, color):
        self.image = self.font.render(self.text, True, color)
