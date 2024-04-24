import sys

sys.path.append("..")
from Code.Helpers.CSV import CSV
import Root
from CMD.Config import Config
from Code.CurveTables.CreatureHealth import CreatureHealth


def build_creature_health(config):
    path = config.get_string("JSON", "CreatureHealthFilesPath").split("\\")
    json_path = Root.build_path(Root.RESOURCES, path)
    return CreatureHealth(json_path)


def build_creature_health_table(config):
    need_sort = config.get_bool('Creature.Health', 'Sort')
    creature_health = build_creature_health(config)
    dicts = creature_health.build_dictionaries()
    return creature_health.build_table(dicts, need_sort)


if __name__ == '__main__':
    config = Config()
    result_path = config.build_result_path(config.get_string('Creature.Health', 'CSVName'), "csv")
    delimiter = config.get_string("CSV", 'Delimiter', 1)
    table = build_creature_health_table(config)
    CSV.build_table(result_path, table, delimiter)
    print("Creature health - Success")
