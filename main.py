import module.proplog as pl
import old
from datetime import datetime as dt
import sys

begin = dt.now()

p = pl.Atom('p1', True)

q = pl.Atom('q', False)

r = pl.Atom('r')

s = pl.Atom('p', False, get_if_exists=True)


f1 = pl.WFF.from_string('(((p) >> q) & (q | s)) & (((q) | s) >> rodo)')

f2 = pl.WFF.from_string('p & ~p')

# print(f1[0])
# print(f1[1])
# print(list(f1))
# print(f1.get_symvars())
# print(f1.get_subformulas())
# print(f1.get_truthfullness())

print(f1.print_truth_table())



# f1 = pl.WFF.from_string('((~(q) >> p) & (s | r)) & ((q) | s)')

# print(f1.get_meaning())

# for var in f1.get_symvars():
#     print(var)

fs = [
    'p >> q',
    '~p >> q',
    '~(p) >> q',
    '(~p) >> q',
    '((~(p)) >> q)',
    '(p) >> ~q',
    '(p) >> ~(q)',
    '(p) >> ~(~q)',
    '(p) >> ~~q',
    '~~~((~~q)) & p',
    '~~~((~~q & q))',
    '((p) & (~q)) | (p >> ~(~s))',
    '~~(~~(p) & ~(~q)) | (p >> ~(~s))',
    '((p) & (~q)) | ~~(~~p >> ~(~s))',
    '~~(~~(p) & ~(~q)) | ~~(~~p >> ~(~s))',
    '(((p) & (~q)) | (p >> s))',
    '((~(p) >> q) & (q | s)) & ((q) | s)',

    '(~(p) >> q) & (q | s) & ((q) | s)',
    '(p) & ~(q) & (s)',
    '(p) & (~q) | p >> ~(~s)',
    'p | q | r',
    'p & q & (r >> q)',
    'p & (q & (r >> q)',
    '(p & ~q) | p >> ~(~s)',

]

# for f in fs:
#     try:
#         print(f'{f.rjust(40)}   ---->   {str(pl.WFF.from_string(f)).ljust(40)}')

#     except:
#         print(f'{f.rjust(40)}   ---->   {"Error".ljust(40)}')


end = dt.now()

print(f'Tiempo de ejecución: {end - begin}')