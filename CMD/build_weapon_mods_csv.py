import sys

sys.path.append("..")
import Root
from CMD.Config import Config
from Code.Decoders.BaseDecoder import BaseDecoder
from Code.Decoders.Templates.F76DTemplates import F76DecTemplates
from Code.Helpers.CSV import CSV
from Code.Helpers.F76AInst import F76AInst
from Code.Mods.Mod import Mod
from Code.Mods.ModHelper import ModHelper
from Code.Units.UnitSeparator import UnitSeparator

mods = {}
curv = {}
dmgt = {}
mc = 0
cc = 0


def mod_listener(unit: bytes):
    global mc
    mc += 1
    idd = F76AInst.get_id(unit)
    name = F76AInst.get_name(unit)

    print("".ljust(100), end='\r')
    print(mc, idd, name, end='\r')
    props = ModHelper.get_weap_properties(unit)
    if props is not None:
        mod = Mod(idd, name, props)
        global mods
        mods[idd] = mod


def curv_listener(unit: bytes):
    idd = F76AInst.get_id(unit)
    index = unit.find(b'JASF')
    if index < 0:
        index = unit.find(b'CRVE')
    global cc
    cc += 1
    if index > -1:
        path_ = unit[index + 6:].partition(b'\x00')[0].decode('latin-1')
        curv[idd] = path_
    print("".ljust(100), end='\r')
    print(cc, idd, end='\r')


def dmgt_listener(unit: bytes):
    idd = F76AInst.get_id(unit)
    name = F76AInst.get_name(unit)[2:]
    dmgt[idd] = name


def prepare_weapon_mods_table(config):
    decoders = [
        BaseDecoder(F76DecTemplates.CURVE).listen(curv_listener, listen_only=True),
        BaseDecoder(F76DecTemplates.DMGT).listen(dmgt_listener, listen_only=True),
        BaseDecoder(F76DecTemplates.OMOD_WEAP).listen(mod_listener, listen_only=True)
    ]
    master = config.get_string("ESM", "F76Master")
    nw = config.get_string("ESM", "F76NW")
    curve_path = config.get_string("Weapon.Mod", "CurveTablesPath")
    json_path = Root.build_path(Root.RESOURCES, curve_path)
    exclude_props = [s.strip() for s in
                     config.get_string("Weapon.Mod", "ExcludeModsWithProps", allow_empty=True).split(",")]
    ignore_props = [s.strip() for s in config.get_string("Weapon.Mod", "IgnoreProps", allow_empty=True).split(",")]
    ignore_empty = config.get_bool("Weapon.Mod", "IgnoreEmptyMods")
    UnitSeparator.separate_and_decode_file(master, decoders)
    UnitSeparator.separate_and_decode_file(nw, decoders)
    for mod in mods.values():
        mod.gather_properties(mods)
        mod.replace_curves_ids(curv, json_path)
        mod.resolve_dgm_types(dmgt)
    table = [["ID", "Name", "ID", "AppType", "Property", "Val1", "Val2", "Curve"]]
    for mod in mods.values():
        if mod.contains_props(exclude_props):
            continue
        mod.as_csv_table(table, ignore_props, ignore_empty)
    return table


if __name__ == '__main__':
    config = Config()
    table = prepare_weapon_mods_table(config)
    delimiter = config.get_string("CSV", "Delimiter", 1)
    path = config.build_result_path(config.get_string("Weapon.Mod", "CSVName"), "csv")
    CSV.build_table(path, table, delimiter)
    print("\nSuccess\n")
