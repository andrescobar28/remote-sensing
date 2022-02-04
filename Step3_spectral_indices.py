# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 20:15:39 2022

@author1: ANDRES JULIAN ESCOBAR CARDONA - Correo: andres.julian.escobar@correounivalle.edu.co
@author2: EDUARDO TAMAYO CORDOBA - Correo: eduardo.tamayo@correounivalle.edu.co
@author3: VALENTINA SEVILLANO RAMIREZ - Correo: valentina.sevillano@correounivalle.educ.o

UNIVERSIDAD DEL VALLE - INGENIERÍA TOPOGRÁFICA
2022-1

OBJETIVO DEL SCRIPT:
Graficación de resultados y parámetros obtenidos con Step2_graphing_script.py

SOLICITADO POR: CESAR EDWIN GARCIA CORTES - Correo: cesar.edwin.garcia@correounivalle.edu.co
Ingeniero Topográfico - Magister en Percepción Remota
Docente Curso TELEDETECCIÓN ESPACIAL

"""

# Importación de Librerías
from pandas import read_excel, DataFrame
from statistics import mean
from os import scandir, mkdir
from math import sqrt
from time import sleep

# Lectura de archivos
escaneo_firmas = []       
with scandir('Archivos_XLSX_FirmasEspectrales') as ficheros:
        for fichero in ficheros:
            escaneo_firmas.append(fichero.name)
escaneo_firmas.remove('Consolidado_SpectralFirms.xlsx')

# print(escaneo_firmas)

# # Definir dataframe para almacenar datos
df_almacenamiento = DataFrame()
lista_c1_df = [] # Lista para almacenar el nombre, fecha y variedad del indice
lista_c2_df = [] # Lsita para almacenar el indice

# ----------------------------- CÁLCULO ÍNDICES ESPECTRALES ----------------------------------

print("Loading.... Iniciando cálculo de Índices Espectrales")
sleep(1)
    
for i in range(len(escaneo_firmas)):
    ruta_archivo = f'Archivos_XLSX_FirmasEspectrales/{escaneo_firmas[i]}'
    df_reflectancia = read_excel(ruta_archivo, index_col=False)

    longitudes_onda = df_reflectancia['longitud_onda'].tolist()
    reflectancia_promedio = df_reflectancia['reflect_med'].tolist()

    # Cálculo NDVI = (NIR - RED) / (NIR + RED)
    # --------- NIR entre 780 y 900
    # --------- NIR2 entre 850 y 870
    # --------- RED entre 650 Y 680
    # --------- BLUE entre 450 Y 520
    # --------- GREEN entre 540 y 570
    
    lista_nir = []
    lista_nir2 = []
    lista_red = []
    lista_blue = []
    lista_green = []
    
    for j in range(len(longitudes_onda)):
        # Banda BLUE
        if longitudes_onda[j] >= 450 and longitudes_onda[j] <= 520:
            lista_blue.append(reflectancia_promedio[j])
        # Banda RED
        elif longitudes_onda[j] >= 650 and longitudes_onda[j] <= 680:
            lista_red.append(reflectancia_promedio[j])
        # Banda NIR
        elif longitudes_onda[j] >= 780 and longitudes_onda[j] <= 900:
            lista_nir.append(reflectancia_promedio[j])
                    
    for k in range(len(longitudes_onda)):
        # Banda GREEN
        if longitudes_onda[k] >= 540 and longitudes_onda[k] <= 570:
             lista_green.append(reflectancia_promedio[k])
        # Banda NIR2
        elif longitudes_onda[k] >= 850 and longitudes_onda[k] <= 870:
            lista_nir2.append(reflectancia_promedio[k])
  
    promedio_nir = mean(lista_nir)
    promedio_red = mean(lista_red)
    nir = (promedio_nir-promedio_red)/(promedio_nir+promedio_red)
    
    
    print("\n[",str(round(100*(i+1)/len(escaneo_firmas),2)),f'% ] Calculando Índices Espectrales {escaneo_firmas[i][:-5]}...')
    sleep(1)
    
    lista_c1_df.append(f'NIR {escaneo_firmas[i][:-5]}')
    lista_c2_df.append(nir)
    
    print("--",str(round(100*1/6,2)),f'% NDVI {escaneo_firmas[i][:-5]}: ', nir)

    # Cálculo EVI = (2.5*(NIR-RED)) / (NIR + 6*RED - 7.5*BLUE + 1)   
    promedio_blue = mean(lista_blue)
    evi = 2.5*((promedio_nir-promedio_red) / (promedio_nir + 6*promedio_red - 7.5*promedio_blue + 1))    
    # print(promedio_blue)
    
    lista_c1_df.append(f'EVI {escaneo_firmas[i][:-5]}')
    lista_c2_df.append(evi)
        
    print("--",str(round(100*2/6,2)),f'% EVI {escaneo_firmas[i][:-5]}: ', evi)
    
    # Cálculo SAVI = (NIR-RED) / (NIR+RED+0.428) * 1.428
    savi = (promedio_nir-promedio_red)/(promedio_nir+promedio_red+0.428)*1.428
    
    lista_c1_df.append(f'SAVI {escaneo_firmas[i][:-5]}')
    lista_c2_df.append(savi)
    
    print("--",str(round(100*3/6,2)),f'% SAVI {escaneo_firmas[i][:-5]}: ', savi)
   
    
    # Cálculo CARI = CAR * (r_700/r_670)
    # ----- CAR = ABS(a*670 + r_670 + b) / (a^2 + 1)^0.5
    # ----- a = (r_700 - r_500) / 150
    # ----- b = r_550 - (a*550)
    r_500 = reflectancia_promedio[longitudes_onda.index(500)]
    r_550 = reflectancia_promedio[longitudes_onda.index(550)]
    r_670 = reflectancia_promedio[longitudes_onda.index(670)]
    r_700 = reflectancia_promedio[longitudes_onda.index(700)]
    a = (r_700-r_500)/150
    b = r_550-(a*550)
    car = abs((a*670) + r_670 + b)/pow(pow(a,2)+1,0.5)
    cari = car*(r_700/r_670)
    
    lista_c1_df.append(f'CARI {escaneo_firmas[i][:-5]}')
    lista_c2_df.append(cari)
    
    print("--",str(round(100*4/6,2)),f'% CARI {escaneo_firmas[i][:-5]}: ', cari)
    
    # Cálculo MCARI = 1.5*(2.5*(r_800 - r_670) - 1.3*(r_800 - r_550)) / SQRT((2*r_800 + 1)^2 - (6*r_800 - 5*r_670) - 0.5)
    r_800 = reflectancia_promedio[longitudes_onda.index(800)]
    mcari = (1.5*(2.5*(r_800 - r_670) - 1.3*(r_800 - r_550))) / sqrt((2*r_800 + 1)**2 - (6*r_800 - 5*r_670) - 0.5)
    
    lista_c1_df.append(f'MCARI {escaneo_firmas[i][:-5]}')
    lista_c2_df.append(mcari)
    
    print("--",str(round(100*5/6,2)),f'% MCARI {escaneo_firmas[i][:-5]}: ', mcari)
    
    # Cálculo GCI = (NIR2 / GREEN) - 1
    promedio_nir2 = mean(lista_nir2)
    promedio_green = mean(lista_green)
    gci = (promedio_nir2 - promedio_green) - 1
    
    lista_c1_df.append(f'GCI {escaneo_firmas[i][:-5]}')
    lista_c2_df.append(gci)
    
    print("--",str(round(100*6/6,2)),f'% GCI {escaneo_firmas[i][:-5]}: ', gci)

# Asignar columnas al dataframe
df_almacenamiento['indice/fecha/variedad'] = lista_c1_df
df_almacenamiento['valor'] = lista_c2_df

# Exportación del dataFrame
mkdir('Cálculo de Índices Espectrales')
df_almacenamiento.to_excel('Cálculo de Índices Espectrales/indices_espectrales.xlsx', index=False)

# print(df_almacenamiento)

sleep(2)
print("\nEjecución exitosa!")
print("Se ha creado el directorio 'Cálculo de Índices Espectrales'")  
print("\nPresione ENTER para finalizar...")
input()  
   
