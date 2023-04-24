from unittest import TestCase as TC, main as run

import os
import sys

sys.path.append('/home/maurodonna/Documentos/Programación/Proyectos/proplog')

from module.proplog import *

class Test_WFF_instance_methods(TC):
    p = Atom('p')
    q = Atom('q')
    r = Atom('r')
    s = Atom('s')

    taut = WFF.from_string('p >> (~p >> q)')
    contr = WFF.from_string('p >> ~p')
    conting = WFF.from_string('p >> q')

    def test_get_truthfullness(self):
        self.assertEqual(self.taut.get_truthfullness(), 'tautology')
        self.assertEqual(self.contr.get_truthfullness(), 'contradiction')
        self.assertEqual(self.conting.get_truthfullness(), 'contingency')


if __name__ == '__main__':
    run()
