import struct
from enum import Enum


class UCat(Enum):
    RGW35 = {
        'data': {
            'ID': lambda unit: hex(struct.unpack('<L', unit[12:16])[0])[2:].zfill(8),
            "NAME": lambda unit: unit[30:].partition(b'\x00')[0].decode('latin-1'),
            'ANIM_FIRE': ('<f', 5),
            'RUMBLE_L': ('<f', 9),
            'RUMBLE_R': ('<f', 13),
            'RUMBLE_D': ('<f', 17),
            'ANIM_RELOAD': ('<f', 21),
            'SIGHTED_TRANS': ('<f', 29),
            'UNSIGHTED_TRANS': ('<f', 33)
        },
        'segment': b'RGW35'
    }

    DNAM = {
        'data': {
            'SPEED': ("<f", 6),
            'ATTACK_DELAY': ('<f', 38),
            'CAPACITY': ('<H', 66),
            'WEIGHT': ('<f', 75),
            'ATTACK_SPEED': ('<f', 122),
            'AP': ('<f', 128),

        },
        'segment': b'DNAM'
    }
