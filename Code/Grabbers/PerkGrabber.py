from Code.Grabbers.GrabberConst import entry_names
from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser

e_type_name = {256: "Ability", 512: "Function"}
v_type_name = {1: "Float", 3: "List", 4: "Activate", 5: "Spell", 8: "Actor", 9: "Item"}
operation = {
    1: "SetValue", 2: "AddValue", 3: "MulValue", 5: "MulAddValue", 6: "Abs", 8: "AddItem", 9: "AddActivate",
    10: "SetSpell", 12: "AddValueToActor", 13: "MultiplyActorValueMultiply?", 14: "MulAddValueToActor",
    16: "SetItem"
}


class PerkGrabber(UnitListener):

    def __init__(self, spel, avif, print=True):
        super().__init__(print)
        self.label = 'PERK'
        self.spel = spel
        self.avif = avif
        self.number = 0
        self.perk = {}

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        name = F76AInst.get_name(unit)
        full = F76AInst.get_full(unit)
        result = {}
        self.perk[idd] = result
        result["id"] = idd
        result["name"] = name
        result["full"] = full
        result["effects"] = []
        effect_blocks = F76GroupParser.get_segments_between(unit, b'PRKE', b'PRKF')
        if effect_blocks.__len__() > 0:
            effects = []
            result["effects"] = effects
            for effect_block in effect_blocks:
                effect = {}
                effects.append(effect)
                prke = F76GroupParser.get_group_segment(effect_block, b'PRKE')
                type_index = F76AInst.get_ushort(prke, 1)
                effect["e_type"] = e_type_name[type_index]
                data = F76GroupParser.get_group_segment(effect_block, b'DATA')
                if type_index == 256:
                    effect['v_type'] = 0
                    effect["spell"], success = F76AInst.get_id_and_resolve(data, 2, self.spel)
                else:
                    entry = F76AInst.get_uchar(data, 2)
                    entry_name = entry_names.get(entry)
                    if entry_name is None:
                        entry_name = str(entry)
                        pid = "None"
                        try:
                            epfb = F76GroupParser.get_group_segment(effect_block, b'EPFB')
                            pid = str(F76AInst.get_uchar(epfb, 2))
                        except:
                            ...
                        print("Entry is None", entry, idd, pid)
                    effect["entry"] = entry_name
                    op = F76AInst.get_uchar(data, 3)
                    op_name = operation.get(op)
                    if op_name is None:
                        op_name = str(op)
                        print("Op is None", op, idd)
                    effect["op"] = op_name
                    effect['v_type'] = 2
                    if op != 6:
                        try:
                            epft = F76GroupParser.get_group_segment(effect_block, b'EPFT')
                            v_type = F76AInst.get_uchar(epft, 2)
                            effect['v_type'] = v_type
                            effect["value"] = self._get_epfd_value(v_type, effect_block, idd)
                        except:
                            print(f"Can't get 'EPFT' for {idd}")
        self.number += 1
        self.print_id(self.label, self.number, idd, name)

    def _get_epfd_value(self, v_type, effect_block, idd):
        if v_type_name.get(v_type) is None:
            print(f"Can't get v-type ({v_type}) for {idd}")
            return ""
        if v_type == 1:
            epfd = F76GroupParser.get_group_segment(effect_block, b'EPFD')
            return F76AInst.get_float(epfd, 2)
        if v_type == 3:
            epfd = F76GroupParser.get_group_segment(effect_block, b'EPFD')
            return F76AInst.get_id(epfd, 2)
        if v_type == 4:
            return ""
        if v_type == 5:
            epfd = F76GroupParser.get_group_segment(effect_block, b'EPFD')
            value, success = F76AInst.get_id_and_resolve(epfd, 2, self.spel)
            return value
        if v_type == 8:
            value = 0
            try:
                epfd = F76GroupParser.get_group_segment(effect_block, b'EPFD')
                value = F76AInst.get_float(epfd, 2)
            except:
                if idd != '00606c85':
                    print("Can't get 'EPFD' for: " + idd)
            epf3 = F76GroupParser.get_group_segment(effect_block, b'EPF3')
            actor1, success = F76AInst.get_id_and_resolve(epf3, 2, self.avif)
            actor2 = ""
            try:
                epf4 = F76GroupParser.get_group_segment(effect_block, b'EPF4')
                actor2, success = F76AInst.get_id_and_resolve(epf4, 2, self.avif)
            except:
                ...
            return {"value": value, "actor1": actor1, "actor2": actor2}
        if v_type == 9:
            epfd = F76GroupParser.get_group_segment(effect_block, b'EPFD')
            return F76AInst.get_id(epfd, 2)

    def resolve_loc_names(self):
        self.name_resolver_dict(self.perk)

    def build_csv_table(self):
        result = [["Id", "Name", "Full Name", "Effects"]]
        for value in self.perk.values():
            row = []
            row.append(value['id'])
            row.append(value['name'])
            row.append(value['full'])
            row.append(value['effects'])

            #if value['id'] == '0031d4bc':
            #    print()
            #if row[3] == "Ability":
            #    row[7] = value['spell']
            #elif row[3] == "Function":
            #    if type(p_value).__name__ == 'float' or type(p_value).__name__ == 'str':
            #        row[6] = p_value
            #    else:
            #        row[7] = str(p_value)
            result.append(row)
        return result
