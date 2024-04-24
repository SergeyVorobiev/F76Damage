import struct

from Code.Keys.GroupKey import GroupKey


class UKey:
    def __init__(self, g_key: GroupKey):
        value = g_key.value
        self.label = value[0]
        self.l_length = value[0].__len__()
        self.template = value[1]
        if type(value[2]).__name__ == 'int':
            self.format = ''
            self.format_size = value[2]
        else:
            self.format = value[2]
            self.format_size = struct.calcsize(value[2])
        self.func = value[3]
