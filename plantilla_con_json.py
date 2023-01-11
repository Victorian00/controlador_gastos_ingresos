import os
import math
import json
from datetime import date
from datetime import datetime

path_archivo_python = str(__file__)
path = path_archivo_python.rsplit('/',1)[0]
print(path)

dia_actual = date.today()
fecha_actual = datetime.now()
meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
dias = ("Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")

localizador_referencia = '{year}_Gastos'.format(year=fecha_actual.year)
print(localizador_referencia)
today = '{dia}-{numero}'.format(dia=dias[dia_actual.weekday()], numero=fecha_actual.day)

# Abrimos el JSON
json_file = '{path}/{name}.json'.format(path=path,name=localizador_referencia)
json_name = '{name}.json'.format(name=localizador_referencia)
json_exist = False

list_files = os.listdir(path)
for file in list_files:
    if file == json_name:
        json_exist = True

if json_exist:
    with open(json_file, 'r+') as file:
        data = json.load(file)
else:
    data = {}
    for mes in meses:
        data[mes] = {}
    
print(data)


print('------------------------------------------------------------------------')

# Reflejar sueldo mensual

for mes in data:
    if mes == meses[fecha_actual.month-1]:
        already_sueldo = False
        for item in data[mes]:
            if item == 'Sueldo percibido este mes (€)':
                already_sueldo = True
                break
            else:
                already_sueldo = False
        if already_sueldo != True:
            sueldo_mensual_string = input('Sueldo percibido este mes: ')
            try:
                sueldo_mensual = float(sueldo_mensual_string)
            except:
                sueldo_mensual = float(sueldo_mensual_string.replace(',','.'))
            data[mes]['Sueldo percibido este mes (€)'] = sueldo_mensual


print('------------------------------------------------------------------------')


# Reflejar gastos

gastos = True
for mes in data:
    if mes == meses[fecha_actual.month-1]:
        for item in data[mes]:
            if item == 'Gastos':
                already_gastos = True
                break
            else:
                already_gastos = False
        if already_gastos != True:
            data[mes]['Gastos'] = {}
        while gastos == True:
            respuesta = input('¿Quieres introducir gasto? (si/no) ')
            if respuesta == 'si':
                already_day = False
                for day in data[mes]['Gastos']:
                    if day == today:
                        already_day = True
                        break
                    else:
                        already_day = False
                if already_day != True:
                    data[mes]['Gastos'][today] = {}
                concepto_gasto = input('Introduce concepto de gasto: ')
                valor_gasto_string = input('Valor del gasto en €: ')
                try: 
                    valor_gasto = float(valor_gasto_string)
                except:
                    valor_gasto = float(valor_gasto_string.replace(',','.'))
                data[mes]['Gastos'][today][concepto_gasto] = valor_gasto
            else:
                gastos = False


print('------------------------------------------------------------------------')


# Reflejar ingresos

ingresos = True
for mes in data:
    if mes == meses[fecha_actual.month-1]:
        for item in data[mes]:
            if item == 'Ingresos':
                already_ingresos = True
                break
            else:
                already_ingresos = False
        if already_ingresos != True:
            data[mes]['Ingresos'] = {}
        while ingresos == True:
            respuesta = input('¿Quieres introducir ingreso? (si/no) ')
            if respuesta.find('o') == -1:
                already_day = False
                for day in data[mes]['Ingresos']:
                    if day == today:
                        already_day = True
                    else:
                        already_day = False
                if already_day != True:
                    data[mes]['Ingresos'][today] = {}
                concepto_ingreso = input('Introduce concepto de ingreso: ')
                valor_ingreso_string = input('Valor del ingreso en €: ')
                try:
                    valor_ingreso = float(valor_ingreso_string)
                except:
                    valor_ingreso = float(valor_ingreso_string.replace(',','.'))
                data[mes]['Ingresos'][today][concepto_ingreso] = valor_gasto
            else:
                ingresos = False


print('------------------------------------------------------------------------')

# Balance
for mes in data:
    if mes == meses[fecha_actual.month-1]:
        gastos_totales = 0
        ingresos_totales = data[mes]['Sueldo percibido este mes (€)']
        for day in data[mes]['Gastos']:
            for concepto in data[mes]['Gastos'][day]:
                gastos_totales = gastos_totales + data[mes]['Gastos'][day][concepto]

        for day in data[mes]['Ingresos']:
            for concepto in data[mes]['Ingresos'][day]:
                ingresos_totales = ingresos_totales + data[mes]['Ingresos'][day][concepto]

diferencia = ingresos_totales - gastos_totales
if diferencia > 0:
    capacidad_ahorrar = 'Sí'
else:
    capacidad_ahorrar = 'No'

for mes in data:
    if mes == meses[fecha_actual.month-1]:
        for item in data[mes]:
            if item == 'Balance':
                already_balance = True
                break
            else:
                already_balance = False
        if already_balance != True:
            data[mes]['Balance'] = {}
        data[mes]['Balance']['Gastos totales'] = gastos_totales
        data[mes]['Balance']['Ingresos totales'] = ingresos_totales
        data[mes]['Balance']['Diferencia'] = diferencia
        data[mes]['Balance']['¿Se ha ahorrado este mes?'] = capacidad_ahorrar

print('------------------------------------------------------------------------')

# Tipos de gastos
for mes in data:
    if mes == meses[fecha_actual.month-1]:
        for item in data[mes]:
            if item == 'Tipos de gastos':
                already_tipos_gastos = True
                break
            else:
                already_tipos_gastos = False
        if already_tipos_gastos != True:
            data[mes]['Tipos de gastos'] = []
        for dia in data[mes]['Gastos']:
            for gasto in data[mes]['Gastos'][dia]:
                print(gasto)
                data[mes]['Tipos de gastos'].append(gasto)
        print(data[mes]['Tipos de gastos'])
        for index_prin,gasto in enumerate(data[mes]['Tipos de gastos']):
            for index_sec,gasto_duplicado in enumerate(data[mes]['Tipos de gastos']):
                if index_prin == index_sec:
                    continue
                elif gasto == gasto_duplicado:
                    data[mes]['Tipos de gastos'].pop(index_sec)

print('------------------------------------------------------------------------')

# Porcentaje de gastos 
for mes in data:
    if mes == meses[fecha_actual.month-1]:
        for item in data[mes]:
            if item == 'Porcentaje de gastos':
                already_porcentaje_gastos = True
                break
            else:
                already_porcentaje_gastos = False
        if already_porcentaje_gastos != True:
            data[mes]['Porcentaje de gastos'] = {}
        for tipo_gasto in data[mes]['Tipos de gastos']:
            sumatorio_gasto_producto = 0
            for day in data[mes]['Gastos']:
                for concepto_gasto in data[mes]['Gastos'][day]:
                    if tipo_gasto == concepto_gasto:
                        sumatorio_gasto_producto = sumatorio_gasto_producto + data[mes]['Gastos'][day][concepto_gasto]
            porcentaje_del_gasto_total = sumatorio_gasto_producto*100/gastos_totales
            data[mes]['Porcentaje de gastos'][tipo_gasto] = porcentaje_del_gasto_total


print('------------------------------------------------------------------------')

# Categorías de gastos
for mes in data:
    if mes == meses[fecha_actual.month-1]:
        for item in data[mes]:
            if item == 'Categoria de gastos':
                already_categoria_gastos = True
                break
            else:
                already_categoria_gastos = False
        if already_categoria_gastos != True:
            data[mes]['Categoria de gastos'] = {
                                                    "Compras supermercado": [],
                                                    "Compras bazar chino": [],
                                                    "Fiestas": [],
                                                    "Piso": [],
                                                    "Comer/Cenar fuera": [],
                                                    "Metro": [],
                                                    "Viajes": [],
                                                    "Regalos": [],
                                                    "Otro": []
                                                }
        for categoria in data[mes]['Categoria de gastos']:
            print(categoria)
        hacer_pregunta = True
        while hacer_pregunta == True:
            pregunta = input('¿Quieres añadir otra categoría de gastos? (si/no): ')
            if pregunta == 'si':
                agregar_categoria = input('Nueva categoría: ')
                data[mes]['Categoria de gastos'][agregar_categoria] = []
                hacer_pregunta = True
            elif pregunta == 'no':
                hacer_pregunta = False

print('------------------------------------------------------------------------')





#################################################
# Añadimos la seccion anual

for seccion in data:
    if seccion == 'Balance Anual':
        already_anual = True
        break
    else:
        already_anual = False

if already_anual != True:
    data['Balance Anual'] = {}

gastos_anuales = 0
ingresos_anuales = 0
for mes in data:
    for elemento in data[mes]:
        if elemento == 'Balance':
            gastos_anuales = gastos_anuales + data[mes]['Balance']['Gastos totales']
            ingresos_anuales = ingresos_anuales + data[mes]['Balance']['Ingresos totales']
            break

diferencia_anual = ingresos_anuales - gastos_anuales
data['Balance Anual']['Gastos anuales totales'] = gastos_anuales
data['Balance Anual']['Ingresos anuales totales'] = ingresos_anuales
data['Balance Anual']['Diferencia anual'] = diferencia_anual


# Guardamos el JSON

with open(json_file, 'w') as output:
    json.dump(data, output, indent=4)

print('Archivo guardado')
