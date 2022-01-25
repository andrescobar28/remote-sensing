# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:20:10 2022

@author1: ANDRES JULIAN ESCOBAR CARDONA - Correo: andres.julian.escobar@correounivalle.edu.co
@author2: EDUARDO TAMAYO CORDOBA - Correo: eduardo.tamayo@correounivalle.edu.co
@author3: VALENTINA SEVILLANO RAMIREZ - Correo: valentina.sevillano@correounivalle.educ.o
@author4: LIZETH CATHERINE CARDENAS ALVARADO - Correo: lizeth.cardenas@correounivalle.edu.co

UNIVERSIDAD DEL VALLE - INGENIERÍA TOPOGRÁFICA
2022-1

OBJETIVO DEL SCRIPT:
Generar compilado en formato de texto separado por coma para N cantidad de firmas espectrales
correspondientes a M cantidad de variedades de un cultivo de caña de azúcar.

SOLICITADO POR: CESAR EDWIN GARCIA CORTES - Correo: cesar.edwin.garcia@correounivalle.edu.co
Ingeniero Topográfico - Magister en Percepción Remota
Docente Curso TELEDETECCIÓN ESPACIAL

"""

# ----------------------- Importación de librerías y módulos -------------------------
import csv # Libreria para conversión de dataFrame a TXT
from os import scandir, mkdir # Manipulación de archivos del sistema
from pandas import DataFrame, read_table # Manejo de dataframes

# ----------------------- FUNCIONES -------------------------------
def extraccion_datos(archivo):
    """

    Parameters
    ----------
    archivo : STRING DIRECTORY
        Corresponde a la ruta del archivo de donde se desean extraer los datos.

    Returns
    -------
    lista_ancho_banda2float : LIST TYPE FLOAT
        Lista que contiene los anchos de banda.
    lista_reflectancia2float : LIST TYPE FLOAT
        Lista que contiene los valores de reflectancia

    """
    
    dataframe = read_table(archivo,header=None,sep=' ')
    
    # Selección de columnas "ancho banda" y "reflectancia"
    colum_dataframe = dataframe.iloc[:, [1,3]]
    
    # Eliminación de fila que contiene metadatos
    row_dataframe = colum_dataframe.drop([0],axis=0)
    # print(row_dataframe)
    
    #------------------ Manejo de datos ancho de banda ---------------
    # Conversión columna valor banda espectral a lista
    lista_ancho_banda = row_dataframe[1].tolist()
    # print(lista_ancho_banda)
    
    # Conversión a FLOAT de los valores de las bandas
    lista_ancho_banda2float = []
    for item in lista_ancho_banda:
        lista_ancho_banda2float.append(float(item))
        
    # print(lista_ancho_banda2float)
    
    #------------------ Manejo de datos reflectancia ---------------
    # Conversión columna reflectancia a lista
    lista_reflectancia = row_dataframe[3].tolist()
    # Eliminación de E+000 de cada elemento de lista_reflectancia
    
    lista_reflectancia2 = [ elem[:-5] for elem in lista_reflectancia ]
    #print(lista_reflectancia2)
    
    # Conversión a FLOAT de los valores de reflectancia
    lista_reflectancia2float = []
    for item in lista_reflectancia2:
        lista_reflectancia2float.append(float(item))
    
    # print(lista_reflectancia2float)
    return lista_ancho_banda2float, lista_reflectancia2float

#print(extraccion_datos("04-junio/011940/1.TRM")[1])  

def consolidacion_datos(directorio):
    """

    Parameters
    ----------
    directorio : STRING DIRECTORY
        Corresponde a la ruta de la carpeta que contiene las firmas espectrales.

    Returns
    -------
    consolidado_reflectancia : TYPE
        Matriz cuyo primer elemento son los valores de los anchos de banda espectral y
        las N filas restantes son los valores de reflectancia.

    """
    # Validación si los anchos de banda son iguales para todas las firmas
    consolidado_anchos_banda = []
    with scandir(directorio) as ficheros:
        for i in ficheros:
            consolidado_anchos_banda.append(extraccion_datos(i)[0])
    
    lista_set = set()
    for firma_espectral in consolidado_anchos_banda:
        lista_set = lista_set.union(set(firma_espectral))
    
    #print(lista_set)
    
    
    if len(lista_set) == len(consolidado_anchos_banda[0]):
        # Conformación de matriz final
        consolidado_reflectancia = []
        with scandir(directorio) as ficheros:
            for i in ficheros:
                consolidado_reflectancia.append(extraccion_datos(i)[1])
                
        return  consolidado_anchos_banda[0], consolidado_reflectancia
    else:
        return []
    
#print(consolidacion_datos("04-junio/011940"))   

def conversion2txt(ruta_inicial, ruta_final_extension):
    """

    Parameters
    ----------
    ruta_inicial : STRING DIRECTORY
        Corresponde a la ruta del archivo para la conversión.
    ruta_final_extension : TYPE
        Corresponde a la ruta del archivo de exportación.

    Returns
    -------
    None.

    """
    
    # Se define ruta a la carpeta
    ruta = ruta_inicial
    print(ruta)
    
    # Creación del dataFrame
    df_final = DataFrame() 
    
    # Se añade cada uno de los elementos al dataframe
    longitud_onda = consolidacion_datos(ruta)[0]
    reflectancia = consolidacion_datos(ruta)[1]
    
    # Se añade columna correspondiente al ancho de banda
    df_final['longitud_onda'] = longitud_onda
    
    # Se añaden columnas para cada una de las firmas espectrales
    for i in range(len(reflectancia)):
        df_final[f'firma{i+1}'] = reflectancia[i]
        
    # print(df_final)
    
    # Permite exportar el resultado del dataFrame en formato TXT
    df_final.to_csv(ruta_final_extension, sep=",",quoting=csv.QUOTE_NONE, escapechar=" ", index=False)
    
def lectura_directorios(ruta_lectura):
    """

    Parameters
    ----------
    ruta_lectura : STRING DIRECTORY
        Corresponde a la ruta de donde se desean conocer los directorios.

    Returns
    -------
    directorios : LIST
        Retorna una lista con el nombre de los directorios.

    """
    with scandir(ruta_lectura) as ficheros:
        directorios = [fichero.name for fichero in ficheros if fichero.is_dir()]
    return directorios


#------------------------ Creación de archivo TXT con el formato solicitado -----------

# Permite crear un directorio en donde se almacenarán los resultados TXT
try:
    # Se intenta crear el directorio de almacenamiento de dato
    mkdir('Archivos_TXT_FirmasEspectrales')
except:
    # Se valida que el usuario no tenga un directorio con el mismo nombre
    print("Ya existe un directorio de almacenamiento, \npor favor valide e intente nuevamente.")

# Se crea lista con los directorios
directorios = lectura_directorios('.')
print(directorios)

# Creación individual de cada archivo TXT
for i in range(len(directorios)):
    subdirectorios = lectura_directorios(f'{directorios[i]}')
    print(subdirectorios)

    for j in range(len(subdirectorios)):    
        sub_ruta1 = f'{subdirectorios[j]}'
        sub_ruta2 = f'{directorios[i]}'
        ruta_inicio = sub_ruta2+"/"+sub_ruta1
        ruta_fin = f'Archivos_TXT_FirmasEspectrales/{directorios[i]}_{sub_ruta1}.csv'
        conversion2txt(ruta_inicio, ruta_fin)

print("Ejecución exitosa! Presione enter para finalizar.")
input()
