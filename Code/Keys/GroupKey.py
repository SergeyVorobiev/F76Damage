from enum import Enum


class GroupKey(Enum):
    F76_WEAPON = (b'WEAP', b'WEAP??\x00*\x00EDID', 28, None)

    F76_GRUP = (b'\x00GRUP', b'\x00GRUP', '<x4s', None)

    F76_PROJ = (b'PROJ', b'PROJ??\x00*\x00EDID', 28, None)

    F76_OMOD = (b'OMOD', b'OMOD??\x00*\x00EDID', 28, None)

    F76_CURV = (b'CURV', b'CURV??\x00*\x00EDID', 28, None)

    F76_DMGT = (b'DMGT', b'DMGT??\x00*\x00EDID', 28, None)
