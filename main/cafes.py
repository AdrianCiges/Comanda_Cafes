para_llevar = 'sí'
# para_llevar = 'no'

coffees =  {
    'Sergio #1': 'café con leche normal',
    # 'Sergio #2': 'café con leche doble normal',
    # 'A. Alarcón': 'café con leche normal',
    # 'A. Bayón': 'café con leche normal',
    # 'A. Delgado': 'solo largo doble',
    # 'A. Delgado #2': 'zumo de naranja',
    # 'A. Sáez': 'café con leche normal',
    # 'Adri': 'café con leche sin lactosa',
    # 'Adri #2': 'descafeinado con leche sin lactosa',
    # 'Adri #3': 'té rojo',
    # 'Adri #4': 'té rojo con leche sin lactosa',
    # 'Ana Murillo': 'café con leche desnatada',
    # 'Ana García #1': 'café con leche sin lactosa', 
    # 'Ana García #2': 'solo largo',
    # 'Carlos': 'solo largo',
    # 'Dani A': 'café con leche normal',
    # 'Dani S': 'té negro',
    # 'Dasha': 'café con leche desnatada',
    # 'Iván': 'café con leche normal',
    # 'Inés MG': 'café con leche desnatada',
    # 'Inés ML #1': 'café con leche desnatada',
    # 'Inés ML #2': 'café con leche sin lactosa',
    # 'Javi Brenes': 'café con leche normal',
    # 'Javi Nieto #1': 'Cola Cao',
    # 'Javi Nieto #2': 'zumo de naranja',
    # 'María': 'café con leche desnatada',
    # 'Maxi': 'café con leche normal',
    # 'Mercedes': 'Cola Cao para llevar',
    # 'Mercedes #2': 'descafeinado con leche sin lactosa',
    # 'Lucía': 'descafeinado con leche normal',
    # 'Rafa': 'solo largo',
    # 'Víctor': 'café con leche normal',
}

custom_tab = '   '
tipo_cafe = ''
counter = 0

def extract_drinks(dicc):
    drinks = []

    for i,j in dicc.items():
        if 'café con leche' in j:
            tipo_cafe = j.find('leche')
            j = j[:tipo_cafe + 5]
            drinks.append(j)

    drinks_dict = {}

    for item in drinks:
        drinks_dict[item] = drinks_dict.get(item, 0) + 1    
        
    command = []

    for i,j in drinks_dict.items():
        command.append('•' + str(j) + ' ' + str(i))

    final = '\n'.join(command)

    return final

def extract_milk(dicc):
    custom_tab = '   '    
    milks = []

    for i,j in dicc.items():
        if 'café con leche' in j:
            tipo_cafe = j.find('leche')
            j = j[tipo_cafe + 6:]
            milks.append(j)

    milks_dict = {}

    for item in milks:
        milks_dict[item] = milks_dict.get(item, 0) + 1    
        
    command = []

    for i,j in milks_dict.items():
        command.append(custom_tab + '•' + str(j) + ' con leche ' + str(i))

    final = '\n'.join(command)
    return final

def extract_other_drinks(dicc):
    other_drinks = []

    for i,j in dicc.items():
        if 'café con leche' not in j:
            other_drinks.append(j)

    other_drinks_dict = {}

    for item in other_drinks:
        other_drinks_dict[item] = other_drinks_dict.get(item, 0) + 1    
    
    command = []

    for i,j in other_drinks_dict.items():
        command.append('•' + str(j) + ' ' + str(i))
    final = '\n'.join(command)
    return final

print('Hola! Os hago un pedido:\n')
print(extract_drinks(coffees)) 
print(extract_milk(coffees))
print(extract_other_drinks(coffees))
if para_llevar == 'sí':
    print('\n(Todos para llevar y con leche templada)\n')
else:
    print('\n(Todos con leche templada)\n')
print('Muchas gracias! 🙂')