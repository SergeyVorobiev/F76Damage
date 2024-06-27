import sys

sys.path.append("..")
from Code.Helpers.CSV import CSV
from CMD.Config import Config


if __name__ == '__main__':
    config = Config()
    health_file_path = config.build_result_path(config.get_string('Creature.Health', 'CSVName'), "csv")
    res_file_path = config.build_result_path(config.get_string('Creature.Resistance', 'CSVName'), "csv")
    res_health_file_path = config.build_result_path(config.get_string('Creature.ResistanceHealth', "CSVName"), "csv")
    delimiter = config.get_string("CSV", 'Delimiter', 1)
    health_map = CSV.read_creature_health_into_map(health_file_path, delimiter)
    CSV.merge_health_into_creature_res_file(res_file_path, res_health_file_path, health_map, delimiter)
    print("Creature res health combine - Success")
