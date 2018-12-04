from pathlib import Path
from filecmp import cmp
from collections import defaultdict as d_dict


def search(p1):
    r_size = d_dict(list)
    for f in p1.iterdir():
        if f.is_file():
            f_size = f.stat().st_size
            r_size[f_size].append(f)
        elif f.is_dir():
            m = search(f)
            for x, y in m.items():
                r_size[x].extend(y)
        else:
            continue
    return r_size


def comparison(file_dct):
    eq_lst_tot = []
    size_lst = sorted(file_dct.keys())
    for sz in size_lst:
        eq_lst = []
        if len(file_dct[sz]) > 1:
            for f in file_dct[sz]:
                for eq in eq_lst:
                    if cmp(eq[0], f, shallow=False):
                        eq.append(f)
                        break
                else:
                    eq_lst.append([f])
        eq_lst_tot.extend(eq_lst)
    return eq_lst_tot


p1 = 'C:/Users/Future visioN/Desktop/nsu_py/dupl_exer/norm'
p_1 = Path(p1)

a = search(p_1)
b = comparison(a)

for x, y in sorted(a.items(), key=lambda p: p[0]):
    print(x, [s.name for s in y], '___', sep='\n')

print('******')

for x in b:
    print([s.name for s in x], '___', sep='\n')
