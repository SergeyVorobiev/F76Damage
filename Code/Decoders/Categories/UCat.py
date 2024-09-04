import struct
from enum import Enum

from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


def tags(unit):
    ids = []
    try:
        kwda = F76GroupParser.get_group_segment(unit, b"KWDA")
    except:
        return ids
    for i in range(F76AInst.get_tags_count(unit)):
        ids.append(F76AInst.get_id(kwda, 2 + i * 4))
    return ids


def level(unit):
    levels = []
    try:
        eilv = F76GroupParser.get_group_segment(unit, b"EILV")
        start = 2
        while start < eilv.__len__():
            levels.append(str(F76AInst.get_uint(eilv, start)))
            start += 4
        return " / ".join(levels)
    except:
        if levels.__len__() == 0:
            return "1"
        return " / ".join(levels)


def at_points(unit):
    points = []
    try:
        attr = F76GroupParser.get_group_segment(unit, b"APPR")
        size = len(attr)
        start = 2
        while start < size:
            points.append(F76AInst.get_id(attr, start))
            start += 4
    except:
        return points
    return points


def def_mods(unit):
    ids = []
    try:
        obtss = F76GroupParser.get_group_segment(unit, b'OBTS', -1)
    except:
        return ids
    for obts in obtss:
        g_ids = []
        group_count = struct.unpack('<H', obts[2:4])[0]
        property_count = struct.unpack("<H", obts[6:8])[0]
        properties_size = property_count * 24
        if group_count > 0:
            size = len(obts) - properties_size
            start = size - group_count * 7
            while start < size:
                g_ids.append(F76AInst.get_id(obts, start))
                start += 7
        if g_ids.__len__() > 0:
            ids.append(g_ids)
    return ids


def damage(unit):
    # [d_id, value, curv]
    result = []
    try:
        if F76AInst.get_id(unit) == '0055c151':
            print("Setup curv manually for '0055c151'")
            bc = '00568628'
        else:
            bc = F76AInst.get_id(F76GroupParser.get_group_segment(unit, b'CVT0'), 2)
        result.append(['', 0, bc])
    except:
        ...
    try:
        dama = F76GroupParser.get_group_segment(unit, b'DAMA')
        start = 2
        while start < dama.__len__():
            damage = ["", 0, ""]
            result.append(damage)
            damage[0] = F76AInst.get_id(dama, start)
            start += 4
            damage[1] = F76AInst.get_uint(dama, start)
            start += 4
            damage[2] = F76AInst.get_id(dama, start)
            start += 4
    except:
        ...
    return result


def rgw3(unit):
    try:
        rgw = F76GroupParser.get_group_segment(unit, b'RGW3')
        return F76AInst.get_id(rgw, 2)
    except:
        return ''


def get_full(unit):
    if F76AInst.get_id(unit) == '0075ec27':
        return b'\x02\x95\x00'
    return F76AInst.get_full(unit)


def crit(unit):
    result = {"mult": 2, "charge": 1, "spell": ""}
    try:
        crdt = F76GroupParser.get_group_segment(unit, b'CRDT')
        result["mult"] = F76AInst.get_float(crdt, 2)
        result["charge"] = F76AInst.get_float(crdt, 6)
        result["spell"] = F76AInst.get_id(crdt, 10)
    except:
        ...
    return result


def weap_effect(unit):
    try:
        eitm = F76GroupParser.get_group_segment(unit, b'EITM')
        return F76AInst.get_id(eitm, 2)
    except:
        return ''


class UCat(Enum):
    ETYP = {
        'data': {
            'EQTYPE': lambda unit: F76AInst.get_id(F76GroupParser.get_group_segment(unit, b'ETYP'), 2)
        },
        'segment': b'ETYP'
    }

    RGW3 = {
        'data': {
            'ID': F76AInst.get_id,
            'NAME': F76AInst.get_name,
            'PROJ_TYPE': rgw3,
            # 'ANIM_FIRE': ('<f', 6),
            # 'RUMBLE_L': ('<f', 10),
            # 'RUMBLE_R': ('<f', 14),
            # 'RUMBLE_D': ('<f', 18),
            'ANIM_RELOAD': ('<f', 22),
            'SIGHTED_TRANS': ('<f', 30),
            'UNSIGHTED_TRANS': ('<f', 34),
            'PROJECTILES': ('<B', 54),
        },
        'segment': b'RGW3'
    }

    DNAM = {
        'data': {
            'AMMO': lambda unit: F76AInst.get_id(F76GroupParser.get_group_segment(unit, b'DNAM')[2:6], 0),
            'SPEED': ("<f", 6),
            'ATTACK_DELAY': ('<f', 38),
            'DAMAGE_OUT_OF_RANGE': ('<f', 46),
            'CAPACITY': ('<H', 66),
            'WEIGHT': ('<f', 75),
            'ATTACK_SPEED': ('<f', 122),
            'AP': ('<f', 128),

        },
        'segment': b'DNAM'
    }

    FULL = {
        'data': {
            "LOCALIZED_NAME": get_full
        },
        'segment': b'FULL'
    }

    KWDA = {
        'data': {
            "TAGS": tags
        },
        'segment': b'KWDA'
    }

    OBTS = {
        'data': {
            "DEF_MODS": def_mods
        },
        'segment': b'OBTS'
    }

    APPR = {
        'data': {
            "AT_POINTS": at_points
        },
        'segment': b'APPR'
    }

    EILV = {
        'data': {
            "LEVELS": level
        },
        'segment': b'EILV'
    }

    CVT0 = {
        'data': {
            "DAMAGE": damage
        },
        'segment': b'CVT0'
    }

    CRDT = {
        'data': {
            "CRIT": crit
        },
        'segment': b'CRDT'
    }

    EITM = {
        'data': {
            "WEAP_EFFECT": weap_effect
        },
        'segment': b'EITM'
    }
