import logprop as lp
import old

p = lp.Atom('p', True)

q = lp.Atom('q', False)

r = lp.Atom('r', True)

fs = [
    'p >> q',
    '~p >> q',
    '~(p) >> q',
    '(~p) >> q',
    '((~(p)) >> q)',
    '(p) >> ~q',
    '(p) >> ~(q)',
    '(p) >> ~(~q)',
    '((p) & (~q)) | (p >> ~(~s))',
    '(((p) & (~q)) | (p >> s))',
    '(~(p) >> q) & (q | s) & ((q) | s)',

    '(p) & ~(q) & (s)'
]

for f in fs:
    try:
        print(f'{f.rjust(40)}   ---->   {str(lp.WFF.from_string(f)).ljust(40)}')

    except:
        print(f'{f.rjust(40)}   ---->   {"Error".ljust(40)}')

#print(f"Viejo: {old.FBF('(!(p) -> q) & ((q | s) & ((q) | s))')}")