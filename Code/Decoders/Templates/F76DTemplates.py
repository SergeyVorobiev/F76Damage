from enum import Enum

from Code.Decoders.Categories.UCat import UCat
from Code.Helpers.F76AInst import F76AInst
from Code.Keys.GroupKey import GroupKey


def get_size(unit):
    return F76AInst.get_ushort(unit, 4) + len(unit) - 4


def get_default(key, length=5000):
    return {
        'start_key': key,
        'end_key': GroupKey.F76_GRUP,
        'categories': [],
        'max_unit_length': length,
        'size_func': get_size,
        'filter_func': None,
    }


class F76DecTemplates(Enum):
    WEAPON = {
        'start_key': GroupKey.F76_WEAPON,
        'end_key': GroupKey.F76_GRUP,
        'categories': [UCat.RGW3, UCat.DNAM, UCat.FULL, UCat.KWDA, UCat.OBTS, UCat.ETYP, UCat.APPR, UCat.EILV,
                       UCat.CVT0, UCat.CRDT, UCat.EITM],
        'max_unit_length': 3000,
        'size_func': get_size,
        'filter_func': None,
    }

    OMOD_WEAP = {
        'start_key': GroupKey.F76_OMOD,
        'end_key': GroupKey.F76_GRUP,
        'categories': [],
        'max_unit_length': 3000,
        'size_func': get_size,
        'filter_func': lambda unit: unit.find(b'\x00WEAP') > -1,
    }

    PROJECTILES = get_default(GroupKey.F76_PROJ)

    ENCHANTMENTS = get_default(GroupKey.F76_ENCH)

    HAZARDS = get_default(GroupKey.F76_HAZD)

    ALCHEMY = get_default(GroupKey.F76_ALCH)

    MSTT = get_default(GroupKey.F76_MSTT, length=10000)

    MGEF = get_default(GroupKey.F76_MGEF)

    CURVE = get_default(GroupKey.F76_CURV)

    AVIF = get_default(GroupKey.F76_AVIF, length=30000)

    AMMO = get_default(GroupKey.F76_AMMO)

    GLOB = get_default(GroupKey.F76_GLOB)

    EQUP = get_default(GroupKey.F76_EQUP)

    KYWD = get_default(GroupKey.F76_KYWD)

    DMGT = get_default(GroupKey.F76_DMGT)

    EXPL = get_default(GroupKey.F76_EXPL)

    PERK = get_default(GroupKey.F76_PERK, 10000)

    SPEL = get_default(GroupKey.F76_SPEL)
