import os
import sys

sys.path.append("..")

import Root
from Code.Grabbers.AlchemyGrabber import AlchemyGrabber
from Code.Grabbers.HazardGrabber import HazardGrabber
from Code.Grabbers.MSTTGrabber import MSTTGrabber
from Code.Grabbers.GlobGrabber import GlobGrabber
from Code.Grabbers.AVIFGrabber import AVIFGrabber
from Code.Grabbers.AmmoGrabber import AmmoGrabber
from Code.Grabbers.CurvGrabber import CurvGrabber
from Code.Grabbers.DMGTGrabber import DMGTGrabber
from Code.Grabbers.EnchGrabber import EnchGrabber
from Code.Grabbers.ExplosionGrabber import ExplosionGrabber
from Code.Grabbers.KeywordGrabber import KeywordGrabber
from Code.Grabbers.MGEFGrabber import MGEFGrabber
from Code.Grabbers.ModGrabber import ModGrabber
from Code.Grabbers.PerkGrabber import PerkGrabber
from Code.Grabbers.ProjectileGrabber import ProjectileGrabber
from Code.Grabbers.SpelGrabber import SpelGrabber
from CMD.Config import Config
from Code.Decoders.BaseDecoder import BaseDecoder
from Code.Decoders.Templates.F76DTemplates import F76DecTemplates
from Code.Helpers.CSV import CSV
from Code.Units.UnitSeparator import UnitSeparator


def prepare_weapon_mods_table(config):
    curve_path = Root.build_path(Root.RESOURCES, config.get_string("Weapon.Mod", "CurveTablesPath"))
    curv_grabber = CurvGrabber(curve_path)
    glob_grabber = GlobGrabber()
    avif_grabber = AVIFGrabber()
    dmgt_grabber = DMGTGrabber()
    kywd_grabber = KeywordGrabber()
    expl_grabber = ExplosionGrabber(curv_grabber.curv, dmgt_grabber.dmgt)
    proj_grabber = ProjectileGrabber(expl_grabber.expl)
    ammo_grabber = AmmoGrabber(kywd_grabber.kywd, proj_grabber.proj)

    # Contains not resolved perk ids
    mgef_grabber = MGEFGrabber(avif_grabber.avif, kywd_grabber.kywd, proj_grabber.proj, expl_grabber.expl)
    spel_grabber = SpelGrabber(mgef_grabber.mgef, curv_grabber.curv, avif_grabber.avif, glob_grabber.glob)
    ench_grabber = EnchGrabber(mgef_grabber.mgef, curv_grabber.curv, avif_grabber.avif, glob_grabber.glob)

    hazd_grabber = HazardGrabber(spel_grabber.spel, ench_grabber.ench)
    alch_grabber = AlchemyGrabber()
    mstt_grabber = MSTTGrabber(spel_grabber.spel, expl_grabber.expl, hazd_grabber.hazd)

    perk_grabber = PerkGrabber(spel_grabber.spel, avif_grabber.avif)
    mod_grabber = ModGrabber(curv_grabber.curv, dmgt_grabber.dmgt, avif_grabber.avif, ench_grabber.ench,
                             kywd_grabber.kywd,
                             ammo_grabber.ammo, proj_grabber.proj, spel_grabber.spel)

    decoders = [
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
        BaseDecoder(F76DecTemplates.PERK).listen(perk_grabber.listen, listen_only=True).on_finish_listener(
            perk_grabber.resolve_loc_names),
        BaseDecoder(F76DecTemplates.OMOD_WEAP).listen(mod_grabber.listen, listen_only=True),
    ]

    f76_folder = config.get_string("ESM", "F76Folder")
    master = f76_folder + os.sep + config.get_string("ESM", "F76Master")
    exclude_props = [s.strip() for s in
                     config.get_string("Weapon.Mod", "ExcludeModsWithProps", allow_empty=True).split(",")]
    ignore_props = [s.strip() for s in config.get_string("Weapon.Mod", "IgnoreProps", allow_empty=True).split(",")]
    ignore_empty = config.get_bool("Weapon.Mod", "IgnoreEmptyMods")

    UnitSeparator.separate_and_decode_file(master, decoders)
    expl_grabber.resolve_projectiles(proj_grabber.proj)
    expl_grabber.resolve_enchantments(ench_grabber.ench)
    expl_grabber.resolve_objects(hazd_grabber.hazd, alch_grabber.alch, mstt_grabber.mstt)
    mod_grabber.resolve_mods()
    mod_table = [
        ["ID", "Name", "LocalizedName", "ID", "AttachPoint", "TargetIds", "AppType", "Property", "Val1", "Val2",
         "Enchantment", "Curve"]]
    for mod in mod_grabber.mods.values():
        if mod.contains_props(exclude_props):
            continue
        mod.as_csv_table(mod_table, ignore_props, ignore_empty)
    return mod_table, perk_grabber.build_csv_table(), spel_grabber.build_csv_table()


if __name__ == '__main__':
    print("Starting to build weapon mods data")
    config = Config()
    mods, perks, spells = prepare_weapon_mods_table(config)
    delimiter = config.get_string("CSV", "Delimiter", 1)
    mod_path = config.build_result_path(config.get_string("Weapon.Mod", "CSVName"), "csv")
    perk_path = config.build_result_path(config.get_string("Perk", "CSVName"), "csv")
    spell_path = config.build_result_path(config.get_string("Spell", "CSVName"), "csv")
    CSV.build_table(mod_path, mods, delimiter)
    CSV.build_table(perk_path, perks, delimiter)
    CSV.build_table(spell_path, spells, delimiter)
    print("\nSuccess\n")
