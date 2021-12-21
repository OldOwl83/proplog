'''
    Este módulo construye objetos del tipo 'Formula', que representan una fórmula
de la Lógica Proposicional definida por su conectiva principal. A su vez, cada
uno de estos objetos puede estar compuesto por otros objetos de su misma clase base,
que representan sus subfórmulas (los que a su vez pueden estar compuestos por
otros objetos, conformando un árbol de objetos 'Formula'). Esta ramificación
concluye con las fórmulas atómicas o variables proposicionales ('F_ATOM(Formula)')
cuyas únicas propiedades son un string que la identifica y un valor booleano que
funciona como base para determinar el valor de las fórmulas compuestas (objetos
'F_ATOM' con un mismo string siempre tienen el mismo valor booleano).
    Estos objetos, por su parte, disponen de un método para calcular e imprimir
por pantalla su tabla de verdad correspondiente.

Interfaz pública:

Constructor:
        'FBF(string fbf)', donde fbf expresa una fórmula
bien formada de la Lógica Proposicional en texto plano.

Métodos:
        'FBF.Generar_tabla('), calcula e imprime por pantalla la tabla de verdad
correspondiente.

Sintaxis para los string que expresan las fórmulas:

Operadores:
            Conjunción: &
            Disyunción: |
            Implicación: ->
            Negación: !

    No hay un orden de precedencia entre los operadores, de modo que debe gestionar toda la sintaxis de las fórmulas con el uso de paréntesis "()".
'''

#Librerías utilizadas
from re import fullmatch
from pandas import DataFrame
from pandas import options

#Configuración para la salida de las tablas de verdad (librería pandas)
options.display.max_rows = 128
options.display.max_columns = 40
options.display.width = 100

'''
Clase general: aunque técnicamente no es la clase base de los objetos que
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
        elems_form = cls.Descomponer_string(form_str)

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
    def Descomponer_string(form_str):

        subforms = ["", "", ""] # Almacena los elementos componentes de la fórmula expresada en el string (subfórmula izq, conectiva/tipo, [subfórmula der])

        form_str = form_str.replace(' ', '') # Limpia los espacios en blanco

# Función para validar los elementos definidos por paréntesis exteriores. Esta función complementa el análisis hecho con las expresiones regulares, ya que las mismas no pueden controlar la paridad entre paréntesis izquierdos y derechos dentro de un elemento interno de la fórmula. Devuelve el elemento sin los paréntesis externos, o -1 si no es validado
        def Tomar_parentesis(string):
            p_izq = 0  # Contadores de paréntesis izquierdos y derechos
            p_der = 0
            pos = 0 # Contador de ciclos

            if string[0] != '(' and string[-1] != ')': return -1

            for char in string:
                pos += 1
                if char == '(': p_izq += 1
                elif char == ')':
                    p_der += 1
                # Cuando los paréntesis derechos son tantos como los izquierdos (pero más que cero), y coinciden con los extremos del elementos, se completó la validación
                    if p_der == p_izq and p_der > 0 and pos == len(string): return string[1:-1]  # Devuelve el elemento sin paréntesis exteriores

            return -1

#(Continúa "Descomponer_string()")
        #Busca determinar la estructura general de la fórmula, con expresiones regulares

        #Pregunta si la fórmula es una variable proposicional aislada
        if fullmatch("[A-Za-z]+", form_str):
            subforms[0] = form_str
            subforms[1] = 'at'

        #Pregunta si la fórmula es una negación
        elif fullmatch("![A-Za-z]+", form_str) or fullmatch("!\([A-Za-z()&|\->!]+\)", form_str):
            if form_str[1] == '(': subforms[0] = form_str[2:-1]
            else: subforms[0] = form_str[1:]
            subforms[1] = '!'

        #Pregunta si la fórmula está compuesta por dos subfórmulas coordinadas por una conectiva central
        else:
            fr_patt = fullmatch("^(!{0,1}\([A-Za-z()&|\->!]+\))(&|->|\|)(!{0,1}\([A-Za-z()&|\->!]+\))$", form_str) or fullmatch("^(!{0,1}\([A-Za-z()&|\->!]+\))(&|->|\|)(!{0,1}[A-Za-z]+)$", form_str) or fullmatch("^(!{0,1}[A-Za-z]+)(&|->|\|)(!{0,1}\([A-Za-z()&|\->!]+\))$", form_str) or fullmatch("^(!{0,1}[A-Za-z]+)(&|->|\|)(!{0,1}[A-Za-z]+)$", form_str)

            #Registra los tres elementos en la lista 'subforms', validando los elementos que están encerrados entre paréntesis (los demás ya son controlados por las expresiones regulares)
            if fr_patt:
                if fr_patt.group(1)[0] == '(':
                    subforms[0] = Tomar_parentesis(fr_patt.group(1))
                    if subforms[0] == -1: return -1
                else:
                    subforms[0] = fr_patt.group(1)

                if fr_patt.group(3)[0] == '(':
                    subforms[2] = Tomar_parentesis(fr_patt.group(3))
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
        self.subform1 = FBF(subf1) #Todas las subfórmulas están compuestas por al menos otra subfórmula, salvo las atómicas (F_ATOM), que tienen un constructor especial
        if subf2:
            self.subform2 = FBF(subf2)
        else:
            self.subform2 = None

    def __str__(self): pass #El casting a string se define de manera particular en las subclases

#Método que devuelve para cada subfórmula su nivel de profundidad en relación a la fórmula que lo llamó
    def Devolver_profundidad(self):
        if self.subform2: #La profundidad de toda subfórmula puede calcularse como la mayor profundidad alcanzada por sus subfórmulas, más uno (teniendo en cuenta que siempre las subfórmulas atómicas están en el primer nivel)
            prof_acum = max(self.subform1.Devolver_profundidad(),
                            self.subform2.Devolver_profundidad())
        else:
            prof_acum = self.subform1.Devolver_profundidad()
        return prof_acum + 1

#Método que devuelve la sucesión de todas las subfórmulas que componen la fórmula que lo llamó. Aun está sin uso... para futuras aplicaciones.
    def Imprimir_arbol(self):
        self.subform1.Imprimir_arbol()
        if self.subform2:
            self.subform2.Imprimir_arbol()
        print(self, end=" | ")

#Método recursivo que devuelve el valor de verdad de cada subfórmula, dependiendo del valor asignado a las variables proposicionales. Tiene una definición especial en cada subclase.
    def Tomar_valor(self): pass

#Método que construye la tabla de verdad completa de la fórmula que lo llamó (incluyendo los valores de sus subfórmulas), y la imprime por pantalla.
    def Generar_tabla(self):
        val_forms = dict() #Almacena para el string que representa cada subfórmula (keys) su nivel de profundidad y los valores de verdad que le corresponden en cada fila de la tabla.

    #Función que registra el nombre (string) de todas las subfórmulas como "keys" del diccionario 'val_forms', y le asocia su respectivo nivel de profundidad, y una lista vacía que se irá completando con los valores de verdad que le corresponden en cada fila de la tabla.
        def Registro_formulas(self):
            nonlocal val_forms

            val_forms.update(
                {str(self): [self.Devolver_profundidad(), list()]})

            if type(self) != F_ATOM:
                Registro_formulas(self.subform1)
                if self.subform2:
                    Registro_formulas(self.subform2)

    #Función recursiva que recorre el árbol de subfórmulas hasta alcanzar las variables proposicionales que coinciden con el string "var", para poder asignarles el mismo valor de verdad "val".
        def Asignar_valores(self, var, val):
            if type(self) == F_ATOM:
                if self.subform1 == var:
                    self.valor = val
            else:
                Asignar_valores(self.subform1, var, val)
                if self.subform2:
                    Asignar_valores(self.subform2, var, val)

    #Función recursiva que recorre el árbol de subfórmulas para tomar su valor de acuerdo al valor establecido en las variables proposicionales, y lo almacena en las listas de valores correspondiente a cada una de ellas en el diccionario "val_forms".
        def Registrar_valores_fila(self, list_rep):
            for forms in val_forms.keys():
                if str(self) == forms and not forms in list_rep:
                    val_forms[forms][1].append(self.Tomar_valor()) #Almacena el valor correspondiente a la subfórmula particular.
                    list_rep.add(forms) # Set para controlar que los valores de verdad no se dupliquen cuando hay dos subfórmulas iguales.

                    break
            # Y llama al resto del árbol
            if type(self) != F_ATOM:
                Registrar_valores_fila(self.subform1, list_rep)
                if self.subform2:
                    Registrar_valores_fila(self.subform2, list_rep)

#(continúa '.Generar_tabla()')
        Registro_formulas(self) # Registro del árbol de subfórmulas en el diccionario "val_forms".

        var_logs = [val for val in val_forms.keys() if val_forms[val][0] == 1] # Almacena las variables proposicionales, que reconoce por su nivel de profundidad.

        for fila in range(2**len(var_logs)): # Calcula las filas de la tabla de verdad según la cantidad de variables proposicionales
            divisor = 2 # Modifica el período con que variará el valor de verdad de las variables proposicionales en las filas de la tabla.
            for var in var_logs: #Bucle para asignar los valores de las variables proposicionales correspondientes a todas las filas.
                periodo = (2 ** len(var_logs)) / divisor #Calcula el período de variación

                if (fila // periodo) % 2 == 0: # Asigna verdadero o falso
                    Asignar_valores(self, var, True)
                else:
                    Asignar_valores(self, var, False)
                divisor *= 2

            Registrar_valores_fila(self, set()) # Asigna los valores del resto de las subfórmulas.

        tabla = dict() #Diccionario donde se ordenan las subfórmulas por nivel de profundidad y se elimina este dato; de modo que quede apto para construir un "DataFrame" de "pandas".

        for prof in range(1, self.Devolver_profundidad() + 1):
            for form, val in val_forms.items():
                if val[0] == prof:
                    tabla.update({form: val[1]})

        tabla = DataFrame(tabla) #Conversión para su presentación tabular

        print(tabla) #Impresión


#============== SUBCLASES de 'Formula' =====================================

class F_CONJ(Formula):

    def __str__(self):
        return "(" + str(self.subform1) + " & " + str(self.subform2) + ")"

    def Tomar_valor(self):
        if self.subform1.Tomar_valor() and self.subform2.Tomar_valor():
            return True
        else:
            return False


class F_DISY(Formula):

    def __str__(self):
        return "(" + str(self.subform1) + " | " + str(self.subform2) + ")"

    def Tomar_valor(self):
        if self.subform1.Tomar_valor() or self.subform2.Tomar_valor():
            return True
        else:
            return False


class F_COND(Formula):

    def __str__(self):
        return "(" + str(self.subform1) + " -> " + str(self.subform2) + ")"

    def Tomar_valor(self):
        if not self.subform1.Tomar_valor() or self.subform2.Tomar_valor():
            return True
        else:
            return False


class F_NEG(Formula):

    def __str__(self):
        return '!' + str(self.subform1)

    def Tomar_valor(self):
        if not self.subform1.Tomar_valor():
            return True
        else:
            return False


class F_DUP(Formula):

    def __str__(self):
        return "(" + str(self.subform1) + ")"

    def Tomar_valor(self):
        if self.subform1.Tomar_valor():
            return True
        else:
            return False


class F_ATOM(Formula):

    def __init__(self, subf1):
        self.subform1 = subf1 # A diferencia del resto de las subclases de "Formula", la subfórmula que compone a F_ATOM no es ella misma un objeto "Formula", sino un string; de modo de evitar una recursión infinita.

        self.valor = None # Otra diferencia de F_ATOM es que su valor de verdad se define de manera absoluta, mientras que el del resto se define por relación a éste.

    def __str__(self):
        return self.subform1

    def Imprimir_arbol(self):
        print(self, end=" | ")

    def Devolver_profundidad(self): #También la profundidad de F_ATOM se puede decir que es absoluta.
        return 1

    def Tomar_valor(self):
        return self.valor

#======================= FIN del MÓDULO 'logprop' =========================
