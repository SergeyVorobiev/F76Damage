from Code.Grabbers.UnitListener import UnitListener
from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class MSTTGrabber(UnitListener):

    def __init__(self, spell, expl, hazd, print=True):
        super().__init__(print)
        self.mstt = {}
        self.spell = spell
        self.expl = expl
        self.hazd = hazd
        self.number = 0
        self.label = 'MSTT'
        self.skip = [
            "FXSetGraphVariable",
            "WorkshopFloraDamageHelperScript",
            "FXDeleteSelfAfterTimer",
            "Default1StateSyncActivator",
            "E09C_WeddingNetScript",
            "Default2StateActivator",
            "Default1StateSyncActivator",
            "E09A_CrystalAnimHandler",
            "E09C_CollapsingRockPileScript",
            "DefaultPlaySoundOnActivate",
            "DefaultRefEffectShader",
            "p76_DLC01:DLC01_ClientTutorials",
            "VaultDefault2StateActivator",
            "p76_DLC01:DLC01_BabylonClientDataInitializer",
            "FXDeleteSelfAfterGameTimer",
            "ManagedKlaxonScript",
            "Default1StateActivator",
            "KlaxonScript",
            "WorkshopVertibirdGrenadeScript",
            "LC101RotationScript",
            "NewRiverGorgeBridgeDestructionScript",
            "VaultOxygenTankScript",
            "TestLocalDamageScript",
            "FusionGeneratorSCRIPT",
            "DefaultReleaseToHavokScript",
            "MacMechBioJar01",
            "HabitatSpawnController",
            "EN07_MissileSoundRefScript",
            "PlankHingeMoveableScript",
            "HeavyActorPushOnImpact",
            "CryoGrenadeFXScript",
            "HighTechBBQGrillScript",
        ]

    def listen(self, unit: bytes):
        idd = F76AInst.get_id(unit)
        if idd == '0010eaea':
            return
        name = F76AInst.get_name(unit)
        vmad = F76GroupParser.get_group_segment_or_def(unit, b'VMAD', only_existed=True)
        spell = ''
        expl = ''
        hazd = ''
        if vmad:
            vname = F76AInst.get_name(vmad, 10)
            if self.skip.__contains__(vname):
                return
            if vname == "HazardTriggerScript":
                spell, success = F76AInst.get_id_and_resolve(vmad, 52, self.spell)
                if not success:
                    print("Can't resolve HazardTriggerScript script, for: " + idd)
            elif vname == "MTNM01_BaitMineScript":
                expl, success = F76AInst.get_id_and_resolve(vmad, 131, self.expl)
                hazd, success = F76AInst.get_id_and_resolve(vmad, 218, self.hazd)
        result = {}
        self.mstt[idd] = result
        result["id"] = idd
        result["name"] = name
        result["spell"] = spell
        result["expl"] = expl
        result["hazd"] = hazd

        self.print_id(self.label, self.number, idd, name)
