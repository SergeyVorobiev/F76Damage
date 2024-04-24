import json
from abc import abstractmethod


class LevelCurve:
    def __init__(self, path, res_names, max_level, formula_delimiter=';'):
        self._formula_delimiter = formula_delimiter
        self._path = path
        self._max_level = max_level
        self._res_names = res_names

    @abstractmethod
    def _prepare_names(self):
        pass

    @abstractmethod
    def _form_path(self, name, res_name):
        pass

    @abstractmethod
    def _get_exceptions(self):
        pass

    def build_dictionaries(self, exceptions=None):
        if exceptions is None:
            exceptions = self._get_exceptions()

        # Extrude unique creature names
        names_set = self._prepare_names()

        # go through all names to build level-dictionaries
        entities = {}
        for name in names_set:
            entity = {}
            if exceptions.__contains__(name):
                continue
            for res_name in self._res_names:
                cur_path = self._form_path(name, res_name)
                try:
                    entity[res_name] = self.__build(cur_path)
                except Exception as e:
                    print(name)
                    print(e)
                    continue
                entities[name] = entity
        return entities

    def __build(self, cur_path):
        res = []
        with open(cur_path) as f:
            data = json.load(f)
            data_array = data['curve']
            last_index = len(data_array) - 1

            # fill not existing levels up to first accessible
            start_level = data_array[0]['x']
            start_res = data_array[0]['y']
            for index in range(start_level - 1):
                res.append(start_res)

            # fill from the table
            for index in range(last_index):
                start_level = data_array[index]['x']
                end_level = data_array[index + 1]['x']
                start_res = data_array[index]['y']
                end_res = data_array[index + 1]['y']
                all_levels = end_level - start_level
                all_res = end_res - start_res
                if all_levels == 0:
                    ratio = 0
                else:
                    ratio = all_res / all_levels
                res.append(start_res)
                for j in range(all_levels - 1):
                    start_res += ratio
                    res.append(start_res)
            res.append(data_array[last_index]['y'])

            # fill app to max_level
            size = len(res)
            if size < self._max_level:
                end_res = data_array[last_index]['y']
                for i in range(size, self._max_level):
                    res.append(end_res)
        return res

    def build_table(self, dicts: {}, need_sort=True):
        rows = [['Name', "Level"] + self._res_names]
        for name in dicts.keys():
            creature_dict = dicts[name]
            for i in range(self._max_level):
                row = [name, i + 1]
                for j in range(len(self._res_names)):
                    row.append(creature_dict[self._res_names[j]][i])
                rows.append(row)
        if need_sort:
            rows.sort(key=lambda x: x[0])
        return rows

    @abstractmethod
    def build_csv_table_with_formulas(self, path: str, dicts: {}):
        pass
