import mmap
import struct

import Root
from Code.Helpers.F76GroupParser import F76GroupParser
from Code.Helpers.Global import Global


class F76AInst():

    @staticmethod
    def get_ushort(unit: bytes, index=0):
        return struct.unpack('<H', unit[index: index + 2])[0]

    @staticmethod
    def get_short(unit: bytes, index=0):
        return struct.unpack('<h', unit[index: index + 2])[0]

    @staticmethod
    def get_uchar(unit: bytes, index=0):
        return struct.unpack('<B', unit[index: index + 1])[0]

    @staticmethod
    def get_char(unit: bytes, index=0):
        return struct.unpack('<b', unit[index: index + 1])[0]

    @staticmethod
    def get_uint(unit: bytes, index=0):
        return struct.unpack('<I', unit[index: index + 4])[0]

    @staticmethod
    def get_int(unit: bytes, index=0):
        return struct.unpack('<i', unit[index: index + 4])[0]

    @staticmethod
    def get_float(unit: bytes, index=0):
        return struct.unpack('<f', unit[index: index + 4])[0]

    @staticmethod
    def look(unit: bytes, cat: (bytes, int), dictionary: {}, start_from=0, id_func=None):
        idd = id_func(unit)
        if dictionary.__contains__(idd):
            print(idd, F76AInst.analyze_and_find(unit, cat, dictionary[idd], start_from))

    @staticmethod
    def get_id(unit: bytes, start=12):
        return hex(struct.unpack('<L', unit[start:start + 4])[0])[2:].zfill(8)

    @staticmethod
    def get_version(unit: bytes, start=20):
        return F76AInst.get_uchar(unit, start)

    @staticmethod
    def get_id_and_resolve(unit, index, resolver):
        id = ''
        try:
            id = F76AInst.get_id(unit, index)
            return resolver[id], True
        except:
            return id, False

    @staticmethod
    def get_possible_ids(unit: bytes):
        result = []
        for i in range(unit.__len__() - 3):
            result.append([F76AInst.get_id(unit, i), i])
        return result

    @staticmethod
    def get_tags_count(unit: bytes):
        try:
            return struct.unpack('<H', F76GroupParser.get_group_segment(unit, b"KSIZ")[2:4])[0]
        except:
            return 0

    @staticmethod
    def get_name(unit: bytes, start=30):
        return unit[start:].partition(b'\x00')[0].decode('latin-1')

    @staticmethod
    def get_full(unit: bytes):
        try:
            return F76GroupParser.get_group_segment(unit, b'FULL')[2:]
        except:
            return b''

    @staticmethod
    def get_description(unit: bytes):
        try:
            return F76GroupParser.get_group_segment(unit, b'DESC')[2:]
        except:
            return b''

    @staticmethod
    def run_through_getting_numbers(unit: bytes, category, fmt: str, start_from=0, is_print=False,
                                    min_max: () = None) -> []:
        if category is None:
            val = unit
        else:
            index = unit.find(category[0])
            if index < 0:
                return
            if category[1] == 0:
                val = unit[index:]
            else:
                index += category[0].__len__()
                val = unit[index: index + category[1]]
        length = val.__len__()
        size = struct.calcsize(fmt)
        result = []
        for i in range(start_from, length - size + 1):
            number = val[i: i + size]
            value = struct.unpack(fmt, number)[0]
            if min_max is None or min_max[0] < value < min_max[1]:
                result.append(value)
        if is_print:
            print(result)
        return result

    @staticmethod
    def analyze_and_find(unit: bytes, category: (bytes, int), what: (), start_from=0, min_max: () = None,
                         is_print=False):
        value = what[0]
        epsilon = what[1]
        result = {}
        fmts = ['f', 'b', 'B', 'h', 'H', 'i', 'I', 'q', 'Q']
        for fmt in fmts:
            result[fmt] = F76AInst.__get_indexes(
                F76AInst.run_through_getting_numbers(unit, category, '<' + fmt, start_from, is_print, min_max), value,
                epsilon)
        return result

    @staticmethod
    def __get_indexes(array: [], value: float, epsilon: float = None):
        if epsilon is None:
            epsilon = 0.1
        result = []
        for i in range(len(array)):
            if abs(array[i] - value) <= epsilon:
                result.append([i, array[i]])
        return result

    @staticmethod
    def find_id(unit: bytes, idd, starts_from=0):
        for i in range(starts_from, len(unit) - 3):
            if F76AInst.get_id(unit, i) == idd:
                return i

    @staticmethod
    def find_float(unit: bytes, value, starts_from=0, epsilon = 0.000001):
        for i in range(starts_from, len(unit) - 3):
            found = F76AInst.get_float(unit, i)
            if abs(found - value) <= epsilon:
                return i

    @staticmethod
    def find_uint(unit: bytes, value, starts_from=0):
        for i in range(starts_from, len(unit) - 3):
            found = F76AInst.get_uint(unit, i)
            if found == value:
                return i

    @staticmethod
    def find_int(unit: bytes, value, starts_from=0):
        for i in range(starts_from, len(unit) - 3):
            found = F76AInst.get_int(unit, i)
            if found == value:
                return i

    @staticmethod
    def find_char(unit: bytes, value, starts_from=0):
        for i in range(starts_from, len(unit) - 1):
            found = F76AInst.get_char(unit, i)
            if found == value:
                return i

    @staticmethod
    def find_uchar(unit: bytes, value, starts_from=0):
        for i in range(starts_from, len(unit) - 1):
            found = F76AInst.get_uchar(unit, i)
            if found == value:
                return i

    @staticmethod
    def get_cat_unit(unit: bytes, category: (bytes, int), ids: [] = None, id_func=None, is_print=False):
        cat = category[0]
        size = category[1]
        index = unit.find(cat)
        if index == -1:
            return None
        if size == 0:
            size = len(unit) - index
        index += cat.__len__()
        id = id_func(unit) if id_func is not None else None
        ids = ids if id_func is not None else None
        if ids is None or ids.__contains__(id):
            result = unit[index: index + size]
            if is_print:
                print(id, result)
            return result
        return None

    @staticmethod
    def non_standard_float(unit: bytes, cat):
        block = F76AInst.get_cat_unit(unit, cat)
        xx = [b'\x00\x00\x00', b'\x00\x00', b'\x00', b'']
        for x in xx:
            for number in range(1, 4):
                for i in range(len(block)):
                    val = block[i: i + number]
                    val1 = val + x
                    val2 = x + val
                    try:
                        r1 = struct.unpack("<f", val1)[0]
                        r2 = struct.unpack("<f", val2)[0]
                        if r1 != 0 and r1 is not None and 0.0000001 < abs(r1) < 100000:
                            print("val1", r1)
                        if r2 != 0 and r2 is not None and 0.0000001 < abs(r2) < 100000:
                            print("val2", r2)
                    except:
                        continue

    @staticmethod
    def resolve_localized_names(items: [], items_iter, bytes_getter, name_setter):
        path = Global.config.build_resources_path("LOCALIZATION", "SeventySixEngPath")
        with open(path, mode="rb") as f:
            file_map = mmap.mmap(f.fileno(), access=mmap.ACCESS_READ, length=0, offset=0)
            start = file_map.find(b"\x00Door\x00") + 1
            for item in items_iter(items):
                item_bytes = bytes_getter(item)
                if item_bytes is not None:
                    try:
                        item_name = F76AInst.__get_name(file_map, start, item_bytes)
                    except:
                        item_name = item_bytes
                    name_setter(item, item_name)

    @staticmethod
    def __get_name(file_map, start, full_id, encoding='latin-1'):
        file_map.seek(0)
        full_id_index = file_map.find(full_id)
        position_bytes = file_map[full_id_index + 4: full_id_index + 8]
        position = struct.unpack("<I", position_bytes)[0]
        name_start_index = start + position
        return file_map[name_start_index:].partition(b'\x00')[0].decode(encoding)

    @staticmethod
    def find_named_groups(unit, name, default_value=None):
        try:
            return F76GroupParser.find_groups(unit, name)[name]
        except:
            return default_value
