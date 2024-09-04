from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


# TODO: Resolve additional information
class GlobGrabber(UnitListener):

    def __init__(self, print=True):
        super().__init__(print)
        self.glob = {}
        self.number = 0
        self.label = 'GLOB'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        result = {}
        self.glob[idd] = result
        result["id"] = idd
        result["name"] = name
        fltv = F76GroupParser.get_group_segment(unit, b'FLTV', only_existed=True)
        try:
            result["value"] = F76AInst.get_float(fltv, 2)
        except:
            print(f"Can't get 'FLTV' for {idd}")
        self.number += 1
        UnitListener.print_id(self.label, self.number, idd, name)

