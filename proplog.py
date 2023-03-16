import re


class WFF: 
    ############################# PROPERTIES ##################################
    @property
    def truth_val(self):
        if self._l_wff.truth_val is None or (
            (hasattr(self, '_r_wff') and self._r_wff.truth_val is None)
        ):
            return None
        
        else:
            return 'defined'
    

    @truth_val.setter
    def truth_val(self, value: bool|None):
        raise AttributeError(f'{self.__class__.__name__}.truth_val can not be '
                             'assigned. It depends on its subformulas.')

    @truth_val.deleter
    def truth_val(self):
        raise AttributeError(f'{self.__class__.__name__}.truth_val can not be '
                             'erased.')


    ########################### SPECIAL METHODS ###############################
    def __init__(self, l_wff: 'WFF'):
        self._l_wff = l_wff 

    
    def __repr__(self):
        return (f'proplog.{self.__class__.__name__} object obtainable from '
                f'proplog.WFF.from_string("{str(self)}")')
    
    def __bool__(self):
        return bool(self.truth_val)
    

    def __len__(self):
        return len(self._l_wff) + (len(self._r_wff) if hasattr(self, '_r_wff') else 0) + 1
    

    def __getitem__(self, index: int):
        if not isinstance(index, int):
            raise TypeError('Index must be of int type.')
        
        elif index == 0: 
            return self._l_wff
        
        elif index == 1 and hasattr(self, '_r_wff'): 
            return self._r_wff
        
        else: 
            raise IndexError("Index out of range.")


    def __setitem__(self, index: int, other: 'WFF'):
        if not isinstance(index, int):
            raise TypeError('Index must be of int type.')
        
        elif not isinstance(other, WFF):
            raise TypeError('Subformula should be of WFF type.')
        
        elif index == 0: 
            self._l_wff = other
        
        elif index == 1 and hasattr(self, '_r_wff'): 
            self._r_wff = other
        
        else: 
            raise IndexError("Index out of range.")
        

    def __delitem__(self, index: int):
        raise AttributeError('A subformula can not be erased. You could want '
                             'to substract it.')
    

    def __sub__(self, other: 'WFF'):
        if not hasattr(self, '_r_wff'):
            raise ArithmeticError('It is only possible to make a subtraction '
                                  'of a bimembered formula')

        if other is self._l_wff: 
            return self._r_wff
        
        elif other is self._r_wff: 
            return self._l_wff
        
        else: 
            raise ArithmeticError("Only one of its subformulas can be "
                                  "substracted from a formula.")

        
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
    

    ########################## INSTANCE METHODS ##############################
    def get_symvars(self, symvars: set=set()):
        if isinstance(self, Atom):
            symvars.add(self)

        else:
            self._l_wff.get_symvars(symvars)

            if hasattr(self, '_r_wff'):
                self._r_wff.get_symvars(symvars)
        
        return symvars
    

    def get_depth(self):
        if isinstance(self, Atom):
            return 1
        else: 
            return max(
                self._l_wff.get_depth(),
                self._r_wff.get_depth() if hasattr(self, '_r_wff') else 0
            ) + 1
        

    ############################## STATIC METHODS #############################
    @staticmethod
    def from_string(wff_str: str):
        wff_str = wff_str.replace(' ', '')


        def break_down_parentheses(string: str):
            if re.fullmatch('~*\([A-Za-z()&|>~]+\)', string):            
                l_pars = r_pars = 0

                for index, char in enumerate(wff_str, 0):
                    if char == '(': 
                        l_pars += 1
                    elif char == ')':
                        r_pars += 1
        
                    if r_pars == l_pars and r_pars > 0:
                        l_wff = wff_str[:index + 1]
                        break

                l_pars = r_pars = 0

                for index, char in enumerate(wff_str[index + 1:], index + 1):
                    if char == '(': 
                        l_pars += 1
                    elif char == ')':
                        r_pars += 1
                    
                    if r_pars == l_pars and r_pars > 0:
                        if index + 1 == len(wff_str):
                            return l_wff
                        else:
                            break
            
            return '--NO MATCH--'


        # Pregunta si la fórmula es una variable proposicional aislada
        if match := (
            re.fullmatch("([A-Za-z]+)", wff_str) or
            re.fullmatch("\(([A-Za-z]+)\)", wff_str)
        ):
            return Atom(match.group(1), get_if_exists=True)

        # Examina fórmulas bimembres
        elif match := (
            re.fullmatch(
                "(~*\([A-Za-z()&|>~]+\))(&|>>|\|)(~*[A-Za-z]+)", 
                wff_str) or 
            re.fullmatch(
                "(~*[A-Za-z]+)(&|>>|\|)(~*\([A-Za-z()&|>~]+\))", 
                wff_str) or 
            re.fullmatch(
                "(~*[A-Za-z]+)(&|>>|\|)(~*[A-Za-z]+)", 
                wff_str) or
            re.fullmatch(
                "(" + re.escape(break_down_parentheses(wff_str)) + ")(&|>>|\|)(~*\([A-Za-z()&|>~]+\))", 
                wff_str)
        ):
            match match.group(2):
                case '>>':
                    connector = Impl
                case '&':
                    connector = Conj
                case '|':
                    connector = Disj

            return connector(
                WFF.from_string(
                    match.group(1)
                ), 
                WFF.from_string(
                    match.group(3)
                )
            ) 
        
        # Pregunta si la fórmula es una negación
        elif match := (
            re.fullmatch("~(~*[A-Za-z]+)", wff_str) or
            re.fullmatch("~(~*\([A-Za-z()&|>~]+\))", wff_str)
        ):
            return Neg(WFF.from_string(match.group(1)))   
    
        
        elif re.fullmatch("\([A-Za-z()&|>~]+\)", wff_str):
            return WFF.from_string(wff_str[1:-1])
        
        else:
            raise ValueError(f'"{wff_str}" is not a WFF string representation.')


class Impl(WFF):
    def __init__(self, l_wff: 'WFF', r_wff: 'WFF'):
        super().__init__(l_wff)

        self._r_wff = r_wff 
        
        
    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (
            not self._l_wff.truth_val or self._r_wff.truth_val)
    
    
    def __str__(self):
        return f"({str(self._l_wff)} >> {str(self._r_wff)})"
    

class Conj(WFF):
    def __init__(self, l_wff: 'WFF', r_wff: 'WFF'):
        super().__init__(l_wff)

        self._r_wff = r_wff 
        
        
    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (
            self._l_wff.truth_val and self._r_wff.truth_val)
    
    
    def __str__(self):
        return f"({str(self._l_wff)} & {str(self._r_wff)})"
    

class Disj(WFF):
    def __init__(self, l_wff: 'WFF', r_wff: 'WFF'):
        super().__init__(l_wff)

        self._r_wff = r_wff 
        

    @WFF.truth_val.getter
    def truth_val(self):
        return WFF.truth_val.fget(self) and (
            self._l_wff.truth_val or self._r_wff.truth_val)
    
    
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
        return WFF.truth_val.fget(self) and (not self._l_wff.truth_val)
    
    
    def __str__(self):
        return f"~{str(self._l_wff)}"


class Atom(WFF):

    _existing_symvars: dict[str, 'Atom'] = {}


    def __new__(
            cls,
            name: str, 
            truth_val: bool|None=None, 
            get_if_exists: bool=False
    ) -> 'Atom':
        if get_if_exists:
            return Atom._existing_symvars.pop(name, super().__new__(cls))
        else:
            return super().__new__(cls)
    

    def __init__(
            self, 
            name: str, 
            truth_val: bool|None=None, 
            get_if_exists: bool=False
    ) -> None:
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
        
        elif value in Atom._existing_symvars.keys():
            raise AttributeError(f'A Atom object with name {value} already '
                                 'exists. Assign it to create a new reference, '
                                 'or construct it with "get_if_exists" parameter.')
        
        else:
            self._name = value
            Atom._existing_symvars.update({value: self})

    @name.deleter
    def name(self):
        raise AttributeError('Atom.name can not be erased.')


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
            Atom._existing_symvars.pop(self.name)

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
