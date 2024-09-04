from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser
from Code.Mods.Mod import Mod
from Code.Mods.ModHelper import ModHelper


class ModGrabber(UnitListener):

    def __init__(self, curv, dmgt, avif, ench, kywd, ammo, proj, spel, print=True):
        super().__init__(print)
        self.mods = {}
        self.curv = curv
        self.dmgt = dmgt
        self.avif = avif
        self.ench = ench
        self.kywd = kywd
        self.ammo = ammo
        self.proj = proj
        self.spel = spel
        self.number = 0
        self.label = "OMOD"

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        props, full_name, attach_id = ModHelper.get_weap_properties(unit)
        target_ids = []
        try:
            bytes = F76GroupParser.get_group_segment(unit, b'MNAM')
            start = 2
            while start < bytes.__len__():
                target_ids.append(F76AInst.get_id(bytes, start))
                start += 4
        except:
            #  if not name.startswith("modcol") and not name.startswith("Debug"):
            #    print(f"Can't get target ids from 'MNAM' for '{idd}' '{name}'")
            ...
        if not (props is None and full_name is None and attach_id is None):
            self.mods[idd] = Mod(idd, name, full_name, attach_id, target_ids, props)
            self.number += 1
            self.print_id(self.label, self.number, idd, name)

    def resolve_mods(self):
        def bytes_getter(mod):
            return mod.full_name_bytes

        def name_setter(mod, name):
            mod.localized_name = name

        def items_iter(items):
            return items.values()

        F76AInst.resolve_localized_names(self.mods, items_iter, bytes_getter, name_setter)

        for mod in self.mods.values():
            mod.gather_properties(self.mods)
            mod.resolve_dmg_types(self.dmgt)
            mod.resolve_avif(self.avif)
            mod.resolve_effects(self.ench)
            mod.resolve_kywd(self.kywd)
            mod.resolve_ammo(self.ammo)
            mod.resolve_proj(self.proj)
            mod.resolve_spell(self.spel)
            mod.replace_curves_ids(self.curv, "TabID")
