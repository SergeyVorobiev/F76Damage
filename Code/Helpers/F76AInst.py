import struct


class F76AInst():

    @staticmethod
    def look(unit: bytes, cat: (bytes, int), dictionary: {}, start_from=0, id_func=None):
        idd = id_func(unit)
        if dictionary.__contains__(idd):
            print(idd, F76AInst.analyze_and_find(unit, cat, dictionary[idd], start_from))

    @staticmethod
    def get_id(unit: bytes, start=12):
        return hex(struct.unpack('<L', unit[start:start + 4])[0])[2:].zfill(8)

    @staticmethod
    def get_name(unit: bytes):
        return unit[30:].partition(b'\x00')[0].decode('latin-1')

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
        for i in range(starts_from, len(unit) - 4):
            if F76AInst.get_id(unit, i) == idd:
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
