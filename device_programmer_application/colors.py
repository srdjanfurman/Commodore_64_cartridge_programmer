"""
Created on Sep 15, 2014

@author: sfurman
"""


# Terminal color palette.
class Color(object):
    def __init__(self):
        pass

    TEXT_RESET_ALL = '\033[0m'
    TEXT_RESET = '\033[39m'  # '\033[49m'
    TEXT_BLACK = '\033[30m'
    TEXT_RED = '\033[31m'
    TEXT_GREEN = '\033[32m'
    TEXT_YELLOW = '\033[33m'
    TEXT_BLUE = '\033[34m'
    TEXT_MAGENTA = '\033[35m'
    TEXT_CYAN = '\033[36m'
    TEXT_WHITE = '\033[37m'
    TEXT_BRIGHT = '\033[1m'
    TEXT_NORMAL = '\033[22m'
    BACKGROUND_BLACK = '\033[40m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_YELLOW = '\033[43m'  # olive
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_MAGENTA = '\033[45m'  # purple
    BACKGROUND_CYAN = '\033[46m'  # light blue
    BACKGROUND_WHITE = '\033[47m'  # grey

# ANSI sequences that 'colorama' converts into win32 calls.

# TEXT:
# ESC [ 0 m       # Reset all (colors and brightness)
# ESC [ 1 m       # Bright
# ESC [ 2 m       # Dim (looks same as normal brightness)
# ESC [ 22 m      # Normal brightness

# FOREGROUND:
# ESC [ 30 m      # Black
# ESC [ 31 m      # Red
# ESC [ 32 m      # Green
# ESC [ 33 m      # Yellow
# ESC [ 34 m      # Blue
# ESC [ 35 m      # Magenta
# ESC [ 36 m      # Cyan
# ESC [ 37 m      # White
# ESC [ 39 m      # Reset

# BACKGROUND:
# ESC [ 40 m      # Black
# ESC [ 41 m      # Red
# ESC [ 42 m      # Green
# ESC [ 43 m      # Yellow
# ESC [ 44 m      # Blue
# ESC [ 45 m      # Magenta
# ESC [ 46 m      # Cyan
# ESC [ 47 m      # White
# ESC [ 49 m      # Reset

# Cursor positioning:
# ESC [ y;x H     # Position cursor at x across, y down.

# Clear the screen:
# ESC [ mode J    # Clear the screen. Only mode 2 (clear entire screen)
#                   is supported.
