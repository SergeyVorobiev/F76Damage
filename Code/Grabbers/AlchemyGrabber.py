from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst


class AlchemyGrabber(UnitListener):

    def __init__(self, print=True):
        super().__init__(print)
        self.alch = {}
        self.number = 0
        self.label = 'ALCH'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.alch[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        self.print_id(self.label, self.number, idd, name)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.alch)
