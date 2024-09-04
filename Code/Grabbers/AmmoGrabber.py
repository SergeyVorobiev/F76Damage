from Code.Grabbers.CategoryHelper import CategoryHelper
from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class AmmoGrabber(UnitListener):

    def __init__(self, kywd, proj, print=True):
        super().__init__(print)
        self.kywd = kywd
        self.proj = proj
        self.ammo = {}
        self.number = 0
        self.label = 'AMMO'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        self.ammo[idd] = result
        for keyword_name in CategoryHelper.get_KWDA(unit, self.kywd, idd):
            if keyword_name is not None and keyword_name.startswith("AmmoType"):
                result["ammo_type"] = keyword_name[8:]
                break
        try:
            data = F76GroupParser.get_group_segment(unit, b'DATA')
            result['value'] = F76AInst.get_uint(data, 2)
            result['weight'] = F76AInst.get_float(data, 6)
        except:
            print("Can't get 'DATA' for " + idd)

        try:
            dnam = F76GroupParser.get_group_segment(unit, b'DNAM')
            result['projectile'], success = F76AInst.get_id_and_resolve(dnam, 2, self.proj)
            result['damage'] = F76AInst.get_float(dnam, dnam.__len__() - 8)
            result['health'] = F76AInst.get_uint(dnam, dnam.__len__() - 4)
        except:
            print("Can't get 'DNAM' for " + idd)
        self.number += 1
        self.print_id(self.label, self.number, idd, name)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.ammo)
