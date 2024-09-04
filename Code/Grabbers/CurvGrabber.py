import os

from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst


class CurvGrabber(UnitListener):

    def __init__(self, curv_path, print=True):
        super().__init__(print)
        self.curv_path = curv_path
        self.print = print
        self.number = 0
        self.curv = {}
        self.label = 'CRVE'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        index = unit.find(b'JASF')
        if index < 0:
            index = unit.find(b'CRVE')
        self.number += 1
        path = ""
        if index > -1:
            path = unit[index + 6:].partition(b'\x00')[0].decode('latin-1')
            self.curv[idd] = path
        self.print_id(self.label, self.number, idd, path)

    def resolve_jsons(self):
        for item in self.curv.items():
            idd = item[0]
            path = item[1]
            full_path = os.path.join(self.curv_path, path.lower())
            json_data = UnitListener._get_data_from_json(full_path)
            self.curv[idd] = path + "\n" + str(json_data)

    # Deprecated
    def resolve_json_path(self, c_id):
        path, json_data = self.load_json_data(c_id, self.curv, self.curv_path)
        return path + "\n" + str(json_data)
