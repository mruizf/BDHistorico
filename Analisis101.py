# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 17:29:21 2025

@author: M R
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from datetime import datetime,timezone
from typing import Dict

class FIBRAS:
    nombre    = 'nombre'
    id_fibra  = 'id_fibra'
    nameFileDB= "historicoFibras.db"

class VELAS:
    timestamp = 'timestamp'
    open      = 'open'
    high      = 'high'
    low       = 'low'
    close     = 'close'
    media     = 'media'
    fecha     = 'fecha'

class DIST:
    dt_exdiv  = 'fecha_ex_dividendo'
    dt_pago   = 'fecha_pago'

FIBRA_FREC : Dict[str,int] = {"DANHOS13":90,
                          "FUNO11":90,
                          "FMTY14":30,
                          "FNOVA17":90,
                          "FINN13":90,
                          "FIHO12":90,
                          "FCFE18":90,
                          "FIBRAMQ12":90,
                          "FIBRAPL14":90,
                          "FSHOP13":90,
                          "FPLUS16":90,
                          "TERRA13":90,
                          "FHIPO14":90}

# Por ejemplo, queremos analizar la FIBRA "FUNO11"
#PARAMETROS
class CONFIG:
    nombre_fibra:str = "FIBRAMQ12"
    periodo_dias:int = FIBRA_FREC[nombre_fibra]
    ganancia:float = 0.006 # ganancia para agregar al precio anterior ex-derecho

def cargarDataFramesFromDB(nombre_fibra:str):
    # Conectar a la base de datos
    conn = sqlite3.connect(FIBRAS.nameFileDB)

    # Leer la tabla de fibras
    fibras = pd.read_sql_query("SELECT * FROM fibras", conn)
    
    # Obtener su id_fibra
    id_fibra = fibras.loc[fibras[FIBRAS.nombre] == nombre_fibra, FIBRAS.id_fibra].values[0]
    print(f"ID de {nombre_fibra}: {id_fibra}")
    
    query = f"SELECT * FROM velas WHERE id_fibra = {id_fibra} AND frecuencia='1D'"
    velas = pd.read_sql_query(query, conn)
    
    query=f"SELECT * FROM distribuciones WHERE id_fibra = {id_fibra}"
    dist = pd.read_sql_query(query, conn)
    
    conn.close()

    return dist,velas


if __name__=="__main__":
    
    df_dist,df_velas = cargarDataFramesFromDB(CONFIG.nombre_fibra)

    df_velas[VELAS.fecha] = pd.to_datetime( df_velas[VELAS.timestamp], unit='s')
    df_velas = df_velas.sort_values(VELAS.timestamp)

    df_dist = df_dist.sort_values(DIST.dt_exdiv)
    #df_dist[CONSDIST.dt_exdiv]=df_dist[CONSDIST.dt_exdiv].astype('Int64')
    #df_dist[CONSDIST.dt_pago]=df_dist[CONSDIST.dt_pago].astype('Int64')

    df_velas[VELAS.media] =df_velas[[VELAS.open,VELAS.high,VELAS.low,VELAS.close]].mean(axis=1)

    diasEspera={} #Diccionario para guardar la distrubucion de los dias de espera
    for indx,row in df_dist.iterrows():
        tms_div = row[DIST.dt_exdiv] 
        
        #searchsorted sin parametros adicionales nos da la posicion idx donde deberia
        #ir insertado el valor buscado, que tambien es la posición del primer elemento
        #mayor al que buscamos, por lo tando idx-1 es un valor menor y por tanto la primera
        #fecha pre ex derecho
        # Asi que sin imiportar si la fecha esta o no en las velas, la posicion de la 
        # fecha previa ex derecho es idx-1, si el valor es mucho mayor que 
        idx = df_velas[VELAS.timestamp].searchsorted(tms_div)
        print ("Indice:",idx)
        if idx > 0  and idx < len(df_velas) :
            print("Vela:",df_velas.iloc[idx][VELAS.timestamp],"  dist:",tms_div)
            vela_preex = df_velas.iloc[idx-1]
            if (row[DIST.dt_exdiv] != df_velas.iloc[idx][VELAS.timestamp]):
                dia = datetime.fromtimestamp(tms_div).strftime('%Y-%m-%d %A')
                print('No existe una vela con timestamp:',tms_div," ",dia)
        else:
            print("""Estamos fuera de rango, no podemos buscar un precio a fecha previa ex derecho 
                  o no tenemos valores despues de fecha ex derecho.
                  """)
            continue
        
        #precio_pre_ex = vela_preex[CONS.close]
        precio_pre_ex = vela_preex[VELAS.media]
        dia_preex = vela_preex[VELAS.timestamp]
        
        precio_ajustado = precio_pre_ex*(1+CONFIG.ganancia+0.005*1.16) # precio ajustado con comisiones e iva de comisiones
        for i in range(idx,len(df_velas)):
            vela = df_velas.iloc[i]        
            #if vela[CONS.close] >= precio_ajustado : #precio_pre_ex:
            if vela[VELAS.media] >= precio_ajustado :
                
                dias = (vela[VELAS.timestamp]-dia_preex)/86400 #86400 = segundos en un dia
                dias = min(dias,CONFIG.periodo_dias)
                
                if dias in diasEspera:
                    diasEspera[dias]+=1
                else:
                    diasEspera[dias]=1
                
                diastr = datetime.fromtimestamp(tms_div,tz=timezone.utc).strftime('%Y-%m-%d %A')
                print(diastr, " ", tms_div)
                break
        else:#for
            diastr = datetime.fromtimestamp(tms_div,tz=timezone.utc).strftime('%Y-%m-%d %A')
            print("Ya llegue al final con esta fecha:",diastr)
            if CONFIG.periodo_dias in diasEspera:
                diasEspera[CONFIG.periodo_dias]+=1
            else:
                diasEspera[CONFIG.periodo_dias]=1
            
    #end for
    
    keys = [int(k) for k in diasEspera.keys()]
    values = [int(k) for k in diasEspera.values()]
    
    print ("Media: " , st.mean(values))
    print ("Desv. std.: " , st.variance(values))
    
    # Graficamos
    plt.bar(keys, values)
    plt.xlabel('Categorías')
    plt.ylabel('Valores')
    plt.title('Dias espera para superar valor fecha pre-ex-derecho '+CONFIG.nombre_fibra)
    plt.show()
    
