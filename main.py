import logprop as lp

p = lp.Atom('p')

q = lp.Atom('q')

r = lp.Atom('r')


g = ((p >> r) & q) >> (r >> q)

#g = lp.Impl(lp.Disj(a, b), lp.Conj(lp.Neg(lp.Conj(a, b)), a))


print(f'{g}: {g.truth_val}')

print(f'len g: {len(g)}')

#f.truth_val = 3


