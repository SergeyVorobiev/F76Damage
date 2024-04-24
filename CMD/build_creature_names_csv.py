import sys

sys.path.append("..")
from Code.CurveTables.Helpers.GSSCSVCreatureParamsBuilder import build_names
import Root
from CMD.Config import Config
from Code.CurveTables.CreatureHealth import CreatureHealth

if __name__ == '__main__':
    config = Config()
    name = config.get_string('Creature.Names', 'CSVName')
    result_path = config.build_result_path(name, "csv")
    path = config.get_string("JSON", "CreatureHealthFilesPath").split("\\")
    json_path = Root.build_path(Root.RESOURCES, path)
    creature_health = CreatureHealth(json_path)
    dicts = creature_health.build_dictionaries()
    build_names(result_path, dicts)
    print("Creature names - Success")
