import fnmatch

from Code.Keys.UKey import UKey


class UnitData:
    def __init__(self, s_key: UKey, e_key: UKey, max_unit_length: int = 0, size_func=None):
        self.__s_key = s_key
        self.__e_key = e_key
        self.__c_key = s_key
        self.__start = True
        self.__max_unit_length = max_unit_length
        self.__size_func = size_func

    @property
    def c_key(self):
        return self.__c_key

    @property
    def s_key(self):
        return self.__s_key

    @property
    def e_key(self):
        return self.__e_key

    @property
    def max_unit_length(self):
        return self.__max_unit_length

    def set_start(self, start):
        self.__start = start
        if start:
            self.__c_key = self.__s_key
        else:
            self.__c_key = self.__e_key

    def match(self, part: bytes) -> (bool, int):
        if self.__c_key.template is None or fnmatch.fnmatch(part, self.__c_key.template):
            if self.__c_key.func is None or self.__c_key.func(part):
                if self.__start:
                    return True, self.unit_size(part)
                return True, 0
        return False, 0

    def unit_size(self, part) -> int:
        if self.__size_func is not None:
            size = self.__size_func(part)
            if size <= 0:
                print(f"Wrong size for part: {part}")
            else:
                return self.__size_func(part)
        return 0
