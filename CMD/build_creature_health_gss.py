import sys

sys.path.append("..")

from CMD.build_all_to_gss import get_spreadsheet_and_config, update_creature_health

if __name__ == '__main__':
    spreadsheet, config = get_spreadsheet_and_config()
    update_creature_health(spreadsheet, config)
