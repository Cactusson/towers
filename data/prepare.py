"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import sys
import pygame as pg

from . import tools


ORIGINAL_CAPTION = "Towers v 1.0"


# Initialization
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION) 
DISPLAYINFO = pg.display.Info()
WINDOWWIDTH = DISPLAYINFO.current_w
WINDOWHEIGHT = DISPLAYINFO.current_h
SCREEN_SIZE = (WINDOWWIDTH, WINDOWHEIGHT)
SCREEN = pg.display.set_mode(SCREEN_SIZE, 0)
FLAGS = SCREEN.get_flags()
SCREEN_RECT = SCREEN.get_rect()

if getattr(sys, 'frozen', False):
    # The application is frozen
    path = os.path.join(os.path.dirname(sys.executable), 'fonts')
else:
    # The application is not frozen
    path = os.path.join("resources", "fonts")

FONTS = tools.load_all_fonts(path)


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("resources", "graphics")
    GFX = {}
    for directory in directories:
        if getattr(sys, 'frozen', False):
            path = os.path.join(os.path.dirname(sys.executable), 'graphics',
                                directory)
        else:
            path = os.path.join(base_path, directory)
        GFX[directory] = tools.load_all_gfx(path)
    return GFX

_SUB_DIRECTORIES = ['decor', 'icons', 'misc', 'monsters', 'terrain',
                    'tower_buttons', 'towers']
GFX = graphics_from_directories(_SUB_DIRECTORIES)
