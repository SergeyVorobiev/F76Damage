import sys

sys.path.append("..")
from CMD.extract_ba2 import extract


if __name__ == '__main__':
    extract("LocalizationFileName", "ResultLocalizationFolder")