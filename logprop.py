import re


class WFF: 
    def __init__(self, l_wff: 'WFF'):
        self.l_wff = l_wff 
        

    @property        
    def l_wff(self):
        return self._l_wff
    
    @l_wff.setter
    def l_wff(self, value: 'WFF'):
        if not isinstance(value, WFF):
            raise TypeError(f'{self.__class__}.l_wff must be of WFF type.')
        
        else:
            self._l_wff = value

    @l_wff.deleter
    def l_wff(self):
        raise AttributeError(f'{self.__class__}.l_wff can not be erased.')
    

    @property
    def r_wff(self):
        return self._r_wff
    
    @r_wff.setter
    def r_wff(self, value: 'WFF'):
        if not isinstance(value, WFF):
            raise TypeError(f'{self.__class__}.r_wff must be of WFF type.')
        
        else:
            self._r_wff = value

    @r_wff.deleter
    def r_wff(self):
        raise AttributeError(f'{self.__class__}.r_wff can not be erased.')
    

    @property
    def truth_val(self):
        if self.l_wff.truth_val is None or (
            (hasattr(self, 'r_wff') and self.r_wff.truth_val is None)
        ):
            return None
        
        else:
            return 'defined'
    

    @truth_val.setter
    def truth_val(self, value: bool|None):
        raise AttributeError(f'{self.__class__.__name__}.truth_val can not be assigned. '
                             'It depends on its subformulas.')

    @truth_val.deleter
    def truth_val(self):
        raise AttributeError(f'{self.__class__}.truth_val can not be erased.')

    
    def __bool__(self):
        return bool(self.truth_val)
    

    def __len__(self):
        return len(self.l_wff) + (len(self.r_wff) if hasattr(self, 'r_wff') else 0) + 1
    

    def __getitem__(self, index: int):
        if not isinstance(index, int):
            raise TypeError('Index must be of int type.')
        
        elif index == 0: 
            return self.l_wff
        
        elif index == 1 and hasattr(self, 'r_wff'): 
            return self.r_wff
        
        else: 
            raise IndexError("Index out of range.")


    def __setitem__(self, index: int, other: 'WFF'):
        if not isinstance(index, int):
            raise TypeError('Index must be of int type.')
        
        elif not isinstance(other, WFF):
            raise TypeError('Subformula should be of WFF type.')
        
        elif index == 0: 
            self.l_wff = other
        
        elif index == 1 and hasattr(self, 'r_wff'): 
            self.r_wff = other
        
        else: 
            raise IndexError("Index out of range.")
        

    def __rshift__(self, other: 'WFF'):
        if not isinstance(other, WFF):
            raise TypeError('Implication consequent should be of WFF type.')
        
        else:
            return Impl(self, other)
        

    def __and__(self, other: 'WFF'):
        if not isinstance(other, WFF):
            raise TypeError('Conjunction member should be of WFF type.')
        
        else:
            return Conj(self, other)
        

    def __or__(self, other: 'WFF'):
        if not isinstance(other, WFF):
            raise TypeError('Disjunction member should be of WFF type.')
        
        else:
            return Disj(self, other)
        
    
    def __invert__(self):
        return Neg(self)
    

class Impl(WFF):
    def __init__(self, l_wff: 'WFF', r_wff: 'WFF'):
        super().__init__(l_wff)

        self.r_wff = r_wff 
        
        
    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (
            not self.l_wff.truth_val or self.r_wff.truth_val)
    
    
    def __str__(self):
        return f"({str(self._l_wff)} >> {str(self._r_wff)})"
    

class Conj(WFF):
    def __init__(self, l_wff: 'WFF', r_wff: 'WFF'):
        super().__init__(l_wff)

        self.r_wff = r_wff 
        
        
    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (
            self.l_wff.truth_val and self.r_wff.truth_val)
    
    
    def __str__(self):
        return f"({str(self._l_wff)} & {str(self._r_wff)})"
    

class Disj(WFF):
    def __init__(self, l_wff: 'WFF', r_wff: 'WFF'):
        super().__init__(l_wff)

        self.r_wff = r_wff 
        

    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (
            self.l_wff.truth_val or self.r_wff.truth_val)
    
    
    def __str__(self):
        return f"({str(self._l_wff)} | {str(self._r_wff)})"
    

class Neg(WFF):
    @property
    def r_wff(self):
        raise AttributeError('Single-membered formulas has not r_wff attribute.')
    
    @r_wff.setter
    def r_wff(self, value):
        raise AttributeError('Single-membered formulas has not r_wff attribute.')


    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (not self.l_wff.truth_val)
    
    
    def __str__(self):
        return f"~{str(self._l_wff)}"


class Atom(WFF):

    _existing_symvars: list[str] = []


    def __init__(self, name: str, truth_val: bool|None=None) -> None:
        self.name = name
        self.truth_val = truth_val


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Atom.name must be of str type.')
        
        elif re.search('[ +*~^<>-]', value):
            raise ValueError('Atom.name should not contain special characters.')
        
        elif value in Atom._existing_symvars:
            raise AttributeError(f'A Atom object with name {value} already '
                                 'exists. Assign it to create a new reference.')
        
        else:
            self._name = value
            Atom._existing_symvars.append(value)

    @name.deleter
    def name(self):
        raise AttributeError('Atom.name can not be erased.')


    @property
    def r_wff(self):
        raise AttributeError('Single-membered formulas has not r_wff attribute.')
    
    @r_wff.setter
    def r_wff(self, value):
        raise AttributeError('Single-membered formulas has not r_wff attribute.')


    @property
    def truth_val(self):
        return self._truth_val
    
    @truth_val.setter
    def truth_val(self, value: bool|None):
        if not (isinstance(value, bool) or value is None):
            raise TypeError('Atom.truth_val must be of boolean or None types.')
        
        else:
            self._truth_val = value

    @truth_val.deleter
    def truth_val(self):
        self._truth_val = None


    def __del__(self):
        if hasattr(self, '_name'):
            Atom._existing_symvars.remove(self.name)

        del(self)


    def __str__(self):
        return self.name

    #def Imprimir_arbol(self):
    #    print(self, end=" | ")

    def __sub__(self, other):
        raise ArithmeticError("The substraction is not defined for "
                              "single-membered formulas")

    def __getitem__(self, index):
        raise IndexError("The index do not make sense for "
                         "single-membered formulas")

    def __setitem__(self, index, subf):
        raise IndexError("The index do not make sense for "
                         "single-membered formulas")
    
    def __len__(self): 
        return 1

    def _Devolver_profundidad(self): #También la profundidad de F_ATOM se puede decir que es absoluta.
        return 1

    def _Tomar_valor(self):
        return self.value