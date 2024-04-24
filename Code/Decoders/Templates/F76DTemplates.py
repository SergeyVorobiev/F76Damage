from enum import Enum

from Code.Decoders.Categories.UCat import UCat
from Code.Keys.GroupKey import GroupKey


class F76DecTemplates(Enum):
    WEAPON = {
        'start_key': GroupKey.F76_WEAPON,
        'end_key': GroupKey.F76_GRUP,
        'categories': [UCat.RGW35, UCat.DNAM],
        'max_unit_length': 3000,
        'size_func': None,
        'filter_func': None,
    }

    PROJECTILES = {
        'start_key': GroupKey.F76_PROJ,
        'end_key': GroupKey.F76_GRUP,
        'categories': [],
        'max_unit_length': 3000,
        'size_func': None,
        'filter_func': None,
    }

    OMOD_WEAP = {
        'start_key': GroupKey.F76_OMOD,
        'end_key': GroupKey.F76_GRUP,
        'categories': [],
        'max_unit_length': 3000,
        'size_func': None,
        'filter_func': lambda unit: unit.find(b'\x00WEAP') > -1,
    }

    CURVE = {
        'start_key': GroupKey.F76_CURV,
        'end_key': GroupKey.F76_GRUP,
        'categories': [],
        'max_unit_length': 3000,
        'size_func': None,
        'filter_func': None,
    }

    DMGT = {
        'start_key': GroupKey.F76_DMGT,
        'end_key': GroupKey.F76_GRUP,
        'categories': [],
        'max_unit_length': 3000,
        'size_func': None,
        'filter_func': None,
    }
