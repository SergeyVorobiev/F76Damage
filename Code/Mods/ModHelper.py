import struct

from Code.Helpers.ColorPrint import cprintln, pc
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class ModHelper:
    value_types = ['Int', 'Float', 'Bool', 'None', 'FormID,I', 'Enum', 'FormID,F']

    fun_types = ['Set', 'MullAdd', 'Add']

    prop_types = {0: "Speed",
                  2: "MinRange",
                  3: "MaxRange",
                  4: "AttackDelay",
                  6: "OutOfRangeDamageMult",
                  7: "SecondaryDamage",
                  8: "CriticalChargeBonus",
                  9: "HitBehaviour",
                  10: "Rank",
                  12: "AmmoCapacity",
                  22: "HasAlternateRumble",
                  25: "IsAutomatic",
                  27: "IsNonPlayable",
                  28: "AttackDamage",
                  29: "Value",
                  30: "Weight",
                  31: "Keywords",
                  32: "AimModel",
                  33: "MinConDegree",
                  34: "MaxConDegree",
                  35: "ConeIncrease",
                  41: "RecoilMaxDegree",
                  42: "RecoilMinDegree",
                  44: "RecoilShotsForRunaway",
                  45: "RecoilArcDeg",
                  46: "RecoilArcRotateDeg",
                  47: "ConIronSights",
                  48: "HasScope",
                  49: "ZoomFOVMult",
                  51: "NumProjectiles",
                  52: "AttackSound",
                  56: "IdleSound",
                  57: "EquipSound",
                  58: "UnEquipSound",
                  59: "SoundLevel",
                  60: "ImpactDataSet",
                  61: "Ammo",
                  62: "CritEffect",
                  63: "BashImpactDataSet",
                  65: "Enchantments",
                  66: "BaseStability",
                  67: "ZoomData",
                  70: "ZoomDataCameraOffsetX",
                  71: "ZoomDataCameraOffsetY",
                  72: "ZoomDataCameraOffsetZ",
                  73: "EquipSlot",
                  75: "NPCAmmoList",
                  76: "ReloadSpeed",
                  77: "DamageTypeValues",
                  78: "AccuracyBonus",
                  79: "APCost",
                  80: "OverrideProjectile",
                  83: "SightedTransition",
                  84: "FullPower",
                  85: "HoldInputToPower",
                  86: "HasRepeatableSingleFire",
                  87: "MinPower",
                  88: "ColorRemapingIndex",
                  89: "MaterialSwaps",
                  90: "CriticalDamageMult",
                  91: "FastEquipSound",
                  94: "ActorValues",
                  97: "Durability",
                  103: "ModelSwap",
                  106: "DamageBonusMult",
                  107: "AimAssist",
                  108: "WeightReduction"}

    @staticmethod
    def get_include_size_prop_size(unit):
        data = F76GroupParser.get_group_segment(unit, b'DATA')
        include_size = F76AInst.get_ushort(data, 2)
        prop_size = F76AInst.get_ushort(data, 6)
        return include_size, prop_size

    co = 0

    @staticmethod
    def get_weap_properties(unit: bytes, need_properties=None):
        ModHelper.co += 1
        name = F76AInst.get_name(unit)
        if name.startswith("Debug") or name.startswith("TestAudio"):
            return None, None, None
        full_name = F76AInst.get_full(unit)
        segment = F76GroupParser.get_group_segment(unit, b'WEAP')
        attach_id = F76AInst.get_id(segment, 2)
        length = len(segment)
        block_size = 24
        start_block = 10
        i_block_size = 7
        end = 0
        result = []
        includes = []
        include_size, prop_size = ModHelper.get_include_size_prop_size(unit)
        if include_size == 0 and prop_size == 0:
            # print("Does not have includes and properties")
            return None, full_name, attach_id

        parent_slots = struct.unpack('<I', segment[6: 10])[0]
        # print("Parrent slots:", parent_slots)

        # Try to find attach slots
        for ps in range(parent_slots):
            # val = struct.unpack('<I', segment[start_block: start_block + 4])[0]
            # print("Parent slot:", hex(val)[2:].zfill(8))
            start_block += 4

        start_block += 4
        for inc in range(include_size):
            start = start_block + i_block_size * inc
            includes.append(F76AInst.get_id(segment, start))
            end = start + i_block_size

        if end > 0:
            start_block = end
        result.append({'Includes': includes})
        for p in range(prop_size):
            start = start_block + block_size * p
            end = start + block_size
            if end > length:
                break
            seg2 = segment[start:end]
            v_type = ModHelper.value_types[struct.unpack('<I', seg2[:4])[0]]
            if v_type == "None":
                cprintln(f"VTYPE: {struct.unpack('<I', seg2[:4])[0]}", pc.red, is_bold=True)
            if v_type == "Int":
                fmt = '<IlliiL'
            elif v_type == "Bool":
                fmt = '<IlliiL'
            elif v_type == "FormID,I":
                fmt = '<IllLiL'
            elif v_type == "FormID,F":
                fmt = '<IllLfL'
            else:
                fmt = '<IllffL'

            v_type, f_type, prop, val1, val2, c_table = struct.unpack(fmt, seg2)
            if need_properties is not None and not need_properties.__contains__(prop):
                continue
            c_table = hex(c_table)[2:].zfill(8)
            v_type = ModHelper.value_types[v_type]
            if v_type == "FormID,I" or v_type == "FormID,F":
                val1 = hex(val1)[2:].zfill(8)
                val2 = round(val2, 3)
            elif v_type == "Float":
                val1 = round(val1, 3)
                val2 = round(val2, 3)
            p_name = ModHelper.prop_types.get(prop, '')
            if len(p_name) == 0:
                cprintln(f"{F76AInst.get_id(unit)} Can't get name for property {prop}", pc.red, is_bold=True)
                p_name = "prop" + str(prop)
            result.append({"ValType": v_type, "FunType": ModHelper.fun_types[f_type], "Prop": p_name, "Val1": val1,
                           "Val2": val2, "TabID": c_table})
        if len(includes) == 0 and len(result) == 1:
            return None, None, None
        return result, full_name, attach_id
