from Code.Helpers.F76AInst import F76AInst
from Code.Helpers.F76GroupParser import F76GroupParser


class CategoryHelper:

    @staticmethod
    def get_KWDA(unit, kywd, idd=None):
        result = []
        try:
            ksiz = F76GroupParser.get_group_segment(unit, b'KSIZ')
            count = F76AInst.get_ushort(ksiz, 2)
            if count > 0:
                try:
                    kwda = F76GroupParser.get_group_segment(unit, b'KWDA')
                    start = 2
                    for index in range(count):
                        keyword = F76AInst.get_id(kwda, start)
                        keyword_name = kywd.get(keyword)
                        if keyword_name is None:
                            keyword_name = keyword
                        result.append(keyword_name)
                        start += 4
                except:
                    if idd is not None:
                        print("Can't get 'KWDA' for " + idd)
        except:
            ...
        return result

    @staticmethod
    def get_mag_effects(unit, idd, mgef, curv, avif, glob):
        effects = []

        #  EFID / EFIT
        efids = []
        efits = []
        efit_ranges = []
        efid_ranges = []
        try:
            efid_groups = F76GroupParser.find_groups(unit, b'EFID')
            efid_ranges = efid_groups[b'EFID']
            efids = F76GroupParser.get_group_segment(unit, b'EFID', -1, efid_groups)
            efit_groups = F76GroupParser.find_groups(unit, b'EFIT')
            efit_ranges = efit_groups[b'EFIT']
            efits = F76GroupParser.get_group_segment(unit, b'EFIT', -1, efit_groups)
        except:
            ...

        cvts = F76AInst.find_named_groups(unit, b'CVT0', [])
        if efids.__len__() != efits.__len__():
            print("Can't parse effects for: " + idd)
        else:
            for i in range(efids.__len__()):
                efid = efids[i]
                efit = efits[i]
                efit_range = efit_ranges[i]
                efid_range = efid_ranges[i]
                effect = {}
                effect['m_effect'] = mgef[F76AInst.get_id(efid, 2)]
                shift = 4 if efit.__len__() < 18 else 0
                effect['magnitude'] = F76AInst.get_float(efit, 6 - shift)
                effect['area'] = F76AInst.get_uint(efit, 10 - shift)
                effect['duration'] = F76AInst.get_uint(efit, 14 - shift)
                effect["actor"] = ''
                effect["glob_duration"] = ''
                effect["glob_magnitude"] = ''
                effect['d_curv'] = ''
                segment = F76GroupParser.get_segments_between(unit, b'EFID', b'CODV', starts_from=efid_range[0] - 4)[0]

                # Actor value
                maga = F76GroupParser.get_group_segment_or_def(segment, b'MAGA')
                if maga is not None:
                    effect["actor"], success = F76AInst.get_id_and_resolve(maga, 2, avif)

                # Glob duration
                durg = F76GroupParser.get_group_segment_or_def(segment, b'DURG')
                if durg is not None:
                    effect["glob_duration"] = glob[F76AInst.get_id(durg, 2)]

                # Glob magnitude
                magg = F76GroupParser.get_group_segment_or_def(segment, b'MAGG')
                if magg is not None:
                    effect["glob_magnitude"] = glob[F76AInst.get_id(magg, 2)]

                if cvts.__len__() > 0:
                    start_cvt_index = efit_range[0] + efit_range[1] + 4
                    for cvt in cvts:
                        if cvt[0] == start_cvt_index:
                            cvt_bytes = unit[cvt[0]: cvt[0] + cvt[1]]
                            effect['d_curv'], success = F76AInst.get_id_and_resolve(cvt_bytes, 2, curv)
                            break
                effects.append(effect)
        return effects
