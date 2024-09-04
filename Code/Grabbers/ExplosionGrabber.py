from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class ExplosionGrabber(UnitListener):

    def __init__(self, curv, dmgt, print=True):
        super().__init__(print)
        self.expl = {}
        self.curv = curv
        self.dmgt = dmgt
        self.number = 0
        self.label = 'EXPL'

    def listen(self, unit: bytes):
        result = {}
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        version = F76AInst.get_version(unit)
        self.expl[idd] = result
        result["id"] = idd
        result["name"] = name
        result["enchantment"] = ""
        try:
            result["enchantment"] = F76AInst.get_id(F76GroupParser.get_group_segment(unit, b'EITM'), 2)
        except:
            ...
        try:
            data = F76GroupParser.get_group_segment(unit, b'DATA')
            result["object"] = ''
            object_id = F76AInst.get_id(data, 18)
            if object_id != '00000000' and object_id != idd:
                result["object"] = object_id
            result["projectile"] = F76AInst.get_id(data, 22)
            if version > 163:
                result["exp_curv"], success = F76AInst.get_id_and_resolve(data, 26, self.curv)
                result["force"] = F76AInst.get_float(data, 30)
                result["damage"] = F76AInst.get_float(data, 34)
            else:
                result["exp_curv"] = ''
                result["force"] = F76AInst.get_float(data, 26)
                result["damage"] = F76AInst.get_float(data, 30)
        except:
            print("Can't find data for " + idd)
        dama_cats = F76GroupParser.find_groups(unit, b'DAMA').get(b'DAMA')
        if dama_cats is None:
            dama_cats = []
        dama_size = dama_cats.__len__()
        if dama_size > 1:
            print("Several 'DAMA' categories in " + result["id"])
        result["d_type"] = ''
        result["d_value"] = 0
        result["d_curv"] = '00000000'
        if dama_size > 0:
            try:
                dama = F76GroupParser.get_group_segment(unit, b'DAMA')
                result["d_type"], success = F76AInst.get_id_and_resolve(dama, 2, self.dmgt)
                result["d_value"] = F76AInst.get_float(dama, 6)
                result["d_curv"], success = F76AInst.get_id_and_resolve(dama, 10, self.curv)
            except:
                print("Can't find data in 'DAMA' for " + idd)
        self.number += 1
        self.print_id(self.label, self.number, idd, name)

    def resolve_enchantments(self, ench):
        for value in self.expl.values():
            try:
                value["enchantment"] = ench[value['enchantment']]
            except:
                ...

    def resolve_projectiles(self, proj):
        for value in self.expl.values():
            try:
                value['projectile'] = proj[value['projectile']]
            except:
                ...

    def resolve_objects(self, hazd, alch, mstt):
        for value in self.expl.values():
            if value['object'] != '':
                if not self._resolve(self.expl, value, "EXPL"):
                    if not self._resolve(hazd, value, "HAZD"):
                        if not self._resolve(alch, value, "ALCH"):
                            if not self._resolve(mstt, value, "MSTT"):
                                ...

    def _resolve(self, effect, value, o_type):
        try:
            value['object'] = {"type": o_type, "value": effect[value['object']]}
            return True
        except:
            return False