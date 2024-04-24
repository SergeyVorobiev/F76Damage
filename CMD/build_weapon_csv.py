import sys

sys.path.append("..")
from CMD.Config import Config
from Code.Decoders.BaseDecoder import BaseDecoder
from Code.Decoders.Templates.F76DTemplates import F76DecTemplates
from Code.Helpers import Printing
from Code.Helpers.CSV import CSV
from Code.Units.UnitSeparator import UnitSeparator


def parse_weapon_data(config):
    m_sort = config.get_string("Weapon", "MeleeSort")
    r_sort = config.get_string("Weapon", "RangeSort")
    ignore_melee = [s.strip() for s in config.get_string("Weapon", "IgnoreMeleeIfNameStartsWith").split(",")]
    ignore_range = [s.strip() for s in config.get_string("Weapon", "IgnoreRangeIfNameStartsWith").split(",")]
    decoders = [BaseDecoder(F76DecTemplates.WEAPON).print_result(Printing.print_f76_weapon)]
    master = config.get_string("ESM", "F76Master")
    nw = config.get_string("ESM", "F76NW")
    UnitSeparator.separate_and_decode_file(master, decoders)
    UnitSeparator.separate_and_decode_file(nw, decoders)
    melee_table = CSV.build_melee_range_table(decoders[0].get_data(), True, m_sort, ignore_melee)
    range_table = CSV.build_melee_range_table(decoders[0].get_data(), False, r_sort, ignore_range)
    return decoders, melee_table, range_table


if __name__ == '__main__':
    config = Config()
    sort = config.get_string("Weapon", "Sort")
    path = config.build_result_path(config.get_string("Weapon", "CSVName"), "csv")
    m_path = config.build_result_path(config.get_string("Weapon", "CSVMelee"), "csv")
    r_path = config.build_result_path(config.get_string("Weapon", "CSVRange"), "csv")
    delimiter = config.get_string("CSV", "Delimiter", 1)
    decoders, melee_table, range_table = parse_weapon_data(config)
    decoders[0].to_csv(path, delimiter, sort)
    CSV.build_melee(m_path, melee_table, delimiter)
    CSV.build_range(r_path, range_table, delimiter)
