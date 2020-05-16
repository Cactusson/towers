import pygame as pg

from ..components.data import tower_kinds


class Bullet(pg.sprite.Sprite):
    """
    Bullet is a particle that hits monsters.
    """
    def __init__(self, tower, target):
        """
        Where it comes from and it's target.
        We use self.effects and not self.tower.effects because tower's effects
        can change due to upgrade when bullet is still on its path.
        """
        pg.sprite.Sprite.__init__(self)
        self.tower = tower
        self.target = target
        self.effects = self.tower.effects
        self.speed = tower_kinds[self.tower.kind]['bullet_speed']
        self.damage = self.tower.actual_damage
        self.image = pg.Surface((7, 7)).convert()
        self.rect = self.image.get_rect(center=tower.rect.center)

    def check_effects(self, game, target):
        """
        Apply all the effects on the target.
        """
        for effect in self.effects:
            if 'slow' in effect:
                speed_reduction = effect['slow']['speed_reduction']
                slow_duration = effect['slow']['slow_duration']
                target.get_slowed(game, speed_reduction, slow_duration)

    def update(self, game):
        """
        If target's dead, kill itself.
        If the bullet hits its target => deal damage + apply effects.
        Then kill itself.
        Otherwise continue pursuit.
        """
        if not self.target.alive():
            self.kill()
        elif pg.sprite.collide_rect(self, self.target):
            self.kill()
            self.check_effects(game, self.target)
            self.target.current_health -= self.damage
            if self.target.current_health <= 0:
                game.gold += self.target.bounty
                game.sidebar.update_gold(game.gold)
                if game.selected == self.target:
                    game.change_selection()
                self.target.kill()
            else:
                if self.target == game.sidebar.selected_monster:
                    game.sidebar.update_selection_monster(
                        game.sidebar.selected_monster)
        else:
            if self.target.rect.centerx <= self.rect.centerx:
                dx = -self.speed
            else:
                dx = self.speed
            if self.target.rect.centery <= self.rect.centery:
                dy = -self.speed
            else:
                dy = self.speed
            if (abs(self.target.rect.centerx - self.rect.centerx) <
                    abs(self.target.rect.centery - self.rect.centery)):
                dx = dx // 2
            else:
                dy = dy // 2
            self.rect.x += dx
            self.rect.y += dy
