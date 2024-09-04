import mmap
import os

from Code.Decoders.AbstractDecoder import AbstractDecoder
from Code.Units.UnitData import UnitData


class UnitSeparator:

    # Return pos or -1 if a label was not found.
    # How far - how far it must search from current position to understand that it is over, -1 means to the end of file
    @staticmethod
    def __find_unit(file_map: mmap.mmap, pos: int, unit: UnitData, start: bool = True, how_far=-1) -> (int, int):
        unit.set_start(start)
        end_pos = 0
        if how_far > 0:
            end_pos = pos + how_far
            if end_pos > file_map.size():
                end_pos = file_map.size()
        file_map.seek(pos, os.SEEK_SET)
        pos = UnitSeparator.__find_next_pos(file_map, unit.c_key.label, pos, end_pos, how_far)
        while pos >= 0:
            file_map.seek(pos, os.SEEK_SET)
            try:
                part = file_map.read(unit.c_key.format_size)
            except:
                return -1, -1
            try:
                result, size = unit.match(part)
                if result:
                    return pos, size
            except:
                pass
            pos += unit.c_key.l_length
            file_map.seek(pos, os.SEEK_SET)
            pos = UnitSeparator.__find_next_pos(file_map, unit.c_key.label, pos, end_pos, how_far)
        return pos, -1

    @staticmethod
    def __find_next_pos(file_map, label, pos, end_pos, how_far):
        if how_far > 0:
            pos_inside = file_map[pos: end_pos].find(label)
            if pos_inside == -1:
                return -1
            else:
                pos += pos_inside
        else:
            pos = file_map.find(label)
        return pos

    @staticmethod
    def separate_and_decode_bytes(unit: bytes, decoders: [AbstractDecoder]):
        mm = mmap.mmap(-1, unit.__len__())
        mm.write(unit)
        UnitSeparator.separate_and_decode_mmap(mm, decoders)

    @staticmethod
    def separate_and_decode_mmap(unit: mmap, decoders: [AbstractDecoder]):
        with unit as file_map:
            for decoder in decoders:
                unit: UnitData = decoder.unit
                stop = False
                next_e_key_pos = -1
                decoder.before_start()
                pos, size = UnitSeparator.__find_unit(file_map, 0, unit)
                while pos >= 0 and not stop:
                    if size > 0:
                        next_pos = pos + size
                        next_m_key_pos, next_size = UnitSeparator.__find_unit(file_map, next_pos, unit, how_far=1000)
                    else:
                        next_pos = pos + unit.s_key.l_length
                        next_m_key_pos, next_size = UnitSeparator.__find_unit(file_map, next_pos, unit)

                    if next_e_key_pos <= next_m_key_pos and size <= 0:
                        next_e_key_pos, _ = UnitSeparator.__find_unit(file_map, pos, unit, start=False)
                    if size > 0:
                        if next_m_key_pos == -1:
                            stop = True
                        unit_length = size
                    elif next_m_key_pos == -1 and next_e_key_pos >= 0:
                        unit_length = next_e_key_pos - pos
                    elif next_m_key_pos >= 0 and next_e_key_pos == -1:
                        unit_length = next_m_key_pos - pos
                    elif next_m_key_pos == -1 and next_e_key_pos == -1:
                        unit_length = file_map.size() - pos
                        stop = True
                    else:
                        next_pos = next_m_key_pos if next_m_key_pos < next_e_key_pos else next_e_key_pos
                        unit_length = next_pos - pos
                    file_map.seek(pos, os.SEEK_SET)
                    if 0 < unit.max_unit_length < unit_length:
                        unit_length = unit.max_unit_length
                    decoder.decode_unit(file_map.read(unit_length))
                    pos = next_m_key_pos
                    size = next_size
                decoder.on_finish()

    @staticmethod
    def separate_and_decode_file(path, decoders: [AbstractDecoder]):
        if type(path).__name__ != 'str':
            path = path.value
        with open(path, mode="rb") as f:
            UnitSeparator.separate_and_decode_mmap(mmap.mmap(f.fileno(), access=mmap.ACCESS_READ, length=0, offset=0),
                                                   decoders)
