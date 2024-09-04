import subprocess
import sys

sys.path.append("..")

from CMD.Config import Config


def extract(file_path_key, result_folder_path_key):
    config = Config()
    path_to_archive = config.get_string("BA", "Archive2Path")
    path_to_file = config.get_string("BA", file_path_key)
    result_folder = config.get_string("BA", result_folder_path_key)
    cmd = f"{path_to_archive} {path_to_file} -extract={result_folder}"
    print("Starting to extract files")
    print(f"Path to archive {path_to_archive}")
    print(f"Path to file {path_to_file}")
    print(f"Path to destination folder {result_folder}")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        # print(proc.stdout.read())
        pass
    print("Done")


if __name__ == '__main__':
    extract("LocPath", "ResultFolder")