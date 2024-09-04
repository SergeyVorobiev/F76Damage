import csv
import struct


def build_exclusions():
    exclu = [b'UUU', b'KKR', b'MIV', b'WEAPO', b'A333', b'PCGZ', b'ADNA', b'SNDD', b'AEPF']
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    g_data = "DATA"
    for i in range(len(alphabet)):
        exclu.append(bytes(alphabet[i] + g_data, 'utf-8'))
    return exclu


class F76GroupParser:
    exclusions = build_exclusions()
    existed = [b'EDID', b'AVIF', b'DATA', b'WEAP', b'RGW3', b'DNAM', b'KWDA', b'OBTS', b'ETYP', b'FULL', b'KYWD',
               b'AMMO', b'APPR', b'EILV', b'CVT0', b'DAMA', b'KSIZ', b'SPIT', b'DESC', b'ENIT', b'PERK', b'PRKE',
               b'FLTV', b'EPFT', b'EPFD', b'NTWK', b'MAGA', b'DURG', b'MAGG', b'CODV', b'CRDT', b'DSTD', b'DSTF',
               b'EITM', b'ALCH', b'MSTT', b'OBND', b'VMAD']

    # group_index -1 = all groups
    @staticmethod
    def get_group_segment(unit: bytes, group_name, group_index=0, groups=None, only_existed=False):
        if not groups:
            groups = F76GroupParser.find_groups(unit, group_name, only_existed=only_existed)
        if group_index < 0:
            result = []
            for group_with_name in groups[group_name]:
                result.append(unit[group_with_name[0]: group_with_name[0] + group_with_name[1]])
            return result
        else:
            range = groups[group_name][group_index]
            return unit[range[0]: range[0] + range[1]]

    @staticmethod
    def get_group_segment_or_def(unit: bytes, group_name, def_value=None, group_index=0, only_existed=False):
        try:
            return F76GroupParser.get_group_segment(unit, group_name, group_index=group_index,
                                                    only_existed=only_existed)
        except:
            return def_value

    # They should not intersect each other
    @staticmethod
    def get_segments_between(unit: bytes, start_group, end_group, include_start_group_name=True,
                             include_end_group_name=False, starts_from=0):
        result = []
        try:
            start_groups = F76GroupParser.find_groups(unit, start_group, starts_from=starts_from)[start_group]
            for i in range(start_groups.__len__()):
                start_index = start_groups[i][0]
                end_index = start_index + unit[start_index:].find(end_group)
                if end_index < 0:
                    continue
                if include_start_group_name:
                    start_index = start_index - start_group.__len__()
                    if start_index < 0:
                        start_index = 0
                if include_end_group_name:
                    end_index = end_index + end_group.__len__()
                    if end_index < 0:
                        end_index = 0
                result.append(unit[start_index: end_index])
        except:
            return result
        return result

    @staticmethod
    def __find_keyword(word, w_l, more_than):
        existed_group = False
        is_word = True
        word_l = w_l
        for j, value in enumerate(struct.unpack(f'<{w_l}B', word)):
            if F76GroupParser.existed.__contains__(word):
                existed_group = True
                word_l = word.__len__()
                break
            if j > more_than and F76GroupParser.existed.__contains__(word[: j]):
                word_l = j
                break
            if value < 65 or value > 90:
                if j == 0:  # We are not starting from letter
                    is_word = False
                    break
                elif value > 57 or value < 48:
                    if j < 4:
                        is_word = False
                    else:
                        word_l = j
                    break
        return word_l, is_word, existed_group

    @staticmethod
    def find_groups(unit: bytes, only_name=None, min_group_length=4, max_group_length=4, starts_from=0,
                    only_existed=False):
        max_word_l = max_group_length
        result = {}
        last_word = ''
        last_index = 0
        size = -1
        more_than = min_group_length - 1
        i = starts_from
        end = unit.__len__()
        search_name = True
        while i < end:
            word = unit[i: i + max_word_l]
            word2 = unit[i: i + max_word_l + 1] # Avoid WEAPO
            if only_name is not None and search_name:
                if not word.startswith(only_name):
                    i += 1
                    continue
                else:
                    search_name = False  # Need to find closing group next time
            if size > -1:
                size += 1

            w_l = word.__len__()
            if w_l < min_group_length:
                break
            word_l, is_word, existed_group = F76GroupParser.__find_keyword(word, w_l, more_than)
            if not existed_group and only_existed:
                i += 1
                continue
            if not existed_group and is_word:
                if F76GroupParser.exclusions.__contains__(word[:word_l]):
                    is_word = False

            if is_word and F76GroupParser.exclusions.__contains__(word2):
                is_word = False
            if is_word:
                word = struct.unpack(f'<{word_l}s', word[:word_l])[0]
                if size == -1:
                    size = 0
                else:  # complete current group
                    if only_name is None or (
                            only_name is not None and last_word.startswith(only_name)):  # closing group
                        existed = result.get(last_word)
                        if existed is None:
                            result[last_word] = [[last_index, size]]
                        else:
                            existed[-1] = [last_index, size]
                    size = 0
                    search_name = only_name and not word.startswith(only_name)  # Next group again must be 'only_name'
                if only_name is None or (only_name is not None and word.startswith(only_name)):

                    # add next group
                    existed = result.get(word)
                    if existed is not None:
                        existed.append([0, 0])
                    else:
                        result.__setitem__(word, [[0, 0]])

                # rewrite last group
                last_word = word
                last_index = i + word_l
                i += word_l
            i += 1
        existed = result.get(last_word)
        if existed is not None:
            existed[-1] = [last_index, unit.__len__() - last_index]
        return result

    @staticmethod
    def parse_groups(unit: bytes, min_max=None, include_zeroes=True):
        group_names = F76GroupParser.find_groups(unit)
        result = {}
        fmts = ["<f", "<h"]
        for item in group_names.items():
            key = item[0]
            # a group is considered to be unique
            value = item[1][0]
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
                    # A group is considered to be unique
                    start_index = item[1][0][0]
                    size = item[1][0][1]
                    write.writerow([group_name, start_index, size])
