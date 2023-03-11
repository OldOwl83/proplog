import logprop as lp

a = lp.Atom('x', False)

b = lp.Atom('y', True)

c = lp.Atom('x')

b.name = 'x'

#a.truth_val = True

print(a.name, ': ', a.truth_val)

print(b.name, ': ', b.truth_val)

print(c.name, ': ', c.truth_val)

print(lp.Atom._existing_symvars)
