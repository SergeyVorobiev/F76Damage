import csv


class CSV:

    @staticmethod
    def build_table(path: str, table, delimiter):
        with open(path, 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)
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
    def read_rows(path: str, delimiter: str, skip_header=True):
        result = []
        with open(path, newline='') as f:
            reader = csv.reader(f, delimiter=delimiter, quotechar='|')
            for row in reader:
                if skip_header:
                    skip_header = False
                    continue
                result.append(row)
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
    def build_weapon_table(data, sort=None, ignore_names=None):
        if ignore_names is None:
            ignore_names = []
        if sort is not None and sort != "None":
            data.sort(key=lambda r: r[sort])
        header = list(data[0].keys())
        header.append("W_TYPE")
        table = [header]
        range_table = [header]
        melee_table = [header]
        thrown_table = [header]
        unarmed_table = [header]

        for row in data:
            new_row = CSV.__prepare_row(row, ignore_names)
            if new_row is not None:
                last = new_row.__len__() - 1
                table.append(new_row)
                if new_row[last] == "Melee":
                    melee_table.append(new_row)
                elif new_row[last] == "Unarmed":
                    unarmed_table.append(new_row)
                elif new_row[last] == "Thrown":
                    thrown_table.append(new_row)
                else:
                    range_table.append(new_row)
        return table, range_table, melee_table, thrown_table, unarmed_table

    @staticmethod
    def save_table(path: str, table, delimiter=','):
        with open(path, 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            write.writerows(table)

    melee = ["MeleeGeneral", "Melee1H", "Melee2H"]
    thrown = ["Thrown", "Grenade", "Mine", "PulseGrenade", "CryoGrenade"]
    unarmed = ["Unarmed"]
    range = ["Range", "Automatic", "Ballistic", "Pistol", "Laser", "NoAttack", "NonOffensive", "HeavyGun"]

    @staticmethod
    def __assign_w_type(row, names, tag):
        for name in names:
            tags = row['TAGS']
            if tags.__contains__(name):
                row['W_TYPE'] = tag
                return True
        return False

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
        for item in row.items():
            key = item[0]
            value = item[1]
            try:
                row[key] = round(value, 5)
            except:
                continue
        assigned = CSV.__assign_w_type(row, CSV.unarmed, "Unarmed")
        if not assigned:
            assigned = CSV.__assign_w_type(row, CSV.melee, "Melee")
        if not assigned:
            assigned = CSV.__assign_w_type(row, CSV.thrown, "Thrown")
        if not assigned:
            row['W_TYPE'] = "Range"
        #mods = row['DEF_MODS']
        #if mods and len(mods) > 0:
        #    row['DEF_MODS'] = row['DEF_MODS']
        #else:
        #    row['DEF_MODS'] = ""
        tags = row['TAGS']
        if tags and len(tags) > 0:
            row['TAGS'] = " / ".join(row['TAGS'])
        else:
            row['TAGS'] = ""
        return list(row.values())
