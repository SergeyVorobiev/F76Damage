import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(ROOT_DIR, "Resources")


def build_root_path(names):
    return build_path(ROOT_DIR, names)


def build_path(root, names):
    if type(names).__name__ == 'tuple' or type(names).__name__ == 'list':
        for r in names:
            root = os.path.join(root, str(r))
        return root
    else:
        return os.path.join(root, names)


def build_resources_path(names):
    return build_path(RESOURCES, names)


CURVE_TABLES = build_resources_path('CurveTables')
