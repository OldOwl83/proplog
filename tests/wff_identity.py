from unittest import TestCase as TC, main as run

import os
import sys

sys.path.append('/home/maurodonna/Documentos/Programación/Proyectos/proplog')

from module.proplog import *

class Test_WFF_identity(TC):

    def test_existing_wff(self):
        f1 = Atom('p')

        with self.assertRaises(AttributeError) as cm:
            Atom('p')
        
        self.assertEqual(
            str(cm.exception),
            f'A Atom object with name {f1.name} already exists. Assign it to '
            'create a new reference, or construct it with "get_if_exists" parameter.'
        )

        with self.assertRaises(ValueError) as cm:
            Atom('p', True, get_if_exists=True)
        
        self.assertEqual(
            str(cm.exception),
            'Truth value cannot be set if you get an existing Atom.'
        )
            

    def test_existing_wffs_dict(self):

        f1 = WFF.from_string('(p >> ~q) >> ((r & s) | ~t)')
        length = len(f1)
        self.assertEqual(length, len(WFF._existing_wffs))

        f2 = WFF.from_string('(p >> q) | (p >> q)')
        length += 2
        self.assertEqual(length, len(WFF._existing_wffs))

        f1 = f1 - f1[1]
        length -= 7
        self.assertEqual(length, len(WFF._existing_wffs))

        f3 = Atom('p', get_if_exists=True)
        f4 = Atom('q', get_if_exists=True)
        f5 = Neg(f4)
        f6 = Impl(f3, f5)
        self.assertEqual(length, len(WFF._existing_wffs))

        f7 = Atom('new_wff')
        length += 1
        self.assertEqual(length, len(WFF._existing_wffs))

        del(f5)
        del(f7)
        length -= 1
        self.assertEqual(length, len(WFF._existing_wffs))

    def test_identity(self):

        f1 = WFF.from_string('(p >> ~q) >> ((r & s) | ~t)')
        f2 = WFF.from_string('(r & s)')
        self.assertEqual(len(f1), len(WFF._existing_wffs))

        self.assertEqual(f2, f1[1][0])
        self.assertIs(f2, f1[1][0])


if __name__ == '__main__':
    run()
