from Code.Helpers.ColorPrint import cprint, cprintln, pc

printed_objects = []

exclude = False


def is_exclude(name):
    if not exclude:
        return False
    return name.startswith("cr") or name.startswith("zzz") or name.startswith("DEPRECATED") or name.startswith("DEL") or \
        name.startswith("ATX") or name.startswith("ZZZ") or name.startswith("DLC") or name.startswith("XPD") or \
        name.startswith("DEl") or name.startswith("CAT") or name.startswith("Protest") or name.startswith(
            "Workshop") or name.startswith("Trap") or name.endswith("NONPLAYABLE") or name.startswith("GasTrap")


def cprint_f76_weapon(unit: bytes, result: {}):
    name = result['NAME']
    id = result['ID']
    if is_exclude(name):
        return
    printed_objects.append(result)
    cprint(id, pc.cyan, pc.white, True, end=" ")
    cprint(f'{name:<70}', pc.blue, pc.white, True, end=" ")
    cprintln(result, pc.red)


def print_f76_weapon(unit: bytes, result: {}):
    name = result['NAME']
    idd = result['ID']
    print("".ljust(100), end='\r')
    print(idd, name, end='\r')


def print_f76_weapon_melee(unit: bytes, result: {}):
    name = result['NAME']
    id = result['ID']
    if is_exclude(name):
        return
    if result['ANIM_FIRE'] is not None:
        return
    printed_objects.append(result)
    cprint(id, pc.cyan, pc.white, True, end=" ")
    cprint(f'{name:<70}', pc.blue, pc.white, True, end=" ")
    cprintln(result, pc.red)


def print_f76_weapon_range(unit: bytes, result: {}):
    name = result['NAME']
    id = result['ID']
    if is_exclude(name):
        return
    if result['ANIM_FIRE'] is None:
        return
    printed_objects.append(result)
    cprint(id, pc.cyan, pc.white, True, end=" ")
    cprint(f'{name:<70}', pc.blue, pc.white, True, end=" ")
    cprintln(result, pc.red)
