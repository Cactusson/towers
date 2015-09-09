"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare, tools
from .states import intro, game, win_screen, choose_level


def main():
    """
    Add states to control here.
    """
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {'INTRO': intro.Intro(),
                  'GAME': game.Game(),
                  'WIN_SCREEN': win_screen.WinScreen(),
                  'CHOOSE_LEVEL': choose_level.ChooseLevel()}
    run_it.setup_states(state_dict, 'INTRO')
    run_it.main()
