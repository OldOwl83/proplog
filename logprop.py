import re

class _SymVar:

    _existing_var_names = set()


    def __init__(self, name: str, truth_val: bool=None) -> None:
        self.name = name
        self.truth_val = truth_val


    def get_name(self):
        return self._name
    
    def set_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError('_SymVar.name must be of str type.')
        
        elif re.search('[ +*~^<>-]', value):
            raise ValueError('_SymVar.name should not contain '
                             'special characters.')
        
        elif value in _SymVar._existing_var_names - {self.name if hasattr(self, '_name') else None}:
            raise ValueError(f'A SymVar object with name {value} already exists.')
        
        else:
            self._name = value
            _SymVar._existing_var_names.add(value)

    def del_name(self):
        raise AttributeError('_SymVar.name can not be erased.')
    
    name = property(get_name, set_name, del_name)


    def get_truth_val(self):
        return self._truth_val
    
    def set_truth_val(self, value: bool):
        if not (isinstance(value, bool) or value is None):
            raise TypeError('_SymVar.truth_val must be of boolean or None types.')
        else:
            self._truth_val = value

    def del_truth_val(self):
        self._truth_val = None

    truth_val = property(get_truth_val, set_truth_val, del_truth_val)


    def __del__(self):
        if hasattr(self, '_name'):
            _SymVar._existing_var_names.remove(self.name)

        del(self)



class WFF: pass


class Atom(WFF):

    _existing_symvars: dict[str: _SymVar] = {}


    def __init__(self, name: str, truth_val: bool=None) -> None:
        self.name = name

        if truth_val is not None:
            self.truth_val = truth_val


    def get_name(self):
        return self._symvar.name
    
    def set_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Atom.name must be of str type.')
        
        elif re.search('[ +*~^<>-]', value):
            raise ValueError('Atom.name should not contain '
                             'special characters.')
        
        elif value in Atom._existing_symvars.keys():
            self._symvar = Atom._existing_symvars[value]
        
        else:
            self._symvar = _SymVar(value)
            Atom._existing_symvars.update({value: self._symvar})

    def del_name(self):
        raise AttributeError('Atom.name can not be erased.')

    name = property(get_name, set_name, del_name)


    def get_truth_val(self):
        return self._symvar.truth_val
    
    def set_truth_val(self, value: bool):
        if not (isinstance(value, bool) or value is None):
            raise TypeError('Atom.truth_val must be of boolean or None types.')
        else:
            self._symvar.truth_val = value

    def del_truth_val(self):
        del(self._symvar.truth_val)

    truth_val = property(get_truth_val, set_truth_val, del_truth_val)
    
    '''
    Evaluar la conveniencia de conservar las variables proposicionales en
    Atom._existing_symvars aun cuando no queden objetos Atom apuntando a ellas.
    '''
    # def __del__(self):
    #     Atom._existing_symvars.pop(self.name)

    #     del(self)


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
    
    def __len__(self): # La propiedad len podría ser un alias para la profundidad
        return 1

    def _Devolver_profundidad(self): #También la profundidad de F_ATOM se puede decir que es absoluta.
        return 1

    def _Tomar_valor(self):
        return self.value