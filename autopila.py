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
    for palabra in entrada.split():
        if palabra in reserved:
            simbolos_procesados.append(palabra)
        else:
            for char in palabra:
                simbolos_procesados.append('alpha' if char.isalpha() else char)
    return simbolos_procesados + ['$']

# Función de analizador sintáctico.
def analizador(entrada):
    pila = ['$', 'REPETITIVA']
    registro = [' '.join(pila)]  # Inicializa el registro de los estados de la pila
    entry_symbols = transformador(entrada.strip())

    while pila and entry_symbols:
        tope_pila = pila[-1]  # Accede al elemento en la cima de la pila sin eliminarlo
        current_symbol = entry_symbols[0]  # Obtiene el próximo símbolo de entrada

        if tope_pila == current_symbol:
            if tope_pila == '$':  # Si ambos son el símbolo de fin de entrada
                registro.append('Aceptación')
                break
            pila.pop()  # Elimina el símbolo procesado de la pila
            entry_symbols.pop(0)  # Avanza al siguiente símbolo de entrada
            registro.append(' '.join(pila or ['Aceptación']))  # Estado de aceptación
        elif (tope_pila, current_symbol) in tabla_predictiva:
            pila.pop()  # Elimina el símbolo no terminal procesado
            regla_produccion = tabla_predictiva[(tope_pila, current_symbol)]
            if regla_produccion != ['epsilon']:  # Si no es una producción epsilon
                pila.extend(reversed(regla_produccion))  # Agrega los elementos de la producción en orden inverso
            registro.append(' '.join(pila))  # Actualiza el registro después de cada cambio
        else:
            return '\n'.join(registro) + f'\nError en la entrada cerca de "{current_symbol}"'

    return '\n'.join(registro)