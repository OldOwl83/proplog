import logprop as lp

#======= EJEMPLO de USO del MÓDULO 'LOGPROP' ===========================================

print('''
Este programa le permite generar tablas de verdad a partir de una fórmula dada.
No hay un orden de precedencia entre los operadores, de modo que debe
gestionar toda la sintaxis de las fórmulas con el uso de paréntesis "()".
Operadores:
            Conjunción: &
            Disyunción: |
            Implicación: ->
            Negación: !''')

while 1:
    print()
    print("Introduzca una fórmula de la Lógica Proposicional, o '0' para salir:")
    fr = input()
    print()
    if fr == '0':
        exit()
    else:
        try:
            fr = lp.FBF(fr) #Llamadas al constructor y al método
            fr.Generar_tabla()
        except Exception as e: #Si la fórmula ingresada está mal formada, levanta una excepción
            print(e)
