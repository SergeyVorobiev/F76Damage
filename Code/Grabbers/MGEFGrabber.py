from Code.Grabbers.CategoryHelper import CategoryHelper
from Code.Grabbers.GrabberConst import e_type_resolver, target_resolver, a_type_resolver
from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class MGEFGrabber(UnitListener):
    def __init__(self, avif, kywd, proj, expl, print=True):
        super().__init__(print)
        self.mgef = {}
        self.avif = avif
        self.kywd = kywd
        self.proj = proj
        self.expl = expl
        self.number = 0
        self.label = 'MGEF'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.mgef[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        result["keywords"] = CategoryHelper.get_KWDA(unit, self.kywd, idd)
        try:
            data = F76GroupParser.get_group_segment(unit, b'DATA')
            result["resist"], success = F76AInst.get_id_and_resolve(data, 22, self.avif)
            result["actor_value1"], success = F76AInst.get_id_and_resolve(data, 74, self.avif)
            result["projectile"], success = F76AInst.get_id_and_resolve(data, 78, self.proj)
            result["explosion"], success = F76AInst.get_id_and_resolve(data, 82, self.expl)
            a_type = F76AInst.get_uint(data, 70)
            e_type = F76AInst.get_uint(data, 86)
            target = F76AInst.get_uint(data, 90)
            try:
                e_type = e_type_resolver[e_type]
            except:
                print("Can't resolve 'e_type' for " + idd + " value: " + str(e_type))
            try:
                target = target_resolver[target]
            except:
                print("Can't resolve 'target' for " + idd + " value: " + str(target))
            try:
                a_type = a_type_resolver[a_type]
            except:
                print("Can't resolve 'a_type' for " + idd + " value: " + str(a_type))
            result['a_type'] = a_type
            result['e_type'] = e_type
            result['target'] = target
            result["actor_value2"], success = F76AInst.get_id_and_resolve(data, 94, self.avif)
            ability = F76AInst.get_id(data, 134)
            result["ability"] = ability  # SPEL
            if ability != '00000000':
                print("\nAbility is found " + idd + "\n")
            result["perk"] = F76AInst.get_id(data, 142)
        except:
            g = F76GroupParser.find_groups(unit, b'DATA')[b'DATA'][0]
            index = g[0] + g[1]
            print("Can't parse 'DATA' for " + idd, "Next 4 bytes: " + str(unit[index: index + 4]))

        self.number += 1
        self.print_id(self.label, self.number, idd, name)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.mgef)
