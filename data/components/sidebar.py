import pygame as pg

from .. import prepare
from ..components.data import monsters_kinds


class MonsterImage(pg.sprite.Sprite):
    """
    Class for just an image of monster, that can't do shit.
    """
    def __init__(self, kind):
        pg.sprite.Sprite.__init__(self)
        self.kind = kind
        self.name = monsters_kinds[self.kind]['name']
        self.image = monsters_kinds[self.kind]['image_right']
        self.speed = monsters_kinds[self.kind]['speed']
        self.health = monsters_kinds[self.kind]['health']

    # why these placeholders?
    # well, it is because of game.change_selection method.
    # yeah, this code is shit.
    def select(self, game):
        pass

    def unselect(self, game):
        pass


class Sidebar():
    """
    Class for sidebar, that's actually on top, not on the side.
    It is divided into three zones that are working independantly.
    """
    def __init__(self):
        """
        Init common stuff + call init functions for all three zones.
        """
        self.monsters_images = pg.sprite.Group()
        self.font_23 = pg.font.Font(prepare.FONTS['Timeless-Bold'], 23)
        self.font_20 = pg.font.Font(prepare.FONTS['Timeless'], 20)
        self.font_18 = pg.font.Font(prepare.FONTS['Timeless'], 18)
        self.bold_font = pg.font.Font(prepare.FONTS['Timeless-Bold'], 17)
        self.font_15 = pg.font.Font(prepare.FONTS['Timeless'], 15)

        self.init_left_zone()
        self.init_middle_zone()
        self.init_right_zone()

    def init_left_zone(self):
        """
        In the left zone we have headline of the wave and monsters' info.
        """
        self.left_zone_rect = pg.rect.Rect(0, 0, 275, 80)
        self.left_zone_image = pg.Surface(self.left_zone_rect.size).convert()
        self.left_zone_image.fill(pg.Color('#82A6CB'))
        self.left_zone_bottom_rect = pg.rect.Rect(0, 70, 265, 10)
        self.left_zone_bottom_image = pg.Surface(
            self.left_zone_bottom_rect.size).convert()
        self.left_zone_bottom_image.fill(pg.Color('#3667A6'))
        self.left_zone_side_rect = pg.rect.Rect(265, 50, 10, 30)
        self.left_zone_side_image = pg.Surface(
            self.left_zone_side_rect.size).convert()
        self.left_zone_side_image.fill(pg.Color('#3667A6'))

        self.headline_pos = (40, 10)
        self.monsters_pos = (20, 40)

    def init_middle_zone(self):
        """
        In the middle zone we have timer, gold and lives.
        """
        self.middle_zone_rect = pg.rect.Rect(275, 0, 225, 60)
        self.middle_zone_image = pg.Surface(
            self.middle_zone_rect.size).convert()
        self.middle_zone_image.fill(pg.Color('#82A6CB'))
        self.middle_zone_bottom_rect = pg.rect.Rect(275, 50, 225, 10)
        self.middle_zone_bottom_image = pg.Surface(
            self.middle_zone_bottom_rect.size).convert()
        self.middle_zone_bottom_image.fill(pg.Color('#3667A6'))

        self.timer_image = prepare.GFX['icons']['timer']
        self.gold_image = prepare.GFX['icons']['gold']
        self.lives_image = prepare.GFX['icons']['lives']
        self.timer_image_pos = (275, 10)
        self.timer_image_rect = self.timer_image.get_rect(
            topleft=self.timer_image_pos)
        self.timer_text_pos = (275+32+3, 20)
        self.gold_image_pos = (375, 10)
        self.gold_image_rect = self.gold_image.get_rect(
            topleft=self.gold_image_pos)
        self.gold_text_pos = (375+32+3, 20)
        self.lives_image_pos = (450, 10)
        self.lives_image_rect = self.lives_image.get_rect(
            topleft=self.lives_image_pos)
        self.lives_text_pos = (450+32+3, 20)

    def init_right_zone(self):
        """
        In the right zone there's info about currently selected tower/monster.
        """
        self.right_zone_rect = pg.rect.Rect(500, 0, 300, 80)
        self.right_zone_image = pg.Surface(self.right_zone_rect.size).convert()
        self.right_zone_image.fill(pg.Color('#82A6CB'))
        self.right_zone_bottom_rect = pg.rect.Rect(500, 70, 800, 10)
        self.right_zone_bottom_image = pg.Surface(
            self.right_zone_bottom_rect.size).convert()
        self.right_zone_bottom_image.fill(pg.Color('#3667A6'))
        self.right_zone_side_rect = pg.rect.Rect(500, 50, 10, 30)
        self.right_zone_side_image = pg.Surface(
            self.right_zone_side_rect.size).convert()
        self.right_zone_side_image.fill(pg.Color('#3667A6'))

        self.selected_tower = None
        self.selected_monster = None
        self.tower_attack_image = prepare.GFX['icons']['tower_damage']
        self.tower_cooldown_image = prepare.GFX['icons']['tower_cooldown']
        self.monster_health_image = prepare.GFX['icons']['monster_health']
        self.monster_speed_image = prepare.GFX['icons']['monster_speed']
        self.selected_image_pos = (510, 10)
        self.selected_name_pos = (570, 7)
        self.selected_info_pos = (570, 30)
        self.selected_description_pos = (570, 50)

    def update_wave_info(self, headline, monsters_list):
        """
        Update wave_info, number of wave + number/images of monsters.
        """
        self.monsters_images.empty()
        self.monsters_list = []
        self.headline_text = self.font_23.render(
            headline, True, pg.Color('black'))
        self.headline_rect = self.headline_text.get_rect(
            topleft=self.headline_pos)
        pos = list(self.monsters_pos)
        for (num, kind) in monsters_list:
            number_text = self.font_20.render(num, True, pg.Color('black'))
            number_rect = number_text.get_rect(topleft=pos)
            pos[0] += number_rect.width + 10
            monster = MonsterImage(kind)
            monster.rect = monster.image.get_rect(topleft=pos)
            self.monsters_images.add(monster)
            pos[0] += monster.rect.width + 10
            self.monsters_list.append(
                ((number_text, number_rect), (monster.image, monster.rect)))

    def update_timer(self, time_string):
        """
        Gets time_string which is just a string as "00:00" or "00:10"
        and renders it into self.timer_text + self.time_rect.
        """
        self.timer_text = self.font_18.render(
            time_string, True, pg.Color('black'))
        self.timer_text_rect = self.timer_text.get_rect(
            topleft=self.timer_text_pos)

    def update_gold(self, gold):
        """
        When money's amount is changed, we call this function.
        Probably not very efficient way.
        """
        self.gold_text = str(gold)
        self.gold_text = self.font_18.render(
            self.gold_text, True, pg.Color('black'))
        self.gold_text_rect = self.gold_text.get_rect(
            topleft=self.gold_text_pos)

    def update_lives(self, lives):
        """
        The same as with gold, but with money.
        """
        self.lives_text = str(lives)
        self.lives_text = self.font_18.render(
            self.lives_text, True, pg.Color('black'))
        self.lives_text_rect = self.lives_text.get_rect(
            topleft=self.lives_text_pos)

    def clear(self):
        """
        Clears selection.
        """
        self.selected_tower = None
        self.selected_monster = None

    def update_selection(self, game, obj):
        """
        If object is given, makes it selected to draw in right zone.
        """
        self.clear()
        if obj:
            if obj in game.towers:
                self.selected_tower = obj
                self.update_selection_tower(self.selected_tower)
            elif obj in game.monsters:
                self.selected_monster = obj
                self.update_selection_monster(self.selected_monster)
            elif obj in self.monsters_images:
                self.selected_monster = obj
                self.update_selection_monster(self.selected_monster, False)

    def update_selection_tower(self, tower):
        """
        Updates all the variables about tower.
        (image, name, level, damage, cooldown, description)
        """
        self.tower_image = tower.image
        self.tower_image_rect = self.tower_image.get_rect(
            topleft=self.selected_image_pos)

        pos = list(self.selected_name_pos)
        self.tower_name = self.bold_font.render(
            tower.name, True, pg.Color('black'))
        self.tower_name_rect = self.tower_name.get_rect(topleft=pos)
        pos[0] += self.tower_name_rect.width + 10

        level = '[{}]'.format(tower.level)
        self.tower_level = self.font_15.render(level, True, pg.Color('black'))
        self.tower_level_rect = self.tower_level.get_rect(topleft=pos)

        if tower.role == 'attack':
            pos = list(self.selected_info_pos)
            self.tower_attack_image_rect = self.tower_attack_image.get_rect(
                topleft=pos)
            pos[0] += self.tower_attack_image_rect.width + 3

            damage = str(tower.damage)
            self.tower_damage = self.font_15.render(
                damage, True, pg.Color('black'))
            self.tower_damage_rect = self.tower_damage.get_rect(topleft=pos)

            if tower.bonus_damage:
                pos[0] += self.tower_damage_rect.width
                bonus_damage = ' + {}'.format((str(tower.bonus_damage)))
                self.tower_bonus_damage = self.font_15.render(
                    bonus_damage, True, pg.Color('darkgreen'))
                self.tower_bonus_damage_rect = \
                    self.tower_bonus_damage.get_rect(topleft=pos)
                pos[0] += self.tower_bonus_damage_rect.width + 10
            else:
                pos[0] += self.tower_damage_rect.width + 10

            self.tower_cooldown_image_rect = \
                self.tower_cooldown_image.get_rect(topleft=pos)
            pos[0] += self.tower_cooldown_image_rect.width + 3

            cooldown = (str(tower.cooldown / 1000))
            self.tower_cooldown = self.font_15.render(
                cooldown, True, pg.Color('black'))
            self.tower_cooldown_rect = self.tower_cooldown.get_rect(
                topleft=pos)

        pos = list(self.selected_description_pos)
        self.tower_description = self.font_15.render(
            tower.description, True, pg.Color('black'))
        self.tower_description_rect = self.tower_description.get_rect(
            topleft=pos)

    def update_selection_monster(self, monster, real=True):
        """
        Updates all the variables about monster.
        (image, name, health, speed)
        real is True, when it is monster and False when it's monster_image.
        """
        self.monster_image = monster.image
        self.monster_image_rect = self.monster_image.get_rect(
            topleft=self.selected_image_pos)

        pos = list(self.selected_name_pos)
        self.monster_name = self.bold_font.render(
            monster.name, True, pg.Color('black'))
        self.monster_name_rect = self.monster_name.get_rect(topleft=pos)

        pos = list(self.selected_info_pos)
        self.monster_health_image_rect = self.monster_health_image.get_rect(
            topleft=pos)
        pos[0] += self.monster_health_image_rect.width + 3

        if real:
            health = '{}/{}'.format(
                str(monster.current_health), str(monster.health))
        else:
            health = str(monster.health)
        self.monster_health = self.font_15.render(
            health, True, pg.Color('black'))
        self.monster_health_rect = self.monster_health.get_rect(topleft=pos)
        pos[0] += self.monster_health_rect.width + 10

        self.monster_speed_image_rect = \
            self.monster_speed_image.get_rect(topleft=pos)
        pos[0] += self.monster_speed_image_rect.width + 3

        speed = (str(monster.speed))
        self.monster_speed = self.font_15.render(
            speed, True, pg.Color('black'))
        self.monster_speed_rect = self.monster_speed.get_rect(
            topleft=pos)

        if real and monster.bonus_speed:
            pos[0] += self.monster_speed_rect.width
            bonus_speed = ' {}'.format((str(monster.bonus_speed)))
            self.monster_bonus_speed = self.font_15.render(
                bonus_speed, True, pg.Color('darkred'))
            self.monster_bonus_speed_rect = \
                self.monster_bonus_speed.get_rect(topleft=pos)

        self.selected_monster_real = real

    def draw(self, screen):
        """
        Draws all the parts of the sidebar.
        """
        self.draw_left_zone(screen)
        self.draw_middle_zone(screen)
        self.draw_right_zone(screen)

    def draw_left_zone(self, screen):
        """
        On the left zone we have wave headline + info about monsters.
        """
        screen.blit(self.left_zone_image, self.left_zone_rect)
        screen.blit(self.left_zone_bottom_image, self.left_zone_bottom_rect)
        screen.blit(self.left_zone_side_image, self.left_zone_side_rect)

        screen.blit(self.headline_text, self.headline_rect)
        for ((number_text, number_rect), (monster_image, monster_rect)) in \
                self.monsters_list:
            screen.blit(number_text, number_rect)
            screen.blit(monster_image, monster_rect)

    def draw_middle_zone(self, screen):
        """
        In the middle there are timer, gold and lives.
        """
        screen.blit(self.middle_zone_image, self.middle_zone_rect)
        screen.blit(
            self.middle_zone_bottom_image, self.middle_zone_bottom_rect)

        screen.blit(self.timer_image, self.timer_image_rect)
        screen.blit(self.timer_text, self.timer_text_rect)
        screen.blit(self.gold_image, self.gold_image_rect)
        screen.blit(self.gold_text, self.gold_text_rect)
        screen.blit(self.lives_image, self.lives_image_rect)
        screen.blit(self.lives_text, self.lives_text_rect)

    def draw_right_zone(self, screen):
        """
        On the right we have info about currently selected tower/monster.
        """
        screen.blit(self.right_zone_image, self.right_zone_rect)
        screen.blit(self.right_zone_bottom_image, self.right_zone_bottom_rect)
        screen.blit(self.right_zone_side_image, self.right_zone_side_rect)

        if self.selected_tower:
            screen.blit(self.tower_image, self.tower_image_rect)
            screen.blit(self.tower_name, self.tower_name_rect)
            screen.blit(self.tower_level, self.tower_level_rect)
            if self.selected_tower.role == 'attack':
                screen.blit(
                    self.tower_attack_image, self.tower_attack_image_rect)
                screen.blit(self.tower_damage, self.tower_damage_rect)
                if self.selected_tower.bonus_damage:
                    screen.blit(
                        self.tower_bonus_damage, self.tower_bonus_damage_rect)
                screen.blit(
                    self.tower_cooldown_image, self.tower_cooldown_image_rect)
                screen.blit(self.tower_cooldown, self.tower_cooldown_rect)
            screen.blit(self.tower_description, self.tower_description_rect)
        elif self.selected_monster:
            screen.blit(self.monster_image, self.monster_image_rect)
            screen.blit(self.monster_name, self.monster_name_rect)
            screen.blit(
                self.monster_health_image, self.monster_health_image_rect)
            screen.blit(self.monster_health, self.monster_health_rect)
            screen.blit(
                self.monster_speed_image, self.monster_speed_image_rect)
            screen.blit(self.monster_speed, self.monster_speed_rect)
            if self.selected_monster_real and self.selected_monster.bonus_speed:
                screen.blit(self.monster_bonus_speed,
                            self.monster_bonus_speed_rect)
