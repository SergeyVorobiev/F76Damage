from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class ProjectileGrabber(UnitListener):

    def __init__(self, expl):
        super().__init__()
        self.proj = {}
        self.expl = expl

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        self.proj[idd] = result
        try:
            dstds = F76GroupParser.get_group_segment(unit, b'DSTD', -1, only_existed=True)
        except:
            dstds = []
        if dstds.__len__() == 0:
            result["destructible"] = ""
        elif dstds.__len__() == 1:
            exp_id = F76AInst.get_id(dstds[0], 10)
            try:
                result["destructible"] = self.expl[exp_id]
            except:
                result["destructible"] = ""
                if exp_id != '00000000':
                    print(f"Found wrong destructible id {exp_id} in {idd}")
        else:
            print(f"Destructibles for {idd} are more than one, no one is taken")
        dnam = F76GroupParser.get_group_segment(unit, b'DNAM')
        result["gravity"] = F76AInst.get_float(dnam, 6)
        result["speed"] = F76AInst.get_float(dnam, 10)
        result["range"] = F76AInst.get_float(dnam, 14)
        result["expl"], success = F76AInst.get_id_and_resolve(dnam, 34, self.expl)
        result["relaunch"] = F76AInst.get_float(dnam, 78)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.proj)