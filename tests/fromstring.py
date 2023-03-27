from unittest import TestCase as TC, main as run

import os
import sys

sys.path.append('/home/maurodonna/Documentos/Programación/Proyectos/proplog')

from module.proplog import *

class TestFromStringMethod(TC):
    p = Atom('p')
    q = Atom('q')
    r = Atom('r')
    s = Atom('s')

    def test_right_strings(self):
        cases = (
            ('p >> q', Impl(self.p, self.q)),
            ('~p >> q', Impl(Neg(self.p), self.q)),
            ('~(p) >> q', Impl(Neg(self.p), self.q)),
            ('(~p) >> q', Impl(Neg(self.p), self.q)),
            ('((~(p)) >> q)', Impl(Neg(self.p), self.q)),
            ('(p) >> ~q', Impl(self.p, Neg(self.q))),
            ('(p) >> ~(q)', Impl(self.p, Neg(self.q))),
            ('(p) >> ~(~q)', Impl(self.p, Neg(Neg(self.q)))),
            ('(p) >> ~~q', Impl(self.p, Neg(Neg(self.q)))),
            ('~~~((~~q)) & p', Conj(Neg(Neg(Neg(Neg(Neg(self.q))))), self.p)),
            ('~~~((~~q & p))', Neg(Neg(Neg(Conj(Neg(Neg(self.q)), self.p))))),
            ('((p) & (~q)) | (p >> ~(~s))', Disj(Conj(self.p, Neg(self.q)), Impl(self.p, Neg(Neg(self.s))))),
            # ('~~(~~(p) & ~(~q)) | (p >> ~(~s))', ),
            # ('((p) & (~q)) | ~~(~~p >> ~(~s))', ),
            # ('~~(~~(p) & ~(~q)) | ~~(~~p >> ~(~s))', ),
            # ('(((p) & (~q)) | (p >> s))', ),
            # ('((~(p) >> q) & (q | s)) & ((q) | s)',),
        )

        for str_case, case in cases:
            self.assertIs(WFF.from_string(str_case), case)


if __name__ == '__main__':
    run()
