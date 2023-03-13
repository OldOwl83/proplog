import logprop as lp

p = lp.Atom('p', True)

q = lp.Atom('q', False)

r = lp.Atom('r', True)

# %%

f = ~(p & q >> r)


print(f.truth_val)


# %%
s = lp.Atom('p', True, get_if_exists=True)

g = ((q | (p >> r) & q)) >> (r >> s)

#g = lp.Impl(lp.Disj(a, b), lp.Conj(lp.Neg(lp.Conj(a, b)), a))


print(f'{g}: {g.truth_val}')

print(f'len g: {len(g)}')

print(g.get_depth())

# print(p, ': ', p.truth_val)
# print(q)
# print(r)
# print(p._existing_symvars)
# print(s, ': ', s.truth_val)


