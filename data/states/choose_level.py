"""
Shows a table with opened levels and lets user choose one.
"""

import pygame as pg

from .. import prepare, tools
from ..components.data import TOTAL_LEVELS
from ..components.button import Button


class Level(pg.sprite.Sprite):
    """
    Class for levels, that are numbers in circles.
    """
    def __init__(self, number, font, location, status):
        pg.sprite.Sprite.__init__(self)
        self.font = font
        self.number = number
        self.status = status
        if self.status == 'opened':
            self.color = pg.Color('black')
        elif self.status == 'closed':
            self.color = pg.Color('gray')
        elif self.status == 'selected':
            self.color = pg.Color('orange')
        elif self.status == 'hovered':
            self.color = pg.Color('white')
        self.image = pg.Surface((60, 60))
        self.image.fill(pg.Color('#82A6CB'))
        self.rect = self.image.get_rect(center=location)
        self.text = self.font.render(str(self.number), True, self.color)
        self.text_rect = self.text.get_rect(center=location)

    def change_status(self, status):
        """
        Level can be opened, closed, selected or hovered.
        """
        self.status = status
        if self.status == 'opened':
            self.color = pg.Color('black')
        elif self.status == 'closed':
            self.color = pg.Color('gray')
        elif self.status == 'selected':
            self.color = pg.Color('orange')
        elif self.status == 'hovered':
            self.color = pg.Color('white')
        self.text = self.font.render(str(self.number), True, self.color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pg.draw.circle(screen, self.color, self.rect.center, 30, 2)
        screen.blit(self.text, self.text_rect)


class ChooseLevel(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title_font = pg.font.Font(
            prepare.FONTS['chickweed-titling.regular'], 29)
        self.text_font = pg.font.Font(prepare.FONTS['Timeless'], 26)
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 35)

        self.bg_color = pg.Color('#BDD8F1')

        self.frame_image = pg.Surface((600+10*2, 400+10*2)).convert()
        self.frame_image.fill(pg.Color('#214177'))
        self.frame_rect = self.frame_image.get_rect(topleft=(100-10, 100-10))

        self.menu_image = pg.Surface((600, 400)).convert()
        self.menu_image.fill(pg.Color('#82A6CB'))
        self.menu_rect = self.menu_image.get_rect(topleft=(100, 100))

        self.choose_frame_image = pg.Surface(
            (600-30*2, 400-30*2-120)).convert()
        self.choose_frame_image.fill(pg.Color('#214177'))
        self.choose_frame_rect = self.choose_frame_image.get_rect(
            topleft=(100+30, 100+30))

        self.choose_image = pg.Surface(
            (600-30*2-10*2, 400-30*2-10*2-120)).convert()
        self.choose_image.fill(pg.Color('#82A6CB'))
        self.choose_rect = self.choose_image.get_rect(
            topleft=(100+30+10, 100+30+10))

        title_text = self.title_font.render('Towers', True, pg.Color('black'))
        title_rect = title_text.get_rect(
            center=(prepare.SCREEN_RECT.width // 2, 50))
        self.title = (title_text, title_rect)

        choose_text = self.text_font.render(
            'Choose level:', True, pg.Color('black'))
        choose_rect = choose_text.get_rect(
            center=(prepare.SCREEN_RECT.width // 2, 185))
        self.choose = (choose_text, choose_rect)

        self.color_opened = pg.Color('black')
        self.color_closed = pg.Color('gray')
        self.color_selected = pg.Color('orange')
        self.color_hovered = pg.Color('orange')

        self.buttons = pg.sprite.Group()
        self.set_buttons()
        self.hovered_button = None

    def set_levels(self):
        for num in range(TOTAL_LEVELS):
            status = 'closed' if num > self.last_opened_level else 'opened'
            level = Level(
                num+1, self.font, (200 + (num % 5) * 100, 255), status)
            if self.to_select == num:
                level.change_status('selected')
            self.levels.add(level)

    def set_buttons(self):
        go = Button('PLAY', self.font, (400, 400), self.action_play)
        quit = Button('QUIT', self.font, (400, 460), self.action_quit)
        self.buttons.add(go, quit)

    def action_play(self):
        for level in self.levels:
            if level.status == 'selected':
                selected_level = level
                break
        else:
            return
        self.next = 'GAME'
        self.next_level = selected_level.number - 1
        self.done = True

    def action_quit(self):
        self.quit = True

    def startup(self, current_time, persistant):
        if self.hovered_button:
            self.hovered_button.change_color(pg.Color('black'))
        self.hovered_button = None
        self.hovered_level = None
        self.next_level = None
        self.levels = pg.sprite.Group()

        self.persist = persistant
        if self.previous == 'GAME':
            move_on = self.persist['move_on']
            level_index = self.persist['level_index']
            if (level_index + 1 > self.last_opened_level and move_on and
                    level_index + 1 <= TOTAL_LEVELS):
                self.last_opened_level = level_index + 1
                self.to_select = level_index + 1
            else:
                # self.last_opened_level = level_index
                self.to_select = level_index
        elif self.previous == 'INTRO':
            self.last_opened_level = 0
            self.to_select = 0
        elif self.previous == 'WIN_SCREEN':
            self.to_select = self.last_opened_level
        self.set_levels()
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        self.done = False
        self.persist['level_index'] = self.next_level
        return self.persist

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.action()
                    break
            else:
                for level in self.levels:
                    if (level.status == 'hovered' and
                            level.rect.collidepoint(event.pos)):
                        for l in self.levels:
                            if l.status == 'selected':
                                l.change_status('opened')
                        level.change_status('selected')
                        break
        elif event.type == pg.MOUSEMOTION:
            if self.hovered_button and not self.hovered_button.rect.collidepoint(
                event.pos
            ):
                self.hovered_button.change_color(self.color_opened)
                self.hovered_button = None
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    self.hovered_button = button
                    self.hovered_button.change_color(self.color_hovered)
            for level in self.levels:
                if level.status == 'hovered':
                    if level.rect.collidepoint(event.pos):
                        break
                    else:
                        level.change_status('opened')
                else:
                    if (level.status == 'opened' and
                            level.rect.collidepoint(event.pos)):
                        level.change_status('hovered')

    def draw(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.frame_image, self.frame_rect)
        screen.blit(self.menu_image, self.menu_rect)
        screen.blit(self.choose_frame_image, self.choose_frame_rect)
        screen.blit(self.choose_image, self.choose_rect)
        screen.blit(*self.title)
        screen.blit(*self.choose)
        for level in self.levels:
            level.draw(screen)
        for button in self.buttons:
            screen.blit(button.image, button.rect)

    def update(self, screen, keys, current_time, time_delta):
        self.current_time = current_time
        self.draw(screen)
