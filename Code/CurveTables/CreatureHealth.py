import os

import Root
from Code.CurveTables.Helpers.GSSCSVCreatureParamsBuilder import build_formula_csv, health_header, en
from Code.CurveTables.LevelCurve import LevelCurve


class CreatureHealth(LevelCurve):

    def __init__(self, path, max_level=120, formula_delimiter=";"):
        super().__init__(path, ['health'], max_level, formula_delimiter)

    def _prepare_names(self):
        file_names = [f[7:-5] for f in os.listdir(self._path) if
                      (os.path.isfile(os.path.join(self._path, f)) and f.endswith('.json'))]
        return set(file_names)

    def _form_path(self, name, res_name):
        return Root.build_resources_path((self._path, res_name + "_" + name + ".json"))

    def _get_exceptions(self):
        return {"e09a_moleminer", "turretbubble", "attackdog"}

    def build_csv_table_with_formulas(self, path: str, dicts: {}, delimiter='#', chunks=1,
                                      use_name_in_each_cell=True, f_language=en, dot_for_floats=True,
                                      sheet_name="CalcDamage", name_cell="$K$24", level_cell="$L$24"):
        build_formula_csv(path, dicts, health_header, self._max_level, self._res_names,
                          self._formula_delimiter, delimiter, chunks, use_name_in_each_cell, f_language, dot_for_floats,
                          sheet_name, name_cell, level_cell)
