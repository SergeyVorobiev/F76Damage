import csv
from abc import abstractmethod

from Code.Decoders.Categories.Category import Category
from Code.Decoders.Categories.UCat import UCat
from Code.Helpers.ColorPrint import cprintln, pc
from Code.Keys.GroupKey import GroupKey
from Code.Keys.UKey import UKey
from Code.Units.UnitData import UnitData


class AbstractDecoder:

    def __init__(self, start_key: GroupKey, end_key: GroupKey, categories: [UCat], max_unit_length: int = 0,
                 size_func=None, filter_func=None):
        self.__unit = UnitData(UKey(start_key), UKey(end_key), max_unit_length, size_func)
        self.__listener = None
        self.__only_listener = False
        self.__on_finish_listener = None
        self._categories = [Category.from_union(ucat) for ucat in categories]
        self._header = []
        self._table = []
        self._print = None
        self._print_u = False
        self.__filter_func = filter_func
        for category in self._categories:
            self._header += list(category.data.keys())

    @property
    def unit(self):
        return self.__unit

    @abstractmethod
    def before_start(self):
        pass

    def decode_unit(self, unit: bytes):
        if self.__filter_func is not None and not self.__filter_func(unit):
            return
        if self.__listener is not None:
            self.check_max_size(unit)
            self.__listener(unit)
        if not self.__only_listener:
            result = {}
            self.check_max_size(unit)
            for category in self._categories:
                result.update(category.decode(unit))
            self._table.append(result)
            self.decoded(unit, result)
            if self._print is not None:
                self._print(unit, result)
            if self._print_u:
                print(unit)

    def to_csv(self, path, delimiter=",", sort=None):
        if sort is not None and sort != "None":
            self._table.sort(key=lambda r: r[sort])
        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=delimiter, fieldnames=self._header)
            writer.writeheader()
            writer.writerows(self._table)

    @abstractmethod
    def decoded(self, unit: bytes, result: {}):
        pass

    def on_finish(self):
        if self.__on_finish_listener is not None:
            self.__on_finish_listener()

    def on_finish_listener(self, listener):
        self.__on_finish_listener = listener
        return self

    def listen(self, listener, listen_only: bool = False):
        self.__only_listener = listen_only
        self.__listener = listener
        return self

    def print_result(self, fun):
        self._print = fun
        return self

    def print_unit(self, flag: bool):
        self._print_u = flag
        return self

    def check_max_size(self, unit: bytes):
        if unit.__len__() == self.__unit.max_unit_length:
            message = f"({self.__unit.s_key.label}) Found a unit with max block length, {self.__unit.max_unit_length} possibly is not enough"
            cprintln(message, pc.b_yellow, pc.magenta)

    def get_data(self):
        return self._table
