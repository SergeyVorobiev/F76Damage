import subprocess
import sys

sys.path.append("..")

from CMD.Config import Config

if __name__ == '__main__':
    config = Config()
    path_to_archive = config.get_string("BA", "Archive2Path")
    path_to_file = config.get_string("BA", "BAFilePath")
    result_folder = config.get_string("BA", "ResultFolder")
    cmd = f"{path_to_archive} {path_to_file} -extract={result_folder}"
    print("Starting to extract files")
    print(f"Path to archive {path_to_archive}")
    print(f"Path to file {path_to_file}")
    print(f"Path to destination folder {result_folder}")
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        # print(proc.stdout.read())
        pass
    print("Done")
