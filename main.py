import module.proplog as pl
import old
from datetime import datetime as dt
import sys

begin = dt.now()

p = pl.Atom('p', True)

q = pl.Atom('q', False)

r = pl.Atom('r')

s = pl.Atom('p1', None, get_if_exists=True)


f1 = pl.WFF.from_string('(((p) >> q) & (q | s)) & (((q) | s) >> rodo)')

f2 = pl.WFF.from_string('p & ~p')

f3 = pl.WFF.from_string('p >> (~p >> q)')

print(f3.get_truthfullness())




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