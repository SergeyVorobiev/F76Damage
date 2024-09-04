from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst


class KeywordGrabber(UnitListener):

    def __init__(self, print=True):
        super().__init__(print)
        self.kywd = {}
        self.number = 0
        self.label = 'KYWD'

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        self.kywd[idd] = name
        self.number += 1
        self.print_id(self.label, self.number, idd, name)

