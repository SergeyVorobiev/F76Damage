from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst


# TODO: Resolve additional information
class AVIFGrabber(UnitListener):

    def __init__(self, print=True):
        super().__init__(print)
        self.avif = {}
        self.avif['00000310'] = {"id": "00000310", "name": "AbsorbChance", "full": ""}
        self.number = 0
        self.label = 'AVIF'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.avif[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        self.number += 1
        UnitListener.print_id(self.label, self.number, idd, name)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.avif)
