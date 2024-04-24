import json
import os


class Mod:
    def __init__(self, idd, name, data):
        self.name = name
        self.idd = idd
        self.contains = []
        self.includes = data[0]['Includes']
        self.properties = []
        for i in range(1, len(data)):
            self.contains.append({idd: data[i]})

    def gather_properties(self, all_data):
        self.properties = self.__get_include(all_data)

    def __get_include(self, all_data):
        props = []
        for include in self.includes:
            try:
                mod = all_data[include]
                props += mod.__get_include(all_data)
            except:
                continue
        return props + self.contains

    def __str__(self):
        label = f"{self.name} {self.idd}\n"
        body = ""
        for content in self.properties:
            body += str(content) + "\n"
        return label + body

    def as_csv_table(self, table, ignore_props=None, ignore_if_empty=False):
        if not ignore_if_empty:
            table.append([self.idd, self.name, self.idd])
        for prop in self.properties:
            values = next(prop.values().__iter__())
            prop_n = values['Prop']
            if ignore_props is not None and ignore_props.__contains__(prop_n):
                continue
            tabId = ''
            if values['TabID'] != '00000000':
                tabId = values['TabID']
            row = ["", "", next(prop.keys().__iter__()), values['FunType'], prop_n, values['Val1'], values['Val2'],
                   tabId]
            if ignore_if_empty:
                ignore_if_empty = False
                table.append([self.idd, self.name, self.idd])
            table.append(row)
        return table

    @staticmethod
    def __get_data_from_json(cur_path):
        try:
            with open(cur_path) as f:
                return json.load(f)
        except:
            return "{Can't extract data}"

    def replace_curves_ids(self, curves, path_to_json_folder):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            try:
                if values['TabID'] != '00000000':
                    path_ = curves[values['TabID']]
                    full_path = os.path.join(path_to_json_folder, path_.lower())
                    json_data = Mod.__get_data_from_json(full_path)
                    values['TabID'] = path_ + "\n" + str(json_data)
            except:
                continue

    def resolve_dgm_types(self, dmgt):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "DamageTypeValues":
                try:
                    dtype = dmgt[values['Val1']]
                    values['Val1'] = dtype
                except:
                    continue

    def contains_props(self, props):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if props.__contains__(values['Prop']):
                return True
        return False
