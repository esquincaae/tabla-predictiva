tabla_predictiva = {
    ('REPETITIVA', 'do'): ['do', 'CUERPO', 'MIENTRAS'],
    ('CUERPO', "{}"): ["{}"],
    ('MIENTRAS', 'mientras'): ['mientras', 'CONDICIONAL'],
    ('CONDICIONAL', '('): ['(', 'EXPRESION', ')'],
    ('EXPRESION', 'VALOR'): ['VALOR', 'OPERADOR', 'V'],
    ('VALOR', 'LETRA'): ['LETRA', 'RESTO'],
    ('LETRA', 'alpha'): ['alpha'],
    ('RESTO', 'LETRA'): ['LETRA', 'RESTO'],
    ('RESTO', '=='): ['epsilon'],
    ('RESTO', '!='): ['epsilon'],
    ('V', 'true'): ['true'],
    ('V', 'false'): ['false'],
    ('OPERADOR', '=='): ['=='],
    ('OPERADOR', '!='): ['!=']
}

symbols = {key[1] for key in tabla_predictiva.keys()}
reserved = {'do', 'mientras', 'true', 'false'}

# Conversión de la entrada a una secuencia de símbolos terminales ya definidos
def transformador(entrada):
    simbolos_procesados = []
    entrada_reemplazada = entrada.replace('{}', ' {} ').replace('(', ' ( ').replace(')', ' ) ')
    elementos = entrada_reemplazada.split()

    for elemento in elementos:
        if elemento in reserved or elemento == '{}' or elemento == '==' or elemento == '!=' or elemento == 'false' or elemento == 'true':
            simbolos_procesados.append(elemento)
        elif elemento == '(' or elemento == ')':
            simbolos_procesados.append(elemento)
        else:
            for char in elemento:
                simbolos_procesados.append('alpha')
        print(f"{elemento}")
    return simbolos_procesados + ['$']


# Función de analizador sintáctico.
def analizador(entrada):
    pila = ['$', 'REPETITIVA']
    registro = [' '.join(pila)]  # Inicializa el registro de los estados de la pila
    entry_symbols = transformador(entrada.strip())

    while pila and entry_symbols:
        tope_pila = pila[-1]  # Accede al elemento en la cima de la pila sin eliminarlo
        current_symbol = entry_symbols[0]  # Obtiene el próximo símbolo de entrada
        #print(f"Analizando: Tope de pila = {tope_pila}, Símbolo actual = {current_symbol}")
        #print(f"Estado de la pila: {pila}")
        #print(f"Símbolos restantes de entrada: {entry_symbols}")

        if tope_pila == current_symbol:
            if tope_pila == '$':  # Si ambos son el símbolo de fin de entrada
                registro.append('Aceptación')
                break
            pila.pop()  # Elimina el símbolo procesado de la pila
            entry_symbols.pop(0)  # Avanza al siguiente símbolo de entrada
        elif (tope_pila, current_symbol) in tabla_predictiva:
            pila.pop()  # Elimina el símbolo no terminal procesado
            regla_produccion = tabla_predictiva[(tope_pila, current_symbol)]
            if regla_produccion != ['epsilon']:  # Si no es una producción epsilon
                pila.extend(reversed(regla_produccion))  # Agrega los elementos de la producción en orden inverso
        else:
            return '\n'.join(registro) + f'\nError en la entrada cerca de "{current_symbol}"'

        registro.append(' '.join(pila) if pila else 'Aceptación')  # Actualiza el registro después de cada cambio

    return '\n'.join(registro)