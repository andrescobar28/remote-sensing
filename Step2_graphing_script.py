# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 20:15:39 2022

@author1: ANDRES JULIAN ESCOBAR CARDONA - Correo: andres.julian.escobar@correounivalle.edu.co
@author2: EDUARDO TAMAYO CORDOBA - Correo: eduardo.tamayo@correounivalle.edu.co
@author3: VALENTINA SEVILLANO RAMIREZ - Correo: valentina.sevillano@correounivalle.educ.o
@author4: LIZETH CATHERINE CARDENAS ALVARADO - Correo: lizeth.cardenas@correounivalle.edu.co

UNIVERSIDAD DEL VALLE - INGENIERÍA TOPOGRÁFICA
2022-1

OBJETIVO DEL SCRIPT:
Graficación de resultados y parámetros obtenidos con Step1_spectral-signature-reader.py

SOLICITADO POR: CESAR EDWIN GARCIA CORTES - Correo: cesar.edwin.garcia@correounivalle.edu.co
Ingeniero Topográfico - Magister en Percepción Remota
Docente Curso TELEDETECCIÓN ESPACIAL

"""
# -------------------------- IMPORTACIÓN DE LIBRERÍAS ------------------------------------------------
import matplotlib.pyplot as plt # Librería para gráficas
from os import scandir, mkdir # Librería para manejo de directorios y ficheros
from pandas import read_excel # Librería para manejo de dataFrames
from time import sleep

# ----------------------------- DEFINICIÓN DE FUNCIONES --------------------------------------------------
def grafico_firma_variedad_estadistico(variedades, escaneo_variedades, lista_x, lista_y, tipo_firma):
    '''

    Parameters
    ----------
    lista_x : LIST
        Corresponde a la lista que contiene los valores del ejeX
    lista_y : LIST
        Corresponde a la lista que contiene los valores del ejeY
    tipo_firma : STRING
        Corresponde al tipo de firma (Mínima, Máxima, Promedio)

    Returns
    -------
    La función genera un gráfico con los parámetros especificados

    '''
    try:
        mkdir('Gráficos por Variedad y Estadístico (min-max-prom)')
    except:
        None
    
    for k in range(len(variedades)):
        fig, ax = plt.subplots()
        for i in range(len(escaneo_variedades[0])):
            ax.plot(lista_x[k][i], lista_y[k][i], label = f'{escaneo_variedades[0][i]}')
            print(f"Proceso de gráficas No. {k+1}-{i+1}... {round(100/(len(escaneo_variedades[0]))*(i+1),2)}%")
        ax.legend(loc = 'upper left')
        ax.set_ylabel('Reflectancia [%]')
        ax.set_xlabel("Longitud de Onda [nm]")
        ax.set_title(f'Firmas Espectrales Temporales ρ-{tipo_firma}\nVariedad {variedades[k]}', loc = "center", fontdict = {'fontsize':10, 'fontweight':'bold'})
        ax.set_ylim([0,100])
        ax.set_xlim([400,900])
        ax.grid(color = '#F5E9E8', linestyle = 'dashdot')
        # plt.show()
        plt.savefig(f'Gráficos por Variedad y Estadístico (min-max-prom)/Firma_{variedades[k]}_{tipo_firma}.png', dpi=600)
        print(f"\nProceso de guardado No. {k+1}... {round(100/(len(variedades))*(k+1),2)}%")

# ------------------------------------- GRÁFICOS POR VARIEDAD POR ESTADÍSTICO ---------------------------------

print("Loading... Iniciando creación de gráficos")

# Filtrar archivos por variedad
escaneo_variedades = []
with scandir('.') as ficheros:
        directorios = [fichero.name for fichero in ficheros if fichero.is_dir()]
        escaneo_variedades.append(directorios)
escaneo_variedades[0].remove('Archivos_XLSX_FirmasEspectrales')
# print(escaneo_variedades[0])

# Escaneo de ficheros
variedades = []
with scandir(f'{escaneo_variedades[0][0]}') as ficheros:
    for fichero in ficheros:
        variedades.append(fichero.name)

# print(variedades)

matriz_conjunto_variedades = []
for i in range(len(escaneo_variedades[0])):
    sub_lista = []
    for j in range(len(variedades)):        
        sub_lista.append(f'{escaneo_variedades[0][j]}_{variedades[i]}.xlsx')
    matriz_conjunto_variedades.append(sub_lista)
    
# print(matriz_conjunto_variedades)

# Construcción de dataframes para los gráficos
lista_x_dataframes = []
lista_y_dataframes_maximo = []
lista_y_dataframes_minimo = []
lista_y_dataframes_promedio = []
for i in range(len(matriz_conjunto_variedades)):
    lista_x_dataframes_control = []
    lista_y_dataframes_maximo_control = []
    lista_y_dataframes_minimo_control = []
    lista_y_dataframes_promedio_control = []
    for j in range(len(matriz_conjunto_variedades[i])):
        df = read_excel(f'Archivos_XLSX_FirmasEspectrales/{matriz_conjunto_variedades[i][j]}')
        lista_x_dataframes_control.append(df['longitud_onda'].tolist())
        lista_y_dataframes_promedio_control.append(df['reflect_med'].tolist())
        lista_y_dataframes_maximo_control.append(df['reflect_maxima'].tolist())
        lista_y_dataframes_minimo_control.append(df['reflect_minima'].tolist())
    lista_x_dataframes.append(lista_x_dataframes_control)
    lista_y_dataframes_maximo.append(lista_y_dataframes_maximo_control)
    lista_y_dataframes_minimo.append(lista_y_dataframes_minimo_control)
    lista_y_dataframes_promedio.append(lista_y_dataframes_promedio_control)

# print(len(lista_x_dataframes))
# print(len(lista_y_dataframes_maximo))
# print(len(lista_y_dataframes_minimo))
# print(len(lista_y_dataframes_promedio))

# Gráficos por varidad en las tres fechas con reflectancia máxima
grafico_firma_variedad_estadistico(variedades, escaneo_variedades, 
                        lista_x_dataframes, lista_y_dataframes_maximo, 'máxima')

# Gráficos por varidad en las tres fechas con reflectancia minima
grafico_firma_variedad_estadistico(variedades, escaneo_variedades, 
                        lista_x_dataframes, lista_y_dataframes_minimo, 'mínima')

# Gráficos por varidad en las tres fechas con reflectancia promedio
grafico_firma_variedad_estadistico(variedades, escaneo_variedades, 
                        lista_x_dataframes, lista_y_dataframes_promedio, 'promedio')

# ---------------------------- GRÁFICA POR VARIEDAD POR FECHA (mínimo-promedio-máximo) -------------------

lista_control_global = []

# print(matriz_conjunto_variedades)

# Creación de directorio
try:
    mkdir('Gráficos por Fecha y Variedad (min-max-prom)')
except:
    None

for i in range(len(matriz_conjunto_variedades)):    
    for k in range(len(matriz_conjunto_variedades[i])):
        lista_subcontrol = []
        lista_subcontrol.append(lista_y_dataframes_maximo[i][k])
        lista_subcontrol.append(lista_y_dataframes_promedio[i][k])
        lista_subcontrol.append(lista_y_dataframes_minimo[i][k])
    
        # print(len(lista_subcontrol))
        lista_control_global.append(lista_subcontrol)
        
# print(len(lista_control_global[0]))
# print(len(lista_y_dataframes_minimo))
# print(len(lista_control_global))
# print(len(lista_control_global[0]))


tipo = ['ρ-máximo','ρ-promedio','ρ-mínimo']
titulos = []

# Aplanaminto de lista matriz_conjunto_variedades
for item in matriz_conjunto_variedades:
    titulos += item

for k in range(len(lista_control_global)):
    fig, ax = plt.subplots()
    for i in range(len(lista_control_global[k])):       
        ax.plot(lista_x_dataframes[0][i], lista_control_global[k][i], label = f'{tipo[i]}')       
        print(f"Proceso 2 de gráficas No. {k+1}-{i+1}... {round(100/(len(lista_control_global))*(i+1),2)}%")
    ax.legend(loc = 'upper left')
    ax.set_ylabel('Reflectancia [%]')
    ax.set_xlabel("Longitud de Onda [nm]")
     
    ax.set_title(f'Firmas Espectrales por Estadístico\nFecha_Variedad: {titulos[k][:-5]}', loc = "center", fontdict = {'fontsize':10, 'fontweight':'bold'})
   
    ax.set_ylim([0,100])
    ax.set_xlim([400,900])
    ax.grid(color = '#F5E9E8', linestyle = 'dashdot')
    # plt.show()
    plt.savefig(f'Gráficos por Fecha y Variedad (min-max-prom)/Firma_{titulos[k][:-5]}.png', dpi=600)
    print(f"\nProceso 2 de guardado No. {k+1}... {round(100/(len(lista_control_global))*(k+1),2)}%")

sleep(2)
print("\nEjecución exitosa!")
print("Se ha creado el directorio 'Gráficos por Variedad y Estadístico (min-max-prom)'")
print("Se ha creado el directorio 'Gráficos por Fecha y Variedad (min-max-prom)'")
print("\nPresione ENTER para finalizar...")
input()

