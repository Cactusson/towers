"""
All the data is here. Info about towers, monsters, levels.
Easy to change something and test things.
"""


from .. import prepare


tower_kinds = {
    'regular': {
        'name': 'Regular Tower',
        'description': ('', ''),
        'image_name': ('tower_regular_lvl1', 'tower_regular_lvl2'),
        'role': 'attack',
        'level_cap': 2,
        'price': (10, 15),
        'tower_button_image': 'tower_button_regular',
        'damage': (2, 5),
        'bullet_speed': 7,
        'cooldown': 1000,
        'range': 120,
        'effects': ([], [])},
    'sniper': {
        'name': 'Sniper Tower',
        'description': ('', ''),
        'image_name': ('tower_sniper_lvl1', 'tower_sniper_lvl2'),
        'role': 'attack',
        'level_cap': 2,
        'price': (15, 20),
        'tower_button_image': 'tower_button_sniper',
        'damage': (6, 14),
        'bullet_speed': 12,
        'cooldown': 2500,
        'range': 170,
        'effects': ([], [])},
    'slower': {
        'name': 'Slower Tower',
        'description': ('-1 speed', '-2 speed'),
        'image_name': ('tower_slower_lvl1', 'tower_slower_lvl2'),
        'role': 'attack',
        'level_cap': 2,
        'price': (15, 20),
        'tower_button_image': 'tower_button_slower',
        'damage': (1, 2),
        'bullet_speed': 7,
        'cooldown': 2000,
        'range': 120,
        'effects': ([{'slow': {'speed_reduction': 1, 'slow_duration': 5.0}}],
                    [{'slow': {'speed_reduction': 2, 'slow_duration': 5.0}}])},
    'support': {
        'name': 'Support Tower',
        'description': ('+2 damage', '+4 damage'),
        'image_name': ('tower_support_lvl1', 'tower_support_lvl2'),
        'role': 'support',
        'level_cap': 2,
        'price': (20, 25),
        'tower_button_image': 'tower_button_support',
        'bonus_damage': (2, 4),
        'range': 150}
}

# tested up to 7 (speed)

monsters_kinds = {
    'red':  {
        'name': 'Red monster',
        'health': 5,
        'bounty': 2,
        'speed': 2,
        'image_right': prepare.GFX['monsters']['monster_red_right'],
        'image_left': prepare.GFX['monsters']['monster_red_left']},
    'blue': {
        'name': 'Blue monster',
        'health': 10,
        'bounty': 4,
        'speed': 2,
        'image_right': prepare.GFX['monsters']['monster_blue_right'],
        'image_left': prepare.GFX['monsters']['monster_blue_left']},
    'green': {
        'name': 'Green monster',
        'health': 15,
        'bounty': 6,
        'speed': 2,
        'image_right': prepare.GFX['monsters']['monster_green_right'],
        'image_left': prepare.GFX['monsters']['monster_green_left']},
    'purple': {
        'name': 'Purple monster',
        'health': 20,
        'bounty': 8,
        'speed': 3,
        'image_right': prepare.GFX['monsters']['monster_purple_right'],
        'image_left': prepare.GFX['monsters']['monster_purple_left']},
    'black': {
        'name': 'Black monster',
        'health': 30,
        'bounty': 10,
        'speed': 4,
        'image_right': prepare.GFX['monsters']['monster_black_right'],
        'image_left': prepare.GFX['monsters']['monster_black_left']}
}

levels_list = [
    (
        1,
        [(0, 275), (275, 275), (275, 425), (800, 425)],
        [[('red', 3)], [('blue', 3)]],
        [(150, 200), (300, 250), (200, 300), (300, 300), (200, 350),
         (350, 350), (450, 350), (550, 350), (300, 450), (400, 450),
         (650, 450)],
        {'big_bush': [(50, 120), (500, 200), (120, 400), (600, 260)],
         'small_bush': [(82, 120), (400, 500), (630, 280)],
         'big_tree_top': [(450, 40), (500, 50), (530, 70), (590, 60),
                          (630, 75), (680, 80), (730, 30), (770, 100),
                          (300, 90), (70, 450)],
         'small_tree_top': [(550, 130), (590, 140), (630, 155), (680, 140),
                            (720, 150), (680, 230), (740, 240),
                            (770, 250), (330, 95), (170, 420)]},
        30,
        ['regular', 'sniper']
    ),
    (
        2,
        [(0, 425), (225, 425), (225, 325), (375, 325), (375, 275),
         (525, 275), (525, 375), (575, 375), (575, 425), (800, 425)],
        [[('red', 3), ('blue', 3)], [('blue', 3), ('green', 2)]],
        [(150, 450), (150, 350), (200, 250), (250, 350), (300, 250),
         (350, 200), (500, 200), (400, 300), (450, 300), (350, 350),
         (550, 300), (600, 350), (500, 400)],
        {'big_bush': [(50, 300), (420, 190), (340, 400), (600, 260)],
         'small_bush': [(40, 220), (400, 500), (630, 280)],
         'big_tree_top': [(150, 80), (220, 65), (290, 50), (380, 40),
                          (460, 55), (530, 80), (600, 30), (700, 100),
                          (100, 150), (70, 450)],
         'small_tree_top': [(550, 450), (590, 440), (630, 155), (680, 140),
                            (770, 250), (130, 170), (500, 435)]},
        40,
        ['regular', 'sniper', 'slower'],
        'slower'
    ),
    (
        3,
        [(0, 225), (125, 225), (125, 275), (325, 275), (325, 425),
         (425, 425), (425, 475), (625, 475), (625, 325), (800, 325)],
        [[('blue', 4), ('green', 3)], [('green', 6)],
         [('green', 5), ('purple', 3)]],
        [(100, 150), (150, 200), (300, 200), (350, 250), (650, 250),
         (150, 300), (250, 300), (400, 350), (550, 350), (450, 400),
         (550, 400), (350, 450), (450, 500), (600, 500)],
        {'big_bush': [(30, 50), (300, 40), (480, 200), (550, 150),
                      (460, 120), (550, 80), (660, 110), (690, 420)],
         'small_bush': [(500, 130), (600, 125), (100, 500), (190, 440)],
         'big_tree_top': [(470, 240), (550, 200)],
         'small_tree_top': [(420, 120), (50, 350), (130, 410), (250, 60),
                            (370, 80)]},
        50,
        ['regular', 'sniper', 'slower', 'support'],
        'support'
    ),
    (
        4,
        [(0, 425), (275, 425), (275, 275), (475, 275), (475, 425),
         (800, 425)],
        [[('green', 7), ('purple', 5)], [('green', 12), ('purple', 9)],
         [('green', 20), ('purple', 15)]],
        [(250, 200), (400, 200), (200, 250), (300, 300), (350, 300),
         (500, 300), (200, 350), (400, 350), (550, 350), (300, 400),
         (200, 450), (450, 450), (650, 450)],
        {'big_bush': [(50, 285), (90, 475), (600, 500), (660, 100),
                      (580, 200), (660, 220), (620, 300), (570, 290)],
         'small_bush': [(350, 480), (130, 250), (330, 90), (380, 100),
                        (740, 240), (700, 280)],
         'big_tree_top': [(55, 120), (100, 50), (350, 10), (200, 60)],
         'small_tree_top': [(150, 110), (10, 450), (500, 100), (250, 60),
                            (600, 80)]},
        60,
        ['regular', 'sniper', 'slower', 'support']
    ),
    (
        5,
        [(0, 225), (525, 225), (525, 325), (325, 325), (325, 375),
         (275, 375), (275, 475), (800, 475)],
        [[('green', 10), ('purple', 5)],
         [('black', 15)],
         [('black', 30)]],
        [(250, 150), (500, 150), (550, 200), (300, 250), (400, 250),
         (450, 250), (250, 300), (550, 300), (350, 350), (450, 350),
         (200, 400), (300, 400), (400, 400), (550, 400), (600, 400),
         (200, 450), (350, 500), (500, 500)],
        {'big_bush': [(40, 100), (140, 250), (180, 310), (640, 510),
                      (740, 350)],
         'small_bush': [(130, 120), (420, 120), (50, 510), (100, 460),
                        (160, 490), (690, 365)],
         'big_tree_top': [(50, 300), (320, 40), (650, 100)],
         'small_tree_top': [(70, 350), (360, 60), (610, 200), (700, 140),
                            (690, 220)]},
        70,
        ['regular', 'sniper', 'slower', 'support']
    )]

TOTAL_LEVELS = len(levels_list)
