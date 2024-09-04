from Code.Grabbers.CategoryHelper import CategoryHelper
from Code.Grabbers.GrabberConst import type_resolver, e_type_resolver, target_resolver
from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class SpelGrabber(UnitListener):
    def __init__(self, mgef, curv, avif, glob, print=True):
        super().__init__(print)
        self.spel = {}
        self.mgef = mgef
        self.curv = curv
        self.avif = avif
        self.glob = glob
        self.number = 0
        self.label = 'SPEL'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.spel[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        spit = F76GroupParser.get_group_segment(unit, b'SPIT')
        size = spit.__len__()
        result['type'] = type_resolver[F76AInst.get_uint(spit, size - 28)]
        result['time'] = F76AInst.get_float(spit, size - 24)
        result['e_type'] = e_type_resolver[F76AInst.get_uint(spit, size - 20)]
        result['target'] = target_resolver[F76AInst.get_uint(spit, size - 16)]
        result['duration'] = F76AInst.get_float(spit, size - 12)
        result['range'] = F76AInst.get_float(spit, size - 8)
        result['perk'] = F76AInst.get_id(spit, size - 4)
        result['mag_effects'] = CategoryHelper.get_mag_effects(unit, idd, self.mgef, self.curv, self.avif, self.glob)
        self.number += 1
        self.print_id(self.label, self.number, idd, name)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.spel)

    def build_csv_table(self):
        result = [["Id", "Name", "Full Name", "Type", "Time", "Activity", "Target", "Duration", "Range", "Perk", "Effects"]]
        for value in self.spel.values():
            row = []
            row.append(value['id'])
            row.append(value['name'])
            full_name = value['full']
            if full_name == "Â¢Scout's Code":
                full_name = "Scout's Code"
            elif full_name == "Â¢Scout's Call":
                full_name = "Scout's Call"
            elif full_name == "Â¢Scout's Courage":
                full_name = "Scout's Courage"
            row.append(full_name)
            row.append(value['type'])
            row.append(value['time'])
            row.append(value['e_type'])
            row.append(value['target'])
            row.append(value['duration'])
            row.append(value['range'])
            row.append(value['perk'])
            row.append(value['mag_effects'])
            result.append(row)
        return result
