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
    return simbolos_procesados + ['$']



def analizador(entrada):
    pila = ['$', 'REPETITIVA']
    registro = [' '.join(pila)]
    entry_symbols = transformador(entrada.strip())

    while pila and entry_symbols:
        tope_pila = pila[-1]
        current_symbol = entry_symbols[0]
        #print(f"Analizando: Tope de pila = {tope_pila}, Símbolo actual = {current_symbol}")
        #print(f"Estado de la pila: {pila}")
        #print(f"Símbolos restantes de entrada: {entry_symbols}")

        if tope_pila == current_symbol:
            pila.pop()
            entry_symbols.pop(0)
        elif (tope_pila, current_symbol) in tabla_predictiva:
            pila.pop() 
            elementos_produccion = tabla_predictiva[(tope_pila, current_symbol)]
            if elementos_produccion != ['epsilon']:
                pila.extend(reversed(elementos_produccion))
        else:
            return '\n'.join(registro) + f'\nError en la entrada cerca de "{current_symbol}"'
        registro.append(' '.join(pila) if pila else 'Aceptación')

    return '\n'.join(registro)
