import sys

sys.path.append("..")

from Code.CurveTables.CreatureResistance import CreatureResistance
from Code.CurveTables.Helpers.GSSCSVCreatureParamsBuilder import fl
import Root
from CMD.Config import Config

if __name__ == '__main__':
    config = Config()
    name = config.get_string('Creature.Resistance', 'CSVFName')
    result_path = config.build_result_path(name, "csv")
    lang = config.get_string_if_satisfy("CSV_FORMULA", "FormulaLang", ['en', 'ru'])
    is_dot = config.get_bool('CSV_FORMULA', 'UseDotForFloats')
    need_sort = config.get_bool('Creature.Resistance', 'Sort')
    delimiter = config.get_string("CSV_FORMULA", 'Delimiter', 1)
    f_delimiter = config.get_string("CSV_FORMULA", 'FormulaDelimiter', 1)
    path = config.get_string("JSON", "CreatureResistanceFilesPath").split("\\")
    sheet_name = config.get_string("CSV_FORMULA", "SheetName")
    name_cell = config.get_string("CSV_FORMULA", "CreatureNameCell")
    level_cell = config.get_string("CSV_FORMULA", "CreatureLevelCell")
    json_path = Root.build_path(Root.RESOURCES, path)

    creature_resistance = CreatureResistance(json_path, formula_delimiter=f_delimiter)
    dicts = creature_resistance.build_dictionaries()
    creature_resistance.build_csv_table_with_formulas(result_path, dicts,
                                                      delimiter=delimiter, chunks=1, use_name_in_each_cell=True,
                                                      f_language=fl.index(lang), dot_for_floats=is_dot,
                                                      sheet_name=sheet_name, name_cell=name_cell, level_cell=level_cell)
    print("Creature resistance formula - Success")
