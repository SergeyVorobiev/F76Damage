from Code.Grabbers.CurvGrabber import CurvGrabber


class Mod:
    def __init__(self, idd, name, full_name_bytes, attach_id, target_ids, data):
        self.name = name
        self.idd = idd
        self.attach_id = attach_id
        self.target_ids = target_ids
        self.full_name_bytes = full_name_bytes
        self.localized_name = "None"
        self.contains = []
        self.properties = []
        if data is None:
            self.includes = []
        else:
            self.includes = data[0]['Includes']
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
            table.append([self.idd, self.name, self.localized_name, self.idd, self.attach_id, self.target_ids])
        for prop in self.properties:
            values = next(prop.values().__iter__())
            prop_n = values['Prop']
            if ignore_props is not None and ignore_props.__contains__(prop_n):
                continue
            tabId = ''
            if values['TabID'] != '00000000':
                tabId = values['TabID']
            row = ["", "", "", next(prop.keys().__iter__()), "", "", values['FunType'], prop_n, values['Val1'],
                   values['Val2'], values['Enchantment'], tabId]
            if ignore_if_empty:
                ignore_if_empty = False
                table.append([self.idd, self.name, self.localized_name, self.idd, self.attach_id, self.target_ids])
            table.append(row)
        return table

    def replace_curves_ids(self, curv, column_name):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            c_id = values[column_name]
            if c_id is None or c_id == '' or c_id == '00000000':
                continue
            if type(c_id) is str:
                try:
                    values[column_name] = curv[c_id]
                except:
                    continue
            else:  # Array
                result = []
                for single_id in c_id:
                    try:
                        result.append(curv[single_id])
                    except:
                        result.append(single_id)
                values[column_name] = result

    def resolve_dmg_types(self, dmgt):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "DamageTypeValues":
                try:
                    dtype = dmgt[values['Val1']]
                    values['Enchantment'] = dtype
                    values['Val1'] = values['Val1'] + " / " + dtype['name']
                except:
                    continue

    def resolve_avif(self, avif):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "ActorValues":
                try:
                    dtype = avif[values['Val1']]
                    values['Enchantment'] = dtype
                    values['Val1'] = values['Val1'] + " / " + dtype['name']
                except:
                    continue

    def resolve_kywd(self, kywd):
        try:
            self.attach_id = self.attach_id + "_" + kywd[self.attach_id]
        except:
            ...  # OK
        new_target_ids = []
        for target_id in self.target_ids:
            try:
                new_target_id = target_id + "_" + kywd[target_id]
            except:
                new_target_id = target_id
            new_target_ids.append(new_target_id)
        self.target_ids = " / ".join(new_target_ids)
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "Keywords":
                try:
                    dtype = kywd[values['Val1']]
                    values['Val1'] = values['Val1'] + " / " + dtype
                except:
                    continue

    def resolve_ammo(self, ammo):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "Ammo":
                try:
                    dtype = ammo[values['Val1']]
                    values['Enchantment'] = dtype
                    values['Val1'] = values['Val1'] + " / " + dtype['name']
                except:
                    continue

    def resolve_proj(self, proj):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "OverrideProjectile":
                try:
                    dtype = proj[values['Val1']]
                    values['Enchantment'] = dtype
                    values['Val1'] = values['Val1'] + " / " + dtype['name']
                except:
                    continue

    def resolve_spell(self, spell):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values['Prop'] == "CritEffect":
                try:
                    dtype = spell[values['Val1']]
                    values['Enchantment'] = dtype
                    values['Val1'] = values['Val1'] + " / " + dtype['name']
                except:
                    continue

    def resolve_effects(self, effects):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if values.get("Enchantment") is None:
                values["Enchantment"] = ''
            if values['Prop'] == "Enchantments":
                try:
                    dtype = effects[values['Val1']]
                    values['Enchantment'] = str(dtype)
                    curv_list = []
                    for item in dtype['efit']:
                        if item['curv_id'] == '':
                            curv_list.append("None")
                        else:
                            curv_list.append(item['curv_id'])
                    values['TabID'] = curv_list
                except:
                    continue

    def contains_props(self, props):
        for prop in self.properties:
            values = next(prop.values().__iter__())
            if props.__contains__(values['Prop']):
                return True
        return False
