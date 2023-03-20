import proplog as pl
import old
from datetime import datetime as dt
import sys

begin = dt.now()

p = pl.Atom('p', True)

q = pl.Atom('q', False)

r = pl.Atom('r')

s = pl.Atom('p', False, get_if_exists=True)


f1 = pl.WFF.from_string('(p >> q) | r')

print(f1)
print(pl.WFF._existing_wffs)
print()
del(s)

print(pl.WFF._existing_wffs)
print()
s1 = str(f1)
f1 = 'caca'

cualca = pl.Impl(r, p)
p = q = 'hola'

pepe = pl.Conj(r, r)
carlos = pl.Disj(r, r)
print(pl.WFF._existing_wffs)
print()







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