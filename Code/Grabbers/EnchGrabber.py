from Code.Grabbers.CategoryHelper import CategoryHelper
from Code.Grabbers.GrabberConst import type_resolver, target_resolver, e_type_resolver
from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class EnchGrabber(UnitListener):

    def __init__(self, mgef, curv, avif, glob, print=True):
        super().__init__(print)
        self.ench = {}
        self.mgef = mgef
        self.curv = curv
        self.avif = avif
        self.glob = glob
        self.number = 0
        self.label = 'ENCH'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.ench[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        enit = F76GroupParser.get_group_segment(unit, b'ENIT')
        size = enit.__len__()
        # result["b_ench"] = F76AInst.get_id(enit, size - 8)
        result["type"] = type_resolver[F76AInst.get_uint(enit, size - 16)]
        result["target"] = target_resolver[F76AInst.get_uint(enit, size - 20)]
        result["e_type"] = e_type_resolver[F76AInst.get_uint(enit, size - 28)]
        result['mag_effects'] = CategoryHelper.get_mag_effects(unit, idd, self.mgef, self.curv, self.avif, self.glob)
        if F76AInst.get_id(enit, size - 8) != '00000000':
            print("Base enchantments id is found! " + idd)
        self.number += 1
        self.print_id(self.label, self.number, idd, name)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.ench)
