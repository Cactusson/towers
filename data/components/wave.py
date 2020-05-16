from ..components.monster import Monster


class Wave():
    """
    Waves are groups of monsters that are coming together.
    """
    def __init__(self, level, number, monsters_list):
        """
        Info about monsters are in monsters_list, it looks like this:
        [('red', 5), ('blue', 10)].
        """
        self.level = level
        self.monsters_list = monsters_list
        self.number = number
        self.total_number = len(self.level.waves_list)
        self.timer_pre = 0.0
        self.timer_post = 0.0
        self.timer_spawn = 0.0
        self.delay_pre = 15000
        self.delay_post = 3000
        self.delay_spawn = 1000
        self.monsters = []
        self.alive_monsters = []
        self.phase = 'inactive'
        self.done = False
        self.started = False
        self.spawning = False
        self.ready_to_spawn = False
        self.time_string = "00:00"

    def kickstart(self, game):
        """
        Creates monsters in self.monsters and sets phase to 'pre'.
        """
        self.phase = 'pre'
        self.timer_pre = game.actual_time
        for (kind, num) in self.monsters_list:
            for _ in range(num):
                self.monsters.append(Monster(self.level.points, kind))
        headline, monsters_list = self.get_wave_info()
        game.sidebar.update_wave_info(headline, monsters_list)

    def pre_timer_go(self, now, game):
        """
        Before wave starts there is a timer of 15 seconds going.
        """
        if now - self.timer_pre > self.delay_pre:
            self.phase = 'go'
            self.spawning = True
            self.ready_to_spawn = True
            self.time_string = "00:00"
            self.timer_spawn = now
        else:
            self.time_string = str(self.delay_pre - now + self.timer_pre)
            self.time_string = '00:{:02d}'.format(int(int(
                float(self.time_string)) / 1000) + 1)
        game.sidebar.update_timer(self.time_string)

    def monsters_go(self, now, game):
        """
        The main phase: spawning monsters and waiting for them to die or
        reach to the end (actually they still die there as well).
        """
        if self.monsters and self.spawning:
            if self.ready_to_spawn:
                self.spawn_monster(game)
                self.ready_to_spawn = False
                if not self.monsters:
                    self.spawning = False
                else:
                    self.timer_spawn = now
            else:
                if now - self.timer_spawn > self.delay_spawn:
                    self.ready_to_spawn = True

        self.alive_monsters = [monster for monster in self.alive_monsters
                               if monster.alive()]
        if not (self.monsters or self.alive_monsters):
            self.phase = 'post'
            self.timer_post = now

    def post_timer_go(self, now, game):
        """
        When wave is done for, let's wait 3 seconds just for fun.
        """
        if now - self.timer_post > self.delay_post:
            self.phase = 'finished'
            self.done = True

    def spawn_monster(self, game):
        """
        Creates a single monster!
        """
        monster = self.monsters.pop(0)
        self.alive_monsters.append(monster)
        game.monsters.add(monster)

    def get_wave_info(self):
        """
        text_headline, [(monster_number, monster_kind), ...]
        text_headline = 'Wave 1/3'
        """
        text_headline = 'Wave {}/{}: '.format(self.number, self.total_number)
        monsters_info = []
        # this here has to be changed. It's really bad. Here and in sidebar.
        for (kind, num) in self.monsters_list:
            monsters_info.append((str(num), kind))
        return text_headline, monsters_info

    def update(self, game):
        """
        Three phases of wave and their functions.
        """
        now = game.actual_time
        # self.set_wave_info()
        if self.phase == 'pre':
            self.pre_timer_go(now, game)
        elif self.phase == 'go':
            self.monsters_go(now, game)
        elif self.phase == 'post':
            self.post_timer_go(now, game)
