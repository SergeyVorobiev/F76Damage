import csv


class CSV:

    @staticmethod
    def build_table(path: str, table, delimiter):
        with open(path, 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            write.writerows(table)

    @staticmethod
    def read_creature_health_into_map(path: str, delimiter):
        result = {}
        with open(path, newline='') as file:
            reader = csv.reader(file, delimiter=delimiter, quotechar='|')
            skip_header = True
            for row in reader:
                if skip_header:
                    skip_header = False
                    continue
                name = row[0]
                array = result.get(name, [])
                array.append(row[2])
                result[name] = array
            return result

    @staticmethod
    def merge_health_into_creature_res_file(creature_res_path: str, path_to_save: str, health_map, delimiter):
        with open(creature_res_path, newline='') as res_file:
            reader = csv.reader(res_file, delimiter=delimiter, quotechar='|')
            with open(path_to_save, 'w', newline='') as csvfile:
                write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
                header = True
                for row in reader:
                    if header:
                        header = False
                        row.append("Health")
                    else:
                        name = row[0]
                        if name == 'critter':  # just skip medium and small
                            name = 'critterlarge'
                        row.append(health_map[name][int(row[1]) - 1])
                    write.writerow(row)

    @staticmethod
    def build_melee_range_table(data, is_melee, sort=None, ignore_names=None):
        if ignore_names is None:
            ignore_names = []
        if sort is not None and sort != "None":
            data.sort(key=lambda r: r[sort])
        header = list(data[0].keys())
        if not header.__contains__("ATTACK_RATE"):
            header.append("ATTACK_RATE")
        if not header.__contains__("MANUAL_RATE"):
            header.append("MANUAL_RATE")
        if not header.__contains__("DEF_FIRE_RATE"):
            header.append("DEF_FIRE_RATE")
        table = [header]
        for row in data:
            if is_melee:
                if row['ANIM_FIRE'] is not None:
                    continue
            else:
                if row['ANIM_FIRE'] is None:
                    continue
            new_row = CSV.__prepare_row(row, ignore_names)
            if new_row is not None:
                table.append(new_row)
        return table

    @staticmethod
    def build_melee(path: str, table, delimiter=','):
        CSV.build_melee_range(path, table, delimiter)

    @staticmethod
    def build_range(path: str, table, delimiter=','):
        CSV.build_melee_range(path, table, delimiter)

    @staticmethod
    def build_melee_range(path: str, table, delimiter=','):
        with open(path, 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            write.writerows(table)

    @staticmethod
    def __prepare_row(row, ignore_names):
        name = row['NAME']
        skip = False
        for i_name in ignore_names:
            if name.startswith(i_name):
                skip = True
                break
        if skip:
            return None
        rate = 0
        m_rate = 0
        f_rate = 0
        new_row = list(row.values())
        for item in row.items():
            key = item[0]
            value = item[1]
            try:
                row[key] = round(value, 3)
                if key == 'ATTACK_SPEED':
                    rate = round(10 / value, 3)
                elif key == 'ATTACK_DELAY' and value > 0:
                    m_rate = round(10 / value, 3)
                elif key == "SPEED":
                    f_rate = round(91 * value, 3)
            except:
                continue
        new_row.append(rate)
        new_row.append(m_rate)
        new_row.append(f_rate)
        return new_row
