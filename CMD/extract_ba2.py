import os
import subprocess
import sys

sys.path.append("..")

from CMD.Config import Config


def extract(file_name_key, result_folder_path_key):
    config = Config()
    path_to_archive = config.get_string("BA", "Archive2Path")
    f76_folder = config.get_string("ESM", "F76Folder")
    path_to_file = f76_folder + os.sep + config.get_string("BA", file_name_key)
    result_folder = config.build_resources_path("BA", result_folder_path_key)
    cmd = f"\"{path_to_archive}\" \"{path_to_file}\" -extract=\"{result_folder}\""
    print("Starting to extract files")
    print(f"Path to archive {path_to_archive}")
    print(f"Path to file {path_to_file}")
    print(f"Path to destination folder {result_folder}")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        # print(proc.stdout.read())
        pass
    print("Done\n")


if __name__ == '__main__':
    extract("JSONGameFileName", "ResultFolder")