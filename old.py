'''
    Este módulo construye objetos del tipo 'Formula', que representan una fórmula
de la Lógica Proposicional, pero siempre instanciados en alguna de sus subclases
de acuerdo con su conectiva principal (F_CONJ, F_DISY, F_COND, F_NEG, F_DUP o F_ATOM).
A su vez, cada uno de estos objetos puede estar compuesto por otros objetos de su
misma clase base, que representan sus subfórmulas (los que a su vez pueden estar
compuestos por otros objetos, conformando un árbol de objetos 'Formula'). Esta
ramificación concluye con las fórmulas atómicas o variables proposicionales
('F_ATOM(Formula)') cuyas únicas propiedades son un string que la identifica y
un valor booleano que funciona como referencia para determinar el valor de las
fórmulas compuestas (objetos 'F_ATOM' con un mismo nombre siempre tienen el mismo
valor booleano).
    Estos objetos, por su parte, disponen de un método para calcular e imprimir
por pantalla su tabla de verdad correspondiente.

Interfaz pública:

Constructor:
        'FBF(string fbf)', donde fbf expresa una fórmula
        bien formada de la Lógica Proposicional en texto plano.

Métodos:
        'FBF.Generar_tabla('), calcula e imprime por pantalla la tabla de verdad
        correspondiente.

Operadores:
        "*", devuelve la conjunción de dos objetos "Formula", o de un objeto "Formula"
        con un string que expresa una fórmula bien formada.
        "+", devuelve la disyunción de dos objetos "Formula", o de un objeto "Formula"
        con un string que expresa una fórmula bien formada.
        "-", devuelve una fórmula resultante de eliminar el operando derecho del
        izquierdo (el operando derecho sólo puede ser una subfórmula del izquierdo).
        "[0/1]", el índice 0 refiere a la primera subfórmula de la fórmula indexada,
        mientras que el índice 1 refiere a la segunda subfórmula, si la hubiere.
        Mediante estos índices puede accederse a las subfórmulas tanto para leerlas
        como para reemplazarlas, ya sea por otra fórmula, o por un string que exprese
        una fórmula bien formada.

Sintaxis para los string que expresan las fórmulas:

Operadores:
            Conjunción: &
            Disyunción: |
            Implicación: ->
            Negación: !

    No hay un orden de precedencia entre los operadores, de modo que se debe gestionar
    toda la sintaxis de las fórmulas con el uso de paréntesis "()".
'''

#Librerías utilizadas
from re import fullmatch, match, sub as subst
from pandas import DataFrame
from pandas import options

#Configuración para la salida de las tablas de verdad (librería pandas)
options.display.max_rows = 128
options.display.max_columns = 40
options.display.width = 120

'''
Clase instanciadora: aunque técnicamente no es la clase base de los objetos que
representan las fórmulas proposicionales, en la práctica funciona como tal,
ya que es la que debe ser llamada por el cliente para generar tal tipo de
objetos. Como parámetro recibe un string en que se expresa una fórmula bien
formada, lo analiza, lo valida si es correcto, y decide a qué subclase de
'Formula' pertenece, según su conectiva principal. Por tanto, si bien esta
clase no construye los objetos 'Formula', funciona como una suerte de
distribuidora que determina cuál es el constructor correcto para cada caso
particular (tanto para la fórmula principal como para sus subfórmulas)
'''

class FBF:
    def __new__(cls, form_str):  # La instanciación del objeto devuelve un objeto de tipo diferente ('Formula')
        # Descompone el string en sus elementos componentes (conectiva principal y fórmulas miembro)
        elems_form = cls._Descomponer_string(form_str)

        if(elems_form != -1):  # Valida si la fórmula es correcta y determina su tipo, pasando sus elementos componentes como argumentos al constructor correspondiente
            match elems_form[1]:
                case '&': return F_CONJ(elems_form[0], elems_form[2])
                case '|': return F_DISY(elems_form[0], elems_form[2])
                case '->': return F_COND(elems_form[0], elems_form[2])
                case '!': return F_NEG(elems_form[0])
                case '0': return F_DUP(elems_form[0])
                case 'at': return F_ATOM(elems_form[0])
        else: raise Exception("Fórmula inválida") # Si la fórmula no es validada, levanta una excepción

# Método de descomposición del string en que se expresa la fórmula
    def _Descomponer_string(form_str):

        subforms = ["", "", ""] # Almacena los elementos componentes de la fórmula expresada en el string (subfórmula izq, conectiva/tipo, [subfórmula der])

        form_str = form_str.replace(' ', '') # Limpia los espacios en blanco

# Función para validar los elementos definidos por paréntesis exteriores. Esta función complementa el análisis hecho con las expresiones regulares, ya que las mismas no pueden controlar la paridad entre paréntesis izquierdos y derechos dentro de un elemento interno de la fórmula. Devuelve el elemento sin los paréntesis externos, o -1 si no es validado
        def _Tomar_parentesis(string):
            p_izq = 0  # Contadores de paréntesis izquierdos y derechos
            p_der = 0
            pos = 0 # Contador de ciclos

            if string[0] != '(' and string[-1] != ')': return -1

            for char in string:
                pos += 1
                if char == '(': p_izq += 1
                elif char == ')':
                    p_der += 1
                # Cuando los paréntesis derechos son tantos como los izquierdos (pero más que cero), y coinciden con los extremos del elemento, se completó la validación
                    if p_der == p_izq and p_der > 0:
                        if pos == len(string): return string[1:-1]  # Devuelve el elemento sin paréntesis exteriores
                        else: return -1 #Si el elemento es más largo, no está bien formado.

            return -1

#(Continúa "_Descomponer_string()")
        #Busca determinar la estructura general de la fórmula, con expresiones regulares

        #Pregunta si la fórmula es una variable proposicional aislada
        if fullmatch("[A-Za-z]+", form_str):
            subforms[0] = form_str
            subforms[1] = 'at'

        #Pregunta si la fórmula es una negación
        elif fullmatch("![A-Za-z]+", form_str) or (fullmatch("!\([A-Za-z()&|\->!]+\)", form_str) and _Tomar_parentesis(form_str[1:]) != -1 and len(_Tomar_parentesis(form_str[1:])) + 3 == len(form_str)):
            if form_str[1] == '(': subforms[0] = form_str[2:-1]
            else: subforms[0] = form_str[1:]
            subforms[1] = '!'

        #Pregunta si la fórmula está compuesta por dos subfórmulas coordinadas por una conectiva central
        else:
            fr_patt = fullmatch("^(!{0,1}\([A-Za-z()&|\->!]+\))(&|->|\|)(!{0,1}\([A-Za-z()&|\->!]+\))$", form_str) or fullmatch("^(!{0,1}\([A-Za-z()&|\->!]+\))(&|->|\|)(!{0,1}[A-Za-z]+)$", form_str) or fullmatch("^(!{0,1}[A-Za-z]+)(&|->|\|)(!{0,1}\([A-Za-z()&|\->!]+\))$", form_str) or fullmatch("^(!{0,1}[A-Za-z]+)(&|->|\|)(!{0,1}[A-Za-z]+)$", form_str)
            #Registra los tres elementos en la lista 'subforms', validando los elementos que están encerrados entre paréntesis (los demás ya son controlados por las expresiones regulares)
            if fr_patt:
                if fr_patt.group(1)[0] == '(':
                    subforms[0] = _Tomar_parentesis(fr_patt.group(1))
                    if subforms[0] == -1: return -1
                else:
                    subforms[0] = fr_patt.group(1)

                if fr_patt.group(3)[0] == '(':
                    subforms[2] = _Tomar_parentesis(fr_patt.group(3))
                    if subforms[2] == -1: return -1
                else:
                    subforms[2] = fr_patt.group(3)

                subforms[1] = fr_patt.group(2)

            #Pregunta si la fórmula es una duplicación con paréntesis externos redundantes
            elif fullmatch("\([A-Za-z()&|\->!]+\)", form_str):
                subforms[0] = form_str[1:-1]
                subforms[1] = '0'
            else: return -1

        return subforms

'''
La superclase que engloba a la fórmula principal y sus subfórmulas. Todas ellas serán, en realidad, instancias de las subclases especiales (F_CONJ, F_DISY, etc.). Sin embargo, en esta clase se definen los métodos comunes, incluyendo su constructor.
'''
class Formula:

    def __init__(self, subf1, subf2=None):
        self._subform1 = FBF(subf1) #Todas las subfórmulas están compuestas por al menos otra subfórmula, salvo las atómicas (F_ATOM), que tienen un constructor especial
        if subf2:
            self._subform2 = FBF(subf2)
        else:
            self._subform2 = None

    def __str__(self): pass #El casting a string se define de manera particular en las subclases

    def __repr__(self):
        return "FBF('{}')".format(str(self)) #Devuelve la expresión con la que el cliente puede construir una copia del objeto.

#Acceso a las subfórmulas mediante índices 0 y 1
    def __getitem__(self, index):
        if index == 0: return self._subform1
        elif index == 1 and self._subform2: return self._subform2
        else: raise IndexError("Índice fuera del rango de subfórmulas.")

#Reemplazo de las subfórmulas mediante índices
    def __setitem__(self, index, other):
        if "Formula" in str(type(other).__bases__): #Reemplazo por otro objeto "Formula"
            if index == 0: self._subform1 = other
            elif index == 1 and self._subform2: self._subform2 = other
            else: raise IndexError("Índice fuera del rango de subfórmulas.")

        elif type(other) == str: #Reemplazo por un string
            if index == 0: self._subform1 = FBF(other)
            elif index == 1 and self._subform2: self._subform2 = FBF(other)
            else: raise IndexError("Índice fuera del rango de subfórmulas.")

        else: raise TypeError("La subfórmulas sólo pueden ser otras fórmulas o strings que representen fórmulas.")

#Conjunción de fórmulas mediante el operador "*"
    def __mul__(self, other):
        if "Formula" in str(type(other).__bases__): return F_CONJ(subst("^\(.+\)$", str(self)[1:-1], str(self)), subst("^\(.+\)$", str(other)[1:-1], str(other))) #Conjunción con un objeto "Formula"

        elif type(other) == str: return F_CONJ(subst("^\(.+\)$", str(self)[1:-1], str(self)), other) #Conjunción con un string

        else: raise TypeError("La fórmulas sólo pueden ser conjuntadas con otras fórmulas o con strings que representen fórmulas.")

#Conmutatividad del operador "*" con un string
    def __rmul__(self, other):
        if type(other) == str: return F_CONJ(other, subst("^\(.+\)$", str(self)[1:-1], str(self)))
        else: raise TypeError("La fórmulas sólo pueden ser conjuntadas con otras fórmulas o con strings que representen fórmulas.")

#Disyunción de fórmulas mediante el operador "+"
    def __add__(self, other):
        if "Formula" in str(type(other).__bases__): return F_DISY(subst("^\(.+\)$", str(self)[1:-1], str(self)), subst("^\(.+\)$", str(other)[1:-1], str(other))) #Disyunción con un objeto "Formula"

        elif type(other) == str: return F_DISY(subst("^\(.+\)$", str(self)[1:-1], str(self)), other) #Disyunción con un string

        else: raise TypeError("La fórmulas sólo pueden ser conjuntadas con otras fórmulas o con strings que representen fórmulas.")

#Conmutatividad del operador "+" con un string
    def __radd__(self, other):
        if type(other) == str: return F_DISY(other, subst("^\(.+\)$", str(self)[1:-1], str(self)))
        else: raise TypeError("La fórmulas sólo pueden ser conjuntadas con otras fórmulas o con strings que representen fórmulas.")

#Eliminación de una subfórmula mediante el operador "-"
    def __sub__ (self, other):
        if other is self._subform1: return self._subform2
        elif other is self._subform2: return self._subform1
        else: raise ArithmeticError("A una fórmula sólo se le puede restar una de sus subfórmulas.")

#Método que devuelve para cada subfórmula su nivel de profundidad en relación a la fórmula que lo llamó
    def _Devolver_profundidad(self):
        if self._subform2: #La profundidad de toda subfórmula puede calcularse como la mayor profundidad alcanzada por sus subfórmulas, más uno (teniendo en cuenta que siempre las subfórmulas atómicas están en el primer nivel)
            prof_acum = max(self._subform1._Devolver_profundidad(),
                            self._subform2._Devolver_profundidad())
        else:
            prof_acum = self._subform1._Devolver_profundidad()
        return prof_acum + 1

#Método recursivo que devuelve el valor de verdad de cada subfórmula, dependiendo del valor asignado a las variables proposicionales. Tiene una definición especial en cada subclase.
    def _Tomar_valor(self): pass

#Función recursiva que recorre el árbol de subfórmulas hasta alcanzar las variables proposicionales que coinciden con el string "var", para poder asignarles el mismo valor de verdad "val".
    def _Asignar_valores(self, var, val):
        if type(self) == F_ATOM:
            if self._subform1 == var:
                self._valor = val
        else:
            self._subform1._Asignar_valores(var, val)
            if self._subform2:
                self._subform2._Asignar_valores(var, val)

#Método que devuelve la sucesión de todas las subfórmulas que componen la fórmula que lo llamó. Aun está sin uso... para futuras aplicaciones.
    # def Imprimir_arbol(self):
    #     self._subform1.Imprimir_arbol()
    #     if self._subform2:
    #         self._subform2.Imprimir_arbol()
    #     print(self, end=" | ")

#Método que construye la tabla de verdad completa de la fórmula que lo llamó (incluyendo los valores de sus subfórmulas), y la imprime por pantalla.
    def Generar_tabla(self):
        val_forms = dict() #Almacena para el string que representa cada subfórmula (keys) su nivel de profundidad y los valores de verdad que le corresponden en cada fila de la tabla.

    #Función interna que registra el nombre (string) de todas las subfórmulas como "keys" del diccionario 'val_forms', y le asocia su respectivo nivel de profundidad, y una lista vacía que se irá completando con los valores de verdad que le corresponden en cada fila de la tabla.
        def __Registro_formulas(self):
            nonlocal val_forms

            val_forms.update(
                {str(self): [self._Devolver_profundidad(), list()]})

            if type(self) != F_ATOM:
                __Registro_formulas(self._subform1)
                if self._subform2:
                    __Registro_formulas(self._subform2)

    #Función recursiva interna que recorre el árbol de subfórmulas para tomar su valor de acuerdo al valor establecido en las variables proposicionales, y lo almacena en las listas de valores correspondiente a cada una de ellas en el diccionario "val_forms".
        def __Registrar_valores_fila(self, list_rep):
            for forms in val_forms.keys():
                if str(self) == forms and not forms in list_rep:
                    val_forms[forms][1].append(self._Tomar_valor()) #Almacena el valor correspondiente a la subfórmula particular.
                    list_rep.add(forms) # Set para controlar que los valores de verdad no se dupliquen cuando hay dos subfórmulas iguales.

                    break
            # Y llama al resto del árbol
            if type(self) != F_ATOM:
                __Registrar_valores_fila(self._subform1, list_rep)
                if self._subform2:
                    __Registrar_valores_fila(self._subform2, list_rep)

#(continúa '.Generar_tabla()')
        __Registro_formulas(self) # Registro del árbol de subfórmulas en el diccionario "val_forms".

        var_logs = [val for val in val_forms.keys() if val_forms[val][0] == 1] # Almacena las variables proposicionales, que reconoce por su nivel de profundidad.

        for fila in range(2**len(var_logs)): # Calcula las filas de la tabla de verdad según la cantidad de variables proposicionales
            divisor = 2 # Modifica el período con que variará el valor de verdad de las variables proposicionales en las filas de la tabla.
            for var in var_logs: #Bucle para asignar los valores de las variables proposicionales correspondientes a todas las filas.
                periodo = (2 ** len(var_logs)) / divisor #Calcula el período de variación

                if (fila // periodo) % 2 == 0: # Asigna verdadero o falso
                    self._Asignar_valores(var, True)
                else:
                    self._Asignar_valores(var, False)
                divisor *= 2

            __Registrar_valores_fila(self, set()) # Asigna los valores del resto de las subfórmulas.

        tabla = dict() #Diccionario donde se ordenan las subfórmulas por nivel de profundidad y se elimina este dato; de modo que quede apto para construir un "DataFrame" de "pandas".

        for prof in range(1, self._Devolver_profundidad() + 1):
            for form, val in val_forms.items():
                if val[0] == prof:
                    tabla.update({form: val[1]})

        tabla = DataFrame(tabla) #Conversión para su presentación tabular

        print(tabla) #Impresión


#============== SUBCLASES de 'Formula' =====================================

class F_CONJ(Formula):

    def __str__(self):
        return "(" + str(self._subform1) + " & " + str(self._subform2) + ")"

    def _Tomar_valor(self):
        if self._subform1._Tomar_valor() and self._subform2._Tomar_valor():
            return True
        else:
            return False


class F_DISY(Formula):

    def __str__(self):
        return "(" + str(self._subform1) + " | " + str(self._subform2) + ")"

    def _Tomar_valor(self):
        if self._subform1._Tomar_valor() or self._subform2._Tomar_valor():
            return True
        else:
            return False


class F_COND(Formula):

    def __str__(self):
        return "(" + str(self._subform1) + " -> " + str(self._subform2) + ")"

    def _Tomar_valor(self):
        if not self._subform1._Tomar_valor() or self._subform2._Tomar_valor():
            return True
        else:
            return False


class F_NEG(Formula):

    def __str__(self):
        return '!' + str(self._subform1)

    def _Tomar_valor(self):
        if not self._subform1._Tomar_valor():
            return True
        else:
            return False

    def __sub__(self, other):
        raise ArithmeticError("La resta no está definida para fórmulas unimembres.")


class F_DUP(Formula):

    def __str__(self):
        return "(" + str(self._subform1) + ")"

    def _Tomar_valor(self):
        if self._subform1._Tomar_valor():
            return True
        else:
            return False

    def __sub__(self, other):
        raise ArithmeticError("La resta no está definida para fórmulas unimembres. Puede intentar la operación para la subfórmula no redundante.")

class F_ATOM(Formula):

    def __init__(self, subf1):
        self._subform1 = subf1 # A diferencia del resto de las subclases de "Formula", la subfórmula que compone a F_ATOM no es ella misma un objeto "Formula", sino un string; de modo de evitar una recursión infinita.

        self._valor = None # Otra diferencia de F_ATOM es que su valor de verdad se define de manera absoluta, mientras que el del resto se define por relación a éste.

    def __str__(self):
        return self._subform1

    #def Imprimir_arbol(self):
    #    print(self, end=" | ")

    def __sub__(self, other):
        raise ArithmeticError("La resta no está definida para fórmulas unimembres.")

    def __getitem__(self, index):
        raise IndexError("Las variables proposicionales no contienen subfórmulas.")

    def __setitem__(self, index, subf):
        raise IndexError("Las variables proposicionales no contienen subfórmulas.")

    def _Devolver_profundidad(self): #También la profundidad de F_ATOM se puede decir que es absoluta.
        return 1

    def _Tomar_valor(self):
        return self._valor

#======================= FIN del MÓDULO 'logprop' =========================
