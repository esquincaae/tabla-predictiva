tabla_predictiva = {
    ('REPETITIVA', 'do'): ['do', 'CUERPO', 'MIENTRAS'],
    ('CUERPO', "{}"): ["{}"],
    ('MIENTRAS', 'mientras'): ['mientras', 'CONDICIONAL'],
    ('CONDICIONAL', '('): ['(', 'EXPRESION', ')'],
    ('EXPRESION', 'alpha'): ['VALOR', 'OPERADOR', 'V'],
    ('VALOR', 'alpha'): ['LETRA', 'RESTO'],
    ('LETRA', 'alpha'): ['alpha'],
    ('RESTO', 'alpha'): ['LETRA', 'RESTO'],
    ('RESTO', '=='): ['epsilon'],
    ('RESTO', '!='): ['epsilon'],
    ('V', 'true'): ['true'],
    ('V', 'false'): ['false'],
    ('OPERADOR', '=='): ['=='],
    ('OPERADOR', '!='): ['!=']
}

symbols = {key[1] for key in tabla_predictiva.keys()}

# Conversión de la entrada a una secuencia de símbolos terminales ya definidos
def transformador(entrada):
    simbolos_procesados = []
    entrada_reemplazada = entrada.replace('{}', ' {} ').replace('(', ' ( ').replace(')', ' ) ').replace('==', ' == ').replace('!=', ' != ')
    elementos = entrada_reemplazada.split()

    for elemento in elementos:
        if elemento in ['do', 'mientras', '{}', '(', ')', '==', '!=', 'true', 'false']:
            simbolos_procesados.append(elemento)
        elif elemento == '(' or elemento == ')':
            simbolos_procesados.append(elemento)
        else:
            for char in elemento:
                simbolos_procesados.append('alpha')
                #print(f"{simbolos_procesados}")
        #print(f"{elemento}")
    return simbolos_procesados + ['$']


# Función de analizador sintáctico.
def analizador(entrada):
    pila = ['$', 'REPETITIVA']
    registro = [' '.join(pila)]  # Inicializa el registro de los estados de la pila
    entry_symbols = transformador(entrada.strip())

    while pila and entry_symbols:
        tope_pila = pila[-1]
        current_symbol = entry_symbols[0]
        #print(f"Analizando: Tope de pila = {tope_pila}, Símbolo actual = {current_symbol}")
        #print(f"Estado de la pila: {pila}")
        print(f"Símbolos restantes de entrada: {entry_symbols}")

        if tope_pila == current_symbol:
            # Coincidencia directa: eliminar el símbolo de la pila y la entrada.
            pila.pop()
            entry_symbols.pop(0)
        elif (tope_pila, current_symbol) in tabla_predictiva:
            # Expansión basada en la tabla predictiva.
            pila.pop()  # Elimina el elemento actual de la pila.
            elementos_produccion = tabla_predictiva[(tope_pila, current_symbol)]
            if elementos_produccion != ['epsilon']:
                # Agrega los elementos de la producción en orden inverso.
                pila.extend(reversed(elementos_produccion))
        else:
            # Error: no se encuentra una regla aplicable.
            return '\n'.join(registro) + f'\nError en la entrada cerca de "{current_symbol}"'

        # Actualizar el registro después de cada paso.
        registro.append(' '.join(pila) if pila else 'Aceptación')

    return '\n'.join(registro)
