import struct

from Code.Decoders.Categories.UCat import UCat


class Category:

    def __init__(self, data: {}, segment: bytes):
        self.__data = data
        self.__segment = segment

    @classmethod
    def from_dict(cls, dictionary):
        return cls(dictionary['data'], dictionary['segment'])

    @classmethod
    def from_union(cls, ucat: UCat):
        dictionary = ucat.value
        return cls(dictionary['data'], dictionary['segment'])

    @property
    def data(self):
        return self.__data

    @property
    def segment(self):
        return self.__segment

    def decode(self, unit) -> {}:
        data = {}
        start = -1
        if self.__segment is not None:
            start = unit.find(self.__segment)
            if start != -1:
                start += self.__segment.__len__()
        for name, value in self.__data.items():
            try:
                if type(value).__name__ == 'tuple' and start > -1:
                    length = struct.calcsize(value[0])
                    s = start + value[1]
                    block = unit[s: s + length]
                    data[name] = struct.unpack(value[0], block)[0]
                else:  # consider it as a function
                    data[name] = value(unit)
            except:
                data[name] = None
        return data
