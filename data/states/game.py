"""
The class for our Game scene is found here.
"""


import pygame as pg

from .. import prepare, tools
from ..components.data import tower_kinds, levels_list, TOTAL_LEVELS
from ..components.tower import Tower
from ..components.level import Level
from ..components.subtitle import Subtitle
from ..components.sidebar import Sidebar
from ..components.menu_screen import MenuScreen


class Game(tools._State):
    """
    State of the game.
    """
    def __init__(self):
        """
        Here we create a bunch of stuff.
        """
        tools._State.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.pause_button = prepare.GFX['misc']['pause']
        self.pause_button_rect = self.pause_button.get_rect(
            bottomright=(790, 590))
        self.move_on = True
        self.sidebar = Sidebar()
        self.foundations = pg.sprite.Group()
        self.tower_buttons = pg.sprite.Group()
        self.towers = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.ground_tiles = pg.sprite.Group()
        self.tooltip = None  # (tower_button, its base's rect)
        self.set_screens()
        self.current_level = None
        self.wave_in_progress = None
        self.selected = None
        self.set_levels()
        self.bg = self.tile_surface(
            prepare.SCREEN_SIZE, prepare.GFX['terrain']['ground'])

    def set_levels(self):
        """
        Get info from components.data about levels and create them.
        """
        self.levels = []
        for level in levels_list:
            self.levels.append(Level(*level))

    def set_screens(self):
        """
        Sets menu_screen, lost_screen and won_screen.
        They appear on the screen, when player pauses the game,
        loses or wins.
        """
        buttons_list = [('RESUME', (0, 75), self.action_resume),
                        ('RESTART', (0, 150), self.action_restart),
                        ('QUIT', (0, 225), self.action_quit)]
        self.menu_screen = MenuScreen(buttons_list)

        text_list = [('You lost! :(', (0, 60))]
        buttons_list = [('RESTART', (0, 160), self.action_restart),
                        ('QUIT', (0, 235), self.action_quit)]
        self.lost_screen = MenuScreen(buttons_list, text_list)

        text_list = [('You won! :D', (0, 60))]
        buttons_list = [('AWESOME!', (0, 215), self.action_win)]
        self.won_screen = MenuScreen(buttons_list, text_list)

    def kickstart_screens(self):
        """
        Call kickstart method of all the screens.
        """
        self.menu_screen.kickstart()
        self.lost_screen.kickstart()
        self.won_screen.kickstart()

    def set_tip_screen(self, new_tower):
        """
        Sets tip screen, where it's shown that a new tower is unlocked.
        """
        tower_name = tower_kinds[new_tower]['name']
        text_list = [(tower_name, (0, 60)),
                     ('is unlocked!'.format(tower_name), (0, 95))]
        buttons_list = [('OK', (0, 190), self.action_ok)]
        self.tip_screen = MenuScreen(buttons_list, text_list)

    def tile_surface(self, size, tile):
        """
        Fill a surface of the given size with a surface tile.
        """
        surface = pg.Surface(size).convert()
        tile_size = tile.get_size()
        for i in range(0, tile_size[0]+size[0], tile_size[0]):
            for j in range(0, tile_size[1]+size[1], tile_size[1]):
                surface.blit(tile, (i, j))
        return surface

    def start_level(self, level_index):
        """
        Gets an index of a level and starts this level.
        """
        self.time_offset = 0.0
        self.current_level = self.levels[level_index]
        self.gold = self.current_level.starting_gold
        self.lives = 3
        self.sidebar.update_gold(self.gold)
        self.sidebar.update_lives(self.lives)
        self.hovered = None
        self.wave_in_progress = None
        self.change_selection()
        self.current_level.kickstart(self)
        self.kickstart_screens()
        self.unlocked_towers = self.current_level.unlocked_towers
        if self.current_level.new_tower:
            new_tower = self.current_level.new_tower
            self.set_tip_screen(new_tower)
            self.tip_screen.kickstart()
            self.phase = 'tip'
        else:
            self.phase = 'game'
        self.subtitle = Subtitle(level_index+1)

    def clear_everything(self):
        """
        Empties all groups and clears variables.
        """
        self.current_level = None
        self.wave_in_progress = None
        self.foundations.empty()
        self.tower_buttons.empty()
        self.towers.empty()
        self.bullets.empty()
        self.monsters.empty()
        self.hovered = None
        self.change_selection()
        self.sidebar.clear()

    def get_tower_button_rects(self, tower_rect, num, side):
        """
        Returns _num_ rects on _side_ of _tower_rect_.
        They are then used to create TowerButtons.
        """
        width = height = 30
        y_distance = 10
        if num == 1:
            space = 0
            x = tower_rect.left + 10
        elif num == 2:
            space = 20
            x = tower_rect.left - 15
        elif num == 3:
            space = 10
            x = tower_rect.left - 30
        if side == 'top':
            y = tower_rect.top - height - y_distance
        elif side == 'bottom':
            y = tower_rect.bottom + y_distance
        rects = []
        for _ in range(num):
            rect = pg.rect.Rect(x, y, width, height)
            x += width + space
            rects.append(rect)
        return rects

    def build_tower(self, foundation, kind):
        """
        Creates a tower of given kind on given foundation if gold is enough.
        Also tower's kind should be in self.unlocked_towers.
        Probably this method should be in TowerButton or somewhere else.
        """
        self.change_selection()
        if (self.gold >= tower_kinds[kind]['price'][0] and
                kind in self.unlocked_towers):
            self.gold -= tower_kinds[kind]['price'][0]
            self.sidebar.update_gold(self.gold)
            rect = foundation.rect
            foundation.kill()
            self.towers.add(Tower(rect, kind))

    def pause(self):
        """
        Shifts self.phase to 'pause'.
        Other possible phases are 'game', 'lost', 'win' and 'tip'.
        I'm sure there are better ways to do it, something like state_machine
        or whatever.
        """
        self.phase = 'pause'

    def unpause(self):
        """
        When unpause, time_offset is set to be the difference between
        current_time (that was updated during the pause) and actual_time
        (that wasn't).
        """
        self.phase = 'game'
        self.time_offset = self.current_time - self.actual_time

    def startup(self, current_time, persistant):
        """
        Starts accordingly to the previous state.
        """
        self.actual_time = current_time
        self.persist = persistant
        level_index = self.persist['level_index']
        self.start_level(level_index)
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        """
        We should know what level we were on
        + should we move on to the next one or not.
        When we win the level that's last opened, we move on.
        """
        self.done = False
        if self.next in ['CHOOSE_LEVEL', 'LOST']:
            self.persist['level_index'] = self.levels.index(self.current_level)
            self.persist['move_on'] = self.move_on
            self.clear_everything()
        return self.persist

    def get_event(self, event):
        """
        Well, MOUSEBUTTONUP part is somewhat ok-ish, I guess,
        but MOUSEMOTION is really messy. Should have changed that.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.phase == 'game':
                    self.pause()
                elif self.phase == 'pause':
                    self.unpause()
        elif event.type == pg.MOUSEBUTTONUP:
            if self.phase == 'game':
                self.click(event.pos)
            elif self.phase == 'pause':
                self.menu_screen.click(event.pos)
            elif self.phase == 'lost':
                self.lost_screen.click(event.pos)
            elif self.phase == 'won':
                self.won_screen.click(event.pos)
            elif self.phase == 'tip':
                self.tip_screen.click(event.pos)
        elif event.type == pg.MOUSEMOTION:
            if self.phase == 'game':
                for tower_button in self.tower_buttons:
                    if tower_button.rect.collidepoint(event.pos):
                        if self.hovered:
                            self.hovered.unhover(self)
                        self.hovered = tower_button
                        self.hovered.hover(self)
                        break
                else:
                    for foundation in self.foundations:
                        if foundation.rect.collidepoint(event.pos):
                            if self.hovered:
                                self.hovered.unhover(self)
                            self.hovered = foundation
                            self.hovered.hover(self)
                            break
                    else:
                        if self.hovered:
                            self.hovered.unhover(self)
                        self.hovered = None
            elif self.phase == 'pause':
                self.menu_screen.hover(event.pos)
            elif self.phase == 'lost':
                self.lost_screen.hover(event.pos)
            elif self.phase == 'won':
                self.won_screen.hover(event.pos)
            elif self.phase == 'tip':
                self.tip_screen.hover(event.pos)

    def change_selection(self, obj=None):
        """
        Changes self.selected to obj, if no obj is given, sets to None.
        """
        self.hovered = None
        self.sidebar.update_selection(self, obj)
        if self.selected:
            self.selected.unselect(self)
        if obj:
            self.selected = obj
            self.selected.select(self)
        else:
            self.selected = None

    def click(self, pos):
        """
        Function is called when MOUSEBUTTONUP event is detected.
        """
        if self.pause_button_rect.collidepoint(pos):
            self.pause()
            return

        # let's first check if it's a tower_button
        for tower_button in self.tower_buttons:
            if tower_button.rect.collidepoint(pos):
                tower_button.do_action(self)
                return

        # now let's go through everything and select what we caught
        everything = pg.sprite.Group(self.towers,
                                     self.foundations,
                                     self.monsters,
                                     self.sidebar.monsters_images)
        for obj in everything:
            if obj.rect.collidepoint(pos):
                self.change_selection(obj)
                break
        else:
            self.change_selection()

    # actions are for buttons
    def action_ok(self):
        self.unpause()

    def action_resume(self):
        self.unpause()

    def action_restart(self):
        level_index = self.current_level.number - 1
        self.clear_everything()
        self.start_level(level_index)

    def action_quit(self):
        self.next = 'CHOOSE_LEVEL'
        self.move_on = False
        self.done = True

    def action_win(self):
        if self.current_level.number == TOTAL_LEVELS:
            self.next = 'WIN_SCREEN'
        else:
            self.next = 'CHOOSE_LEVEL'
            self.move_on = True
        self.done = True

    def draw(self):
        """
        Blit all elements to surface.
        """
        self.screen.blit(self.bg, (0, 0))
        self.current_level.draw(self.screen)
        self.foundations.draw(self.screen)
        for tower in self.towers:
            tower.draw(self.screen, self)
        self.monsters.draw(self.screen)
        self.bullets.draw(self.screen)
        self.tower_buttons.draw(self.screen)
        if self.hovered in self.tower_buttons:
            self.hovered.draw(self.screen, self)
        self.sidebar.draw(self.screen)
        self.screen.blit(self.pause_button, self.pause_button_rect)
        if self.subtitle:
            self.subtitle.draw(self.screen)

        if self.phase == 'pause':
            self.menu_screen.draw(self.screen)
        elif self.phase == 'lost':
            self.lost_screen.draw(self.screen)
        elif self.phase == 'won':
            self.won_screen.draw(self.screen)
        elif self.phase == 'tip':
            self.tip_screen.draw(self.screen)

    def update(self, surface, keys, current_time, time_delta):
        """
        Updates time and everything else.
        """
        self.current_time = current_time
        if self.phase == 'game':
            self.actual_time = self.current_time - self.time_offset
            if self.subtitle:
                self.subtitle.update(self)
        if self.phase in ['game', 'tip']:
            if self.lives <= 0:
                self.phase = 'lost'
            elif self.current_level.done:
                self.phase = 'won'
            else:
                self.current_level.update(self)
                self.bullets.update(self)
                self.monsters.update(self)
                self.towers.update(self)

                if self.wave_in_progress:
                    self.wave_in_progress.update(self)
        self.draw()
