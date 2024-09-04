import sys

sys.path.append("..")

import Root
from Code.Grabbers.AVIFGrabber import AVIFGrabber
from Code.Grabbers.AlchemyGrabber import AlchemyGrabber
from Code.Grabbers.EnchGrabber import EnchGrabber
from Code.Grabbers.GlobGrabber import GlobGrabber
from Code.Grabbers.HazardGrabber import HazardGrabber
from Code.Grabbers.MGEFGrabber import MGEFGrabber
from Code.Grabbers.MSTTGrabber import MSTTGrabber
from Code.Grabbers.SpelGrabber import SpelGrabber
from Code.Grabbers.AmmoGrabber import AmmoGrabber
from Code.Grabbers.DMGTGrabber import DMGTGrabber
from Code.Grabbers.ExplosionGrabber import ExplosionGrabber
from Code.Grabbers.KeywordGrabber import KeywordGrabber
from Code.Grabbers.ProjectileGrabber import ProjectileGrabber
from Code.Grabbers.CurvGrabber import CurvGrabber
from Code.Helpers.F76AInst import F76AInst
from CMD.Config import Config
from Code.Decoders.BaseDecoder import BaseDecoder
from Code.Decoders.Templates.F76DTemplates import F76DecTemplates
from Code.Helpers import Printing
from Code.Helpers.CSV import CSV
from Code.Units.UnitSeparator import UnitSeparator

e_type = {}


def e_type_listener(unit: bytes):
    idd = F76AInst.get_id(unit)
    name = F76AInst.get_name(unit)
    e_type[idd] = name


def resolve_at_points(weapons_table, tags):
    for weapon in weapons_table:
        points = []
        point_ids = weapon["AT_POINTS"]
        for point_id in point_ids:
            try:
                point_name = tags[point_id]
            except:
                point_name = ""
            points.append(point_id + "_" + point_name)
        weapon['AT_POINTS'] = " / ".join(points)


def resolve_damage(curv_grabber, weapons_table, dmgt):
    for weapon in weapons_table:
        damages = weapon['DAMAGE']
        all = []
        if damages.__len__() > 0:
            for damage in damages:
                result = {}
                result["value"] = damage[1]
                result["curv"] = damage[2]
                if damage[2] is not None and damage[2] != '' and damage[2] != '00000000':
                    result["curv"] = curv_grabber.curv[damage[2]].split("\n")
                if damage[0] == '':
                    result["type"] = dmgt['00060a87']
                else:
                    result["type"] = dmgt[damage[0]]
                all.append(result)
        weapon['DAMAGE'] = all


def resolve_ammo(weapons_table, ammo):
    for weapon in weapons_table:
        ammo_id = weapon['AMMO']
        if ammo_id == '00000000':
            weapon['AMMO'] = "None"
        else:
            try:
                ammo_obj = ammo[ammo_id]
                ammo_name = ammo_obj['name']
                if ammo_name.startswith("crAmmo"):
                    ammo_name = ammo_name[6:]
                elif ammo_name.startswith("zzz_Ammo"):
                    ammo_name = ammo_name[8:]
                elif ammo_name.startswith("POST_AmmoDLC05_"):
                    ammo_name = ammo_name[15:]
                elif ammo_name.startswith("DLC01_"):
                    ammo_name = ammo_name[6:]
                elif ammo_name.startswith("DLC03_"):
                    ammo_name = ammo_name[6:]
                elif ammo_name.startswith("DLC04_"):
                    ammo_name = ammo_name[6:]
                elif ammo_name.startswith("EN02_"):
                    ammo_name = ammo_name[5:]
                elif ammo_name.startswith("Ammo_"):
                    ammo_name = ammo_name[5:]
                elif ammo_name.startswith("Ammo"):
                    ammo_name = ammo_name[4:]
                if ammo_name.startswith("DLC01_"):
                    ammo_name = ammo_name[6:]
                elif ammo_name.startswith("DLC03_"):
                    ammo_name = ammo_name[6:]
                elif ammo_name.startswith("DLC04_"):
                    ammo_name = ammo_name[6:]
                ammo_obj['name'] = ammo_name
                weapon['AMMO'] = ammo_obj
            except:
                print("Can't find ammo for id: " + str(ammo_id) + " " + weapon['NAME'])


def resolve_proj(weapons_table, proj):
    for weapon in weapons_table:
        proj_id = weapon['PROJ_TYPE']
        try:
            weapon['PROJ_TYPE'] = proj[proj_id]
        except:
            ...


def resolve_crit(weapons_table, spell):
    for weapon in weapons_table:
        spell_obj = weapon['CRIT']
        try:
            spell_obj["spell"] = spell[spell_obj["spell"]]
        except:
            ...


def resolve_weapon_ench(weapons_table, ench):
    for weapon in weapons_table:
        ench_id = weapon['WEAP_EFFECT']
        try:
            if ench_id != '':
                weapon['WEAP_EFFECT'] = ench[ench_id]
        except:
            print("Can't find ench id: " + str(ench_id) + " " + weapon['NAME'])


def resolve_tags(weapons_table, tags):
    for weapon in weapons_table:
        tag_ids = weapon['TAGS']
        tag_names = []
        ma = []
        for tag_id in tag_ids:
            try:
                tag_name = tags[tag_id]
                if tag_name.startswith("WeaponType"):
                    tag_name = tag_name[10:]
                elif tag_name.startswith("ma_"):
                    ma.append(tag_id + "_" + tag_name)
                else:
                    continue
            except:
                tag_name = tag_id
            tag_names.append(tag_name)
        weapon['TAGS'] = tag_names
        weapon['MA'] = " / ".join(ma)


def resolve_equip(weapons_table):
    for weapon in weapons_table:
        eq_id = weapon['EQTYPE']
        try:
            weapon['EQTYPE'] = e_type[eq_id]
        except:
            print("Can't find type for id: " + str(eq_id) + " " + weapon['NAME'])


def parse_weapon_data(config):
    curv_path = Root.build_path(Root.RESOURCES, config.get_string("Weapon.Mod", "CurveTablesPath"))
    curv_grabber = CurvGrabber(curv_path)
    w_sort = config.get_string("Weapon", "Sort")
    ignore = [s.strip() for s in config.get_string("Weapon", "IgnoreIfNameStartsWith").split(",")]

    glob_grabber = GlobGrabber()
    avif_grabber = AVIFGrabber()
    dmgt_grabber = DMGTGrabber()
    kywd_grabber = KeywordGrabber()
    expl_grabber = ExplosionGrabber(curv_grabber.curv, dmgt_grabber.dmgt)
    proj_grabber = ProjectileGrabber(expl_grabber.expl)
    ammo_grabber = AmmoGrabber(kywd_grabber.kywd, proj_grabber.proj)
    mgef_grabber = MGEFGrabber(avif_grabber.avif, kywd_grabber.kywd, proj_grabber.proj, expl_grabber.expl)
    spel_grabber = SpelGrabber(mgef_grabber.mgef, curv_grabber.curv, avif_grabber.avif, glob_grabber.glob)
    ench_grabber = EnchGrabber(mgef_grabber.mgef, curv_grabber.curv, avif_grabber.avif, glob_grabber.glob)

    hazd_grabber = HazardGrabber(spel_grabber.spel, ench_grabber.ench)
    alch_grabber = AlchemyGrabber()
    mstt_grabber = MSTTGrabber(spel_grabber.spel, expl_grabber.expl, hazd_grabber.hazd)
    decoders = [
        BaseDecoder(F76DecTemplates.WEAPON).print_result(Printing.print_f76_weapon),
        BaseDecoder(F76DecTemplates.CURVE).listen(curv_grabber.listen, listen_only=True).on_finish_listener(
            curv_grabber.resolve_jsons),
        BaseDecoder(F76DecTemplates.GLOB).listen(glob_grabber.listen, listen_only=True),
        BaseDecoder(F76DecTemplates.AVIF).listen(avif_grabber.listen, listen_only=True).on_finish_listener(
            avif_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.DMGT).listen(dmgt_grabber.listen, listen_only=True).on_finish_listener(
            dmgt_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.KYWD).listen(kywd_grabber.listen, listen_only=True),
        BaseDecoder(F76DecTemplates.EXPL).listen(expl_grabber.listen, listen_only=True),
        BaseDecoder(F76DecTemplates.PROJECTILES).listen(proj_grabber.listen, listen_only=True).on_finish_listener(
            proj_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.AMMO).listen(ammo_grabber.listen, listen_only=True).on_finish_listener(
            ammo_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.MGEF).listen(mgef_grabber.listen, listen_only=True).on_finish_listener(
            mgef_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.SPEL).listen(spel_grabber.listen, listen_only=True).on_finish_listener(
            spel_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.ENCHANTMENTS).listen(ench_grabber.listen, listen_only=True).on_finish_listener(
            ench_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.HAZARDS).listen(hazd_grabber.listen, listen_only=True).on_finish_listener(
            hazd_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.ALCHEMY).listen(alch_grabber.listen, listen_only=True).on_finish_listener(
            alch_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.MSTT).listen(mstt_grabber.listen, listen_only=True),
        BaseDecoder(F76DecTemplates.EQUP).listen(e_type_listener, listen_only=True),
    ]
    master = config.get_string("ESM", "F76Master")
    UnitSeparator.separate_and_decode_file(master, decoders)
    expl_grabber.resolve_projectiles(proj_grabber.proj)
    expl_grabber.resolve_enchantments(ench_grabber.ench)
    expl_grabber.resolve_objects(hazd_grabber.hazd, alch_grabber.alch, mstt_grabber.mstt)
    data = decoders[0].get_data()
    resolve_ammo(data, ammo_grabber.ammo)
    resolve_proj(data, proj_grabber.proj)
    resolve_tags(data, kywd_grabber.kywd)
    resolve_equip(data)
    resolve_at_points(data, kywd_grabber.kywd)
    resolve_damage(curv_grabber, data, dmgt_grabber.dmgt)
    resolve_crit(data, spel_grabber.spel)
    resolve_weapon_ench(data, ench_grabber.ench)

    def bytes_getter(item):
        return item['LOCALIZED_NAME']

    def name_setter(item, name):
        item['LOCALIZED_NAME'] = name

    def items_iter(items):
        return items

    F76AInst.resolve_localized_names(data, items_iter, bytes_getter, name_setter)
    table, range_table, melee_table, thrown_table, unarmed_table = CSV.build_weapon_table(data, w_sort, ignore)
    return table, range_table, melee_table, thrown_table, unarmed_table


if __name__ == '__main__':
    config = Config()
    sort = config.get_string("Weapon", "Sort")
    path = config.build_result_path(config.get_string("Weapon", "CSVName"), "csv")
    r_path = config.build_result_path(config.get_string("Weapon", "CSVRange"), "csv")
    m_path = config.build_result_path(config.get_string("Weapon", "CSVMelee"), "csv")
    t_path = config.build_result_path(config.get_string("Weapon", "CSVThrown"), "csv")
    u_path = config.build_result_path(config.get_string("Weapon", "CSVUnarmed"), "csv")
    delimiter = config.get_string("CSV", "Delimiter", 1)
    table, range_table, melee_table, thrown_table, unarmed_table = parse_weapon_data(config)
    CSV.save_table(path, table, delimiter)
    CSV.save_table(r_path, range_table, delimiter)
    CSV.save_table(m_path, melee_table, delimiter)
    CSV.save_table(t_path, thrown_table, delimiter)
    CSV.save_table(u_path, unarmed_table, delimiter)
