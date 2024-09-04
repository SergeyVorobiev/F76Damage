from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class HazardGrabber(UnitListener):

    def __init__(self, spel, ench, print=True):
        super().__init__(print)
        self.hazd = {}
        self.spel = spel
        self.ench = ench
        self.number = 0
        self.label = 'HAZD'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.hazd[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        dnam = F76GroupParser.get_group_segment_or_def(unit, b'DNAM')
        effect = {"type": "none", "value": ""}
        result["effect"] = effect
        if dnam:
            result["radius"] = F76AInst.get_float(dnam, 6)
            result["lifeTime"] = F76AInst.get_float(dnam, 10)
            result["interval"] = F76AInst.get_float(dnam, 18)
            effect_id = F76AInst.get_id(dnam, 26)
            if effect_id != '00000000':
                success = self._resolve_effect("Spell", effect, effect_id, self.spel)
                if not success:
                    success = self._resolve_effect("Ench", effect, effect_id, self.ench)
                    if not success:
                        print("Can not resolve hazard effect for '" + idd + "'")
        self.print_id(self.label, self.number, idd, name)

    def _resolve_effect(self, name, effect, e_id, effect_resolver):
        try:
            obj = effect_resolver[e_id]
            effect["type"] = name
            effect["value"] = obj
            return True
        except:
            return False

    def resolve_loc_names(self):
        self.name_resolver_dict(self.hazd)
