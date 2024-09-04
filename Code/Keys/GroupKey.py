from enum import Enum


class GroupKey(Enum):
    F76_WEAPON = (b'WEAP', b'WEAP??\x00*\x00EDID', 28, None)

    F76_GRUP = (b'\x00GRUP', b'\x00GRUP', '<x4s', None)

    F76_PROJ = (b'PROJ', b'PROJ??\x00*\x00EDID', 28, None)

    F76_OMOD = (b'OMOD', b'OMOD??\x00*\x00EDID', 28, None)

    F76_CURV = (b'CURV', b'CURV*\x00EDID', 28, None)

    F76_DMGT = (b'DMGT', b'DMGT??\x00*\x00EDID', 28, None)

    F76_AVIF = (b'AVIF', b'AVIF*\x00EDID', 28, None)

    F76_AMMO = (b'AMMO', b'AMMO??\x00*\x00EDID', 28, None)

    F76_GLOB = (b'GLOB', b'GLOB??\x00*\x00EDID', 28, None)

    F76_KYWD = (b'KYWD', b'KYWD??\x00*\x00EDID', 28, None)

    F76_EQUP = (b'EQUP', b'EQUP??\x00*\x00EDID', 28, None)

    F76_ENCH = (b'ENCH', b'ENCH??\x00*\x00EDID', 28, None)

    F76_HAZD = (b'HAZD', b'HAZD??\x00*\x00EDID', 28, None)

    F76_ALCH = (b'ALCH', b'ALCH??\x00*\x00EDID', 28, None)

    F76_MSTT = (b'MSTT', b'MSTT??\x00*\x00EDID', 28, None)

    F76_MGEF = (b'MGEF', b'MGEF??\x00*\x00EDID', 28, None)

    F76_EXPL = (b'EXPL', b'EXPL??\x00*\x00EDID', 28, None)

    F76_PERK = (b'PERK', b'PERK??\x00*\x00EDID', 28, None)

    F76_SPEL = (b'SPEL', b'SPEL??\x00*\x00EDID', 28, None)
