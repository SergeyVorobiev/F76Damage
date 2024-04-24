import sys

sys.path.append("..")

from CMD.build_all_to_gss import get_spreadsheet_and_config, update_creature_resistance

if __name__ == '__main__':
    spreadsheet, config = get_spreadsheet_and_config()
    update_creature_resistance(spreadsheet, config)
