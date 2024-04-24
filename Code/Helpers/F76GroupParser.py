import csv
import struct


def build_exclusions():
    exclu = [b'UUU', b'KKR']
    alphabet = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for i in range(len(alphabet)):
        cat = bytearray(b'DATA')
        cat.append(alphabet[i])
        exclu.append(bytes(cat))
    return exclu


class F76GroupParser:
    exclusions = build_exclusions()
    existed = [b'DATA', b'WEAP', b'RGW35', b'DNAM']

    @staticmethod
    def get_group_segment(unit: bytes, group_name, groups=None):
        if not groups:
            groups = F76GroupParser.find_groups(unit)
        range = groups[group_name]
        return unit[range[0]: range[0] + range[1]]

    @staticmethod
    def find_groups(unit: bytes):
        max_word_l = 6
        result = {}
        last_word = ''
        last_index = 0
        size = -1
        i = 0
        end = unit.__len__()
        while i < end:
            word = unit[i: i + max_word_l]
            if size > -1:
                size += 1
            is_word = True
            w_l = word.__len__()
            if w_l < 3:
                break
            word_l = w_l
            for j, value in enumerate(struct.unpack(f'<{w_l}B', word)):
                if j > 2 and F76GroupParser.existed.__contains__(word[: j]):
                    word_l = j
                    break
                if value < 65 or value > 90:
                    if j == 0:  # We are not starting from letter
                        is_word = False
                        break
                    elif value > 57 or value < 48:
                        if j < 3:
                            is_word = False
                        else:
                            word_l = j
                        break
            if F76GroupParser.exclusions.__contains__(word[:word_l]):
                is_word = False
            if is_word:
                if size == -1:
                    size = 0
                else:
                    result[last_word] = [last_index, size]
                    size = 0
                last_word = struct.unpack(f'<{word_l}s', word[:word_l])[0]
                last_index = i + word_l
                result.__setitem__(last_word, [0, 0])
                i += word_l
            i += 1
        result[last_word] = [last_index, unit.__len__() - last_index]
        return result

    @staticmethod
    def parse_groups(unit: bytes, min_max=None, include_zeroes=True):
        group_names = F76GroupParser.find_groups(unit)
        result = {}
        fmts = ["<f", "<h"]
        for item in group_names.items():
            key = item[0]
            value = item[1]
            r = {}
            for fmt in fmts:
                numbers = F76GroupParser.__run_through_unit(unit, value, fmt, min_max=min_max,
                                                            include_zeroes=include_zeroes)
                if numbers.__len__() > 0:
                    r[fmt] = numbers
            if r.__len__() > 0:
                result[key] = (value, r)
        return result

    @staticmethod
    def find_from_group_by_index(unit, group_name, fmt: str, index: int):
        segment = F76GroupParser.get_group_segment(unit, group_name)
        size = struct.calcsize(fmt)
        segment = segment[index: index + size]
        return struct.unpack(fmt, segment)[0]

    @staticmethod
    def get_from_group_by_index(groups: {}, group: bytes, fmt: str, index: int):
        result = []
        try:
            for tuple_ in groups[group][1][fmt]:
                if index == tuple_[0]:
                    result.append(tuple_[1])
        except:
            return None
        return result

    @staticmethod
    def search_in_groups(groups, number: float, epsilon, target_groups: [] = None):
        result = {}
        for item in groups.items():
            group_name = item[0]
            if target_groups is not None and not target_groups.__contains__(group_name):
                continue
            value = item[1]
            fmts = value[1]
            result_fmts = {}
            for fmt in fmts.items():
                name = fmt[0]
                values = fmt[1]
                result_tuple = []
                for value in values:
                    index = value[0]
                    val = value[1]
                    if abs(val - number) <= epsilon:
                        result_tuple.append((index, val))
                if result_tuple.__len__() > 0:
                    result_fmts[name] = result_tuple
            if result_fmts.__len__() > 0:
                result[group_name] = result_fmts
        return result

    @staticmethod
    def __run_through_unit(unit: bytes, group_range: [], fmt: str, min_max: () = None, include_zeroes=True):
        size = struct.calcsize(fmt)
        result = []
        for i in range(group_range[1] - size + 1):
            index = group_range[0] + i
            number = unit[index: index + size]
            if number.__len__() < size:
                break
            value = struct.unpack(fmt, number)[0]
            if min_max is None or min_max[0] <= value <= min_max[1] or (include_zeroes and value == 0):
                result.append((i, value))
        return result

    @staticmethod
    def parse_file(path_file, dest_csv_file):
        with open(path_file, mode="rb") as f:
            unit = f.read()
            groups = F76GroupParser.find_groups(unit)
            with open(dest_csv_file, 'w', newline='') as csvfile:
                write = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                write.writerow(["Name", "StartIndex", "Size"])
                for item in groups.items():
                    group_name = item[0]
                    start_index = item[1][0]
                    size = item[1][1]
                    write.writerow([group_name, start_index, size])
