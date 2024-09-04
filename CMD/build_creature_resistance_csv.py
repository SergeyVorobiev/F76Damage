import csv
import sys

sys.path.append("..")
from Code.Helpers.CSV import CSV
from Code.CurveTables.CreatureResistance import CreatureResistance
import Root
from CMD.Config import Config


def build_creature_resistance_table(config):
    path = config.get_string("JSON", "CreatureResistanceFilesPath").split("\\")
    need_sort = config.get_bool('Creature.Resistance', 'Sort')
    json_path = Root.build_path(Root.RESOURCES, path)
    creature_resistance = CreatureResistance(json_path)
    dicts = creature_resistance.build_dictionaries()
    return creature_resistance.build_table(dicts, need_sort)


if __name__ == '__main__':
    print("Starting to build creature's resistance")
    config = Config()
    name = config.get_string('Creature.Resistance', 'CSVName')
    result_path = config.build_result_path(name, "csv")
    delimiter = config.get_string("CSV", 'Delimiter', 1)
    table = build_creature_resistance_table(config)
    CSV.build_table(result_path, table, delimiter, quoting=csv.QUOTE_MINIMAL)
    print("Creature resistance - Success\n")
