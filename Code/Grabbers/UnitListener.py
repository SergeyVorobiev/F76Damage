import json
import os
from abc import abstractmethod

from Code.Helpers.F76AInst import F76AInst


class UnitListener:

    def __init__(self, print=True):
        self.print = print

    @abstractmethod
    def listen(self, unit: bytes):
        ...

    @staticmethod
    def print_id(keyword, number, idd, name):
        if print and name.__len__() < 75:
            print("".ljust(100), end='\r')
            print(keyword, number, idd, name, end='\r')

    @staticmethod
    def load_json_data(c_id, curv_table, curv_path):
        if c_id != '' and c_id != '00000000':
            path_ = curv_table[c_id]
            full_path = os.path.join(curv_path, path_.lower())
            json_data = UnitListener._get_data_from_json(full_path)
            return path_, str(json_data)
        return "", c_id

    @staticmethod
    def _get_data_from_json(cur_path):
        try:
            with open(cur_path) as f:
                return json.load(f)
        except:
            return "{Can't extract data}"

    # collection is an array of data where 'index' item must be an array of bytes related to full name
    def name_resolver_array(self, collection, index=1):
        def bytes_getter(item):
            return item[index]

        def name_setter(item, name):
            if self.print and name.__len__() < 100:
                print("".ljust(100), end='\r')
                print(name, end='\r')
            item[index] = name

        def items_iter(items):
            return items.values()

        F76AInst.resolve_localized_names(collection, items_iter, bytes_getter, name_setter)

    def name_resolver_dict(self, collection, key="full"):
        def bytes_getter(item):
            return item[key]

        def name_setter(item, name):
            if self.print and name.__len__() < 100:
                print("".ljust(100), end='\r')
                print(name, end='\r')
            item[key] = name

        def items_iter(items):
            return items.values()

        F76AInst.resolve_localized_names(collection, items_iter, bytes_getter, name_setter)
