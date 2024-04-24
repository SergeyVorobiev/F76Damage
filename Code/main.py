from Code.Decoders.BaseDecoder import BaseDecoder
from Code.Decoders.Templates.F76DTemplates import F76DecTemplates
from Code.Helpers import Printing
from Code.Helpers.F76Analyzer import weapon_listener

from Code.Keys.GamePaths import GPaths

from Code.Units.UnitSeparator import UnitSeparator


# > - big-endian
# < - little-endian
# print(sys.byteorder)

# x - pad byte
# c - char (1 byte)
# b - signed char (1 byte)
# B - unsigned char (1 byte)
# ? - bool (1 byte)
# h - short (2 bytes)
# H - unsigned short (2 bytes)
# i - int (4 bytes)
# I - unsigned int (4 bytes)
# l - long (4 bytes)
# L - unsigned long (4 bytes)
# q - long long (8 bytes)
# Q - unsigned long long (8 bytes)
# f - float (4 bytes)
# d - double (4 bytes)
# s - char[] (n bytes)


def analyzer():
    decoders = [BaseDecoder(F76DecTemplates.CURVE).listen(weapon_listener, True)]
    UnitSeparator.separate_and_decode_file(GPaths.F76_MASTER, decoders)
    UnitSeparator.separate_and_decode_file(GPaths.F76_NW, decoders)


def esm_search():
    decoders = [BaseDecoder(F76DecTemplates.WEAPON).print_result(Printing.cprint_f76_weapon)]
    UnitSeparator.separate_and_decode_file(GPaths.F76_MASTER, decoders)
    UnitSeparator.separate_and_decode_file(GPaths.F76_NW, decoders)


if __name__ == '__main__':
    analyzer()
    # esm_search()
