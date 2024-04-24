import csv

from Code.Helpers.Common import get_chunks

IF = ("IF", "ЕСЛИ")
AND = ("AND", "И")
TRUE = ("TRUE", "ИСТИНА")
FALSE = ("FALSE", "ЛОЖЬ")
SUM = ("SUM", "СУММ")

en = 0
ru = 1

fl = ['en', 'ru']


def health_header(f, rows_size):
    return ['', '', '', f'={SUM[f]}(D2:D{rows_size + 1})']


def res_header(f, rows_size):
    return ['', '', '', f'={SUM[f]}(D2:D{rows_size})', f'={SUM[f]}(E2:E{rows_size})', f'={SUM[f]}(F2:F{rows_size})',
            f'={SUM[f]}(G2:G{rows_size})', f'={SUM[f]}(H2:H{rows_size})', f'={SUM[f]}(I2:I{rows_size})']


def build_names(path: str, dicts: {}, delimiter=','):
    with open(path, 'w', newline='') as csvfile:
        write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        names = list(dicts.keys())
        names.sort()
        for name in names:
            write.writerow([name])


def build_formula_csv(path: str, dicts: {}, f_header, max_level, res_names, f_delimiter, delimiter='#', chunks=1,
                      use_name_in_each_cell=True, f=en, dot_for_floats=True, sheet_name="CalcDamage", name_cell="$K$24",
                      level_cell="$L$24"):
    rows_size = len(dicts) * max_level
    ranges = get_chunks(chunks, rows_size)
    cell_number = 1
    rows = []
    for name in dicts.keys():
        creature_dict = dicts[name]
        for i in range(max_level):
            row = ['', name, i + 1]
            for j in range(len(res_names)):
                value = str(creature_dict[res_names[j]][i])

                # for google spreadsheets
                if not dot_for_floats:
                    value = value.replace(".", ",")
                row.append(value)
            rows.append(row)

    c = f_delimiter
    rows.sort(key=lambda x: x[1])
    cell_name_number = 0
    for row in rows:
        cell_number += 1
        if row[2] == 1:
            cell_name_number = cell_number
        else:
            if use_name_in_each_cell:
                cell_name_number = cell_number
            else:
                row[1] = ''  # remove name for performance in spreadsheets

        row[0] = (f"={IF[f]}({AND[f]}({sheet_name}!{name_cell}=B{cell_name_number}{c}"
                  f" {sheet_name}!{level_cell}=C{cell_number}){c} {TRUE[f]}{c} {FALSE[f]})")
        for i in range(3, len(row)):
            row[i] = f"={IF[f]}(A{cell_number}{c}{row[i]}{c}0)"
    first_row = True
    for ran in ranges:
        new_path = path[:-4]
        new_path += str(ran)
        new_path += '.csv'
        with open(new_path, 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
            if first_row:
                first_row = False
                write.writerow(f_header(f, rows_size))
            write.writerows(rows[ran[0]:ran[1]])
