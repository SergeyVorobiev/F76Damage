import configparser
import os

import Root


class Config:
    def __init__(self, config_name='config.ini'):
        config = configparser.ConfigParser()
        if not os.path.isfile(config_name):
            print(f"Can't find '{config_name}' file, be sure that it is placed inside 'CMD' folder")
            exit(-1)
        config.read(config_name)
        self.config = config

    def get_string(self, category, key, length=0, allow_empty=False):
        try:
            cat = self.config[category]
        except:
            print(f"Can't find category [{category}]")
            exit(-2)
        try:
            k = cat[key]
        except:
            print(f"Can't find key '{key}' in category [{category}]")
            exit(-3)
        if length != 0 and length != len(k):
            print(f"Length of key '{key}' in category [{category}] must be {length}")
            exit(-4)
        if len(k) == 0 and not allow_empty:
            print(f"Key '{key}' in category [{category}] can not be empty")
            exit(-5)
        return k

    def get_string_if_satisfy(self, category, key, names_list):
        string = self.get_string(category, key)
        if not names_list.__contains__(string):
            print(f"Key '{key}' in category [{category}] must satisfy the criteria {names_list}")
            exit(-6)
        return string

    def get_bool(self, category, key):
        r = self.get_string(category, key)
        if r == 'True' or r == 'False':
            return r == 'True'
        else:
            print(f"Please use True / False for key '{key}' in category [{category}]")
            exit(-7)

    def build_result_path(self, name, ext, root=""):
        name = name.split("\\")
        name[len(name) - 1] += ("." + ext)
        result_folder = self.get_string("RESULT_FOLDER", "Path").split("\\")
        result_folder += name
        return Root.build_path(root, result_folder)

    def build_resources_path(self, category, key):
        path = self.get_string(category, key).split("\\")
        return Root.build_path(Root.RESOURCES, path)