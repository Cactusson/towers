import pygame as pg

from .. import prepare
from ..components.data import tower_kinds


class TowerButton(pg.sprite.Sprite):
    """
    Button that appears when you click on a tower or hover over foundation,
    sell, choose role or choose tower etc.
    """
    def __init__(self, rect, role, **kwargs):
        """
        Rect of tower/foundation,
        role is 'build', 'show', 'sell', 'upgrade'.
        """
        pg.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pg.Surface(self.rect.size).convert()
        self.image = prepare.GFX['tower_buttons'][kwargs['image_name']]
        self.role = role
        if self.role == 'build':
            self.foundation = kwargs['foundation']
            self.kind = kwargs['kind']
            self.tower_attack_image = prepare.GFX['icons']['tower_damage']
            self.tower_cooldown_image = prepare.GFX['icons']['tower_cooldown']
            self.tower_price_image = prepare.GFX['icons']['tower_price']
        elif self.role == 'show':
            self.foundation = kwargs['foundation']
            self.kinds = kwargs['kinds']
        elif self.role == 'upgrade':
            self.tower = kwargs['tower']
            self.game = kwargs['game']
            self.tower_attack_image = prepare.GFX['icons']['tower_damage']
            self.tower_cooldown_image = prepare.GFX['icons']['tower_cooldown']
            self.tower_price_image = prepare.GFX['icons']['tower_price']
        elif self.role == 'sell':
            self.tower = kwargs['tower']
            self.game = kwargs['game']
        elif self.role == 'locked':
            pass

    def do_action(self, game):
        """
        This function is called when player clicks on tower_button.
        """
        if self.role != 'locked':
            game.tower_buttons.empty()
        if self.role == 'show':
            rects = game.get_tower_button_rects(
                self.foundation.rect, len(self.kinds), 'top')
            for rect, kind in zip(rects, self.kinds):
                if kind in game.unlocked_towers:
                    game.tower_buttons.add(TowerButton(
                        rect, 'build', kind=kind,
                        foundation=self.foundation,
                        image_name=tower_kinds[kind]['tower_button_image']))
                else:
                    game.tower_buttons.add(TowerButton(
                        rect, 'locked', image_name='tower_button_locked'))
        elif self.role == 'build':
            game.build_tower(self.foundation, self.kind)
        elif self.role == 'upgrade':
            self.tower.get_upgrade(self.game)
        elif self.role == 'sell':
            self.tower.sell(self.game)

    def render_text(self, rect, game):
        """
        Returns a list of tuples with (text, rect) for every
        line of info that needs to be drawn on tooltip.
        Location is topleft point of tooltip.
        """
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 15)
        self.bold_font = pg.font.Font(prepare.FONTS['Timeless-Bold'], 17)
        x, y = rect.topleft
        if self.role == 'build':
            kind = self.kind
            level = 0
        elif self.role == 'upgrade':
            kind = self.tower.kind
            level = self.tower.level
        text = []
        tower = tower_kinds[kind]
        name = tower['name']
        text_name = self.bold_font.render(name, True, pg.Color('black'))
        text_name_rect = text_name.get_rect(center=(
            rect.x + rect.width // 2, y+20))
        text.append((text_name, text_name_rect))
        if tower['role'] == 'attack':
            center_pos = list((rect.x + rect.width // 4, y+52))
            damage_image_rect = self.tower_attack_image.get_rect(
                center=center_pos)
            text.append((self.tower_attack_image, damage_image_rect))
            center_pos[0] += damage_image_rect.width + 3

            damage = str(tower['damage'][level])
            text_damage = self.font.render(damage, True, pg.Color('black'))
            text_damage_rect = text_damage.get_rect(center=center_pos)
            text.append((text_damage, text_damage_rect))
            center_pos[0] += text_damage_rect.width + 20

            cooldown_image_rect = self.tower_cooldown_image.get_rect(
                center=center_pos)
            text.append((self.tower_cooldown_image, cooldown_image_rect))
            center_pos[0] += cooldown_image_rect.width + 3

            cooldown = str(tower['cooldown'] / 1000)
            text_cooldown = self.font.render(cooldown, True, pg.Color('black'))
            text_cooldown_rect = text_cooldown.get_rect(center=center_pos)
            text.append((text_cooldown, text_cooldown_rect))

        description = str(tower['description'][level])
        text_description = self.font.render(
            description, True, pg.Color('black'))
        text_description_rect = text_description.get_rect(center=(
            rect.x + rect.width // 2, y+77))
        text.append((text_description, text_description_rect))

        center_pos = list((rect.x + rect.width // 2.5, y+102))
        price_image_rect = self.tower_price_image.get_rect(center=center_pos)
        text.append((self.tower_price_image, price_image_rect))
        center_pos[0] += price_image_rect.width + 3

        price = str(tower['price'][level])
        if game.gold >= int(price):
            color = pg.Color('black')
        else:
            color = pg.Color('red')
        text_price = self.font.render(price, True, color)
        text_price_rect = text_price.get_rect(center=center_pos)
        text.append((text_price, text_price_rect))
        return text

    def get_tooltip(self, game):
        """
        Returns tooltip_rect + text from self.render_text.
        """
        if not (self.role == 'build' or self.role == 'upgrade'):
            return None
        if self.role == 'build':
            rect = self.foundation.rect
        elif self.role == 'upgrade':
            rect = self.tower.rect
        width, height = 170, 120
        if rect.top > 270:
            x, y = rect.left - 65, rect.top - 50 - height
        else:
            x, y = rect.left - 65, rect.top + 10
        tooltip_rect = pg.rect.Rect(x, y, width, height)
        text = self.render_text(tooltip_rect, game)
        return (tooltip_rect, text)

    # some stupid placeholders, why not.
    def hover(self, game):
        pass

    def unhover(self, game):
        pass

    def draw(self, screen, game):
        """
        Draws itself. If hovered, draws tooltip/name.
        """
        screen.blit(self.image, self.rect)
        if game.hovered == self:
            if self.role == 'build':
                if tower_kinds[self.kind]['role'] == 'attack':
                    color = pg.Color('black')
                elif tower_kinds[self.kind]['role'] == 'support':
                    color = pg.Color('#9E7EFF')
                center = self.foundation.rect.center
                radius = tower_kinds[self.kind]['range']
                pg.draw.circle(
                    screen, color, center, radius, 2)
            elif self.role == 'upgrade':
                pg.draw.circle(
                    screen, self.tower.color_range,
                    self.tower.rect.center, self.tower.range, 2)
            tooltip = self.get_tooltip(game)
            if tooltip:
                self.draw_tooltip(screen, tooltip)
            else:
                self.draw_name(screen)

    def draw_tooltip(self, screen, tooltip):
        """
        Draws tooltip.
        """
        rect, text = tooltip
        pg.draw.rect(screen, pg.Color('#F7FA86'), rect)
        for (line, rect) in text:
            screen.blit(line, rect)

    def draw_name(self, screen):
        """
        Draws name near itself like 'attack' or 'sell'.
        """
        font = pg.font.Font(prepare.FONTS['collegiateHeavyOutline Medium'], 20)
        if self.role == 'show':
            name = tower_kinds[self.kinds[0]]['role']
        elif self.role == 'sell':
            name = 'Sell'
        elif self.role == 'locked':
            name = 'Locked'
        name_text = font.render(name, True, pg.Color('black'))
        name_rect = name_text.get_rect(topleft=(
            self.rect.x - 5, self.rect.y - 20))
        screen.blit(name_text, name_rect)
