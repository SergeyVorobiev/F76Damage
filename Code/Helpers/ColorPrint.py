from enum import Enum


class pc(Enum):
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    gray = 37
    b_red = 91
    b_green = 92
    b_yellow = 93
    b_blue = 94
    b_magenta = 95
    b_cyan = 96
    b_gray = 97
    white = 245


def cprint(text, t_color: pc = pc.black, bg_color: pc = pc.white, is_bold=False, end=''):
    print(f'\033[{int(is_bold)};{t_color.value};{bg_color.value + 10}m{text}\033[0m', end=end)


def cprintln(text, t_color: pc = pc.black, bg_color: pc = pc.white, is_bold=False):
    cprint(text, t_color, bg_color, is_bold, end='\n')
