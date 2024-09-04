import subprocess
import sys

sys.path.append("..")

from CMD.build_creature_resistance_csv import build_creature_resistance_table
from CMD.build_weapon_csv import parse_weapon_data
from CMD.build_weapon_mods_csv import prepare_weapon_mods_table
from gspread.utils import ValueRenderOption, ValueInputOption

from Code.CurveTables.Helpers.GSSCSVCreatureParamsBuilder import SUM, fl, IF, AND, TRUE, FALSE, res_header
from CMD.Config import Config
from CMD.build_creature_health_csv import build_creature_health_table, build_creature_health
from Code.GSheet.SheetConnect import SheetConnect


def prepare_health_table(config):
    table = build_creature_health_table(config)
    rows_size = len(table)
    lang = config.get_string_if_satisfy("CSV_FORMULA", "FormulaLang", ['en', 'ru'])
    d_sheet_name = config.get_string("CSV_FORMULA", "SheetName")
    name_cell = config.get_string("CSV_FORMULA", "CreatureNameCell")
    level_cell = config.get_string("CSV_FORMULA", "CreatureLevelCell")
    f = fl.index(lang)
    header = ['', '', '', f'={SUM[f]}(D2:D{rows_size})', '']
    table[0] = header
    for i in range(1, len(table)):
        cell_num = i + 1
        row = table[i]
        val = round(row[2], 2)
        str_val = str(val).replace(".", ",")
        row.append(f"={IF[f]}(A{cell_num};{str_val};0)")
        row.append(val)
        row[2] = row[1]
        row[1] = row[0]
        row[0] = (f"={IF[f]}({AND[f]}({d_sheet_name}!{name_cell}=B{cell_num}; " +
                  f"{d_sheet_name}!{level_cell}=C{cell_num}); {TRUE[f]}; {FALSE[f]})")
    return table


def prepare_resistance_table(config):
    table = build_creature_resistance_table(config)
    rows_size = len(table)
    lang = config.get_string_if_satisfy("CSV_FORMULA", "FormulaLang", ['en', 'ru'])
    d_sheet_name = config.get_string("CSV_FORMULA", "SheetName")
    name_cell = config.get_string("CSV_FORMULA", "CreatureNameCell")
    level_cell = config.get_string("CSV_FORMULA", "CreatureLevelCell")
    f = fl.index(lang)
    table[0] = res_header(f, rows_size)

    for i in range(1, len(table)):
        cell_num = i + 1
        row = table[i]
        for j in range(2, row.__len__()):
            val = round(row[j], 2)
            str_val = str(val).replace(".", ",")
            row[j] = f"={IF[f]}(A{cell_num};{str_val};0)"
        row.insert(0, f"={IF[f]}({AND[f]}({d_sheet_name}!{name_cell}=B{cell_num}; " +
                   f"{d_sheet_name}!{level_cell}=C{cell_num}); {TRUE[f]}; {FALSE[f]})")
    return table


def prepare_sheet(spreadsheet, config, config_sheet_name):
    sheet_name = config.get_string("GSheet", config_sheet_name)
    print(f"Connected, send the data to '{sheet_name}'")
    error_message = f"'{sheet_name}' does not exist, trying to create new one"
    sheet = SheetConnect.get_or_create_sheet(sheet_name, spreadsheet, error_message)
    sheet.clear()
    return sheet


def update_creature_health(spreadsheet, config):
    print("Update creature health")
    creature_health_sheet = prepare_sheet(spreadsheet, config, "CreatureHealthSheet")
    table = prepare_health_table(config)
    creature_health_sheet.update(table, value_input_option=ValueInputOption.user_entered,
                                 response_value_render_option=ValueRenderOption.formula)
    print("Success\n")


def update_creature_resistance(spreadsheet, config):
    print("Update creature resistance")
    creature_resistance_sheet = prepare_sheet(spreadsheet, config, "CreatureResistanceSheet")
    table = prepare_resistance_table(config)
    creature_resistance_sheet.update(table, value_input_option=ValueInputOption.user_entered,
                                     response_value_render_option=ValueRenderOption.formula)
    print("Success\n")


def update_weapon_mods(spreadsheet, config):
    print("Update weapon mods")
    weapon_mods_sheet = prepare_sheet(spreadsheet, config, "WeaponModSheet")
    weapon_perks_sheet = prepare_sheet(spreadsheet, config, "PerkSheet")
    weapon_spells_sheet = prepare_sheet(spreadsheet, config, "SpellSheet")
    mods, perks, spells = prepare_weapon_mods_table(config)
    weapon_mods_sheet.update(mods)
    weapon_perks_sheet.update(perks)
    weapon_spells_sheet.update(spells)
    print("\nSuccess\n")


def update_creature_names(spreadsheet, config):
    print("Update creature_names")
    creature_names_sheet = prepare_sheet(spreadsheet, config, "CreatureNameSheet")
    creature_health = build_creature_health(config)
    dicts = creature_health.build_dictionaries()
    table = []
    names = list(dicts.keys())
    names.sort()
    for name in names:
        table.append([name])
    creature_names_sheet.update(table)
    print("Success\n")


def check_gspread():
    if 'gspread' not in sys.modules:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gspread'])


def get_spreadsheet_and_config():
    check_gspread()
    config = Config()
    spreadsheet_name = config.get_string("GSheet", "SpreadsheetName")
    print(f"Connect to Spreadsheet '{spreadsheet_name}'")
    return SheetConnect.get_spreadsheet(config, spreadsheet_name), config


def update_weapons(spreadsheet, config):
    print("Update weapons")
    weapon_sheet = prepare_sheet(spreadsheet, config, "WeaponSheet")
    r_weapon_sheet = prepare_sheet(spreadsheet, config, "RangeWeaponSheet")
    m_weapon_sheet = prepare_sheet(spreadsheet, config, "MeleeWeaponSheet")
    t_weapon_sheet = prepare_sheet(spreadsheet, config, "ThrownWeaponSheet")
    u_weapon_sheet = prepare_sheet(spreadsheet, config, "UnarmedWeaponSheet")
    table, range_table, melee_table, thrown_table, unarmed_table = parse_weapon_data(config)
    weapon_sheet.update(table)
    r_weapon_sheet.update(range_table)
    m_weapon_sheet.update(melee_table)
    t_weapon_sheet.update(thrown_table)
    u_weapon_sheet.update(unarmed_table)
    print("\nSuccess\n")


if __name__ == '__main__':
    spreadsheet, config = get_spreadsheet_and_config()
    update_creature_names(spreadsheet, config)
    update_creature_health(spreadsheet, config)
    update_creature_resistance(spreadsheet, config)
    update_weapons(spreadsheet, config)
    update_weapon_mods(spreadsheet, config)
