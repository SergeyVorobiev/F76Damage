from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


def projectile_listener(unit: bytes):
    look_values_for_id(unit, '0007cab1', (1.7, 1.8), False)


def look_values_for_id(unit, idd, min_max, include_zeroes):
    idd_ = F76AInst.get_id(unit)
    if idd == idd_:
        print(F76AInst.get_name(unit), idd)
        g_n = F76GroupParser.parse_groups(unit, min_max, include_zeroes)
        print(g_n)


def look_values_by_index(unit: bytes, ids: [], group: bytes, fmt: str, index):
    idd = F76AInst.get_id(unit)
    if ids.__contains__(idd):
        print(F76AInst.get_name(unit), idd)
        print(F76GroupParser.get_from_group_by_index(F76GroupParser.parse_groups(unit), group, fmt, index))


def weapon_listener(unit: bytes):
    print(F76AInst.get_id(unit), F76AInst.get_name(unit))
