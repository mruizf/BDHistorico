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

#%matplotlib inline

# Conectar a la base de datos
conn = sqlite3.connect("historicoFibras.db")

# Leer la tabla de fibras
fibras = pd.read_sql_query("SELECT * FROM fibras", conn)
fibras.head()

# Por ejemplo, queremos analizar la FIBRA "FUNO11"
nombre_fibra = "FMTY14"
periodo_dias = 30

class CONS:
    timestamp = 'timestamp' 
    dt_exdiv  = 'fecha_ex_dividendo'
    dt_pago   = 'fecha_pago'
    fecha     = 'fecha'
    nombre    = 'nombre'
    id_fibra  = 'id_fibra'
    open      = 'open'
    high      = 'high'
    low       = 'low'
    close     = 'close'
    media     = 'media'

# Obtener su id_fibra
id_fibra = fibras.loc[fibras[CONS.nombre] == nombre_fibra, CONS.id_fibra].values[0]
print(f"ID de {nombre_fibra}: {id_fibra}")

query = f"SELECT * FROM velas WHERE id_fibra = {id_fibra} AND frecuencia='1D'"
df_velas = pd.read_sql_query(query, conn)

df_velas[CONS.fecha] = pd.to_datetime(df_velas[CONS.timestamp], unit='s')
df_velas = df_velas.sort_values(CONS.timestamp)
df_velas.head()


df_velas[CONS.media] =df_velas[[CONS.open,CONS.high,CONS.low,CONS.close]].mean(axis=1)

query=f"SELECT * FROM distribuciones WHERE id_fibra = {id_fibra}"
df_dist = pd.read_sql_query(query, conn)
df_dist = df_dist.sort_values(CONS.dt_exdiv)
df_dist[CONS.dt_exdiv]=df_dist[CONS.dt_exdiv].astype('Int64')
df_dist[CONS.dt_pago]=df_dist[CONS.dt_pago].astype('Int64')

conn.close()



diasEspera={} #Diccionario para guardar la distrubucion de los dias de espera
fechas_exdiv_procesadas=set()
for indx,row in df_dist.iterrows():
    tms_div = row[CONS.dt_exdiv] 
    
    idx = df_velas[CONS.timestamp].searchsorted(tms_div)
    print ("Indice:",idx)
    if idx > 0 :
        if df_velas[CONS.timestamp][idx] == tms_div:
            vela_preex = df_velas.iloc[idx-1]
        else:
            dia = datetime.fromtimestamp(tms_div).strftime('%Y-%m-%d %A')
            print('No existe una vela con timestamp:',tms_div," ",dia)
            
            dias_anteriores =df_velas[df_velas[CONS.timestamp]<tms_div]
            if not dias_anteriores.empty :
                idx_ultimo = dias_anteriores[CONS.timestamp].idxmax()
                vela_preex =df_velas.iloc[idx_ultimo-1]
            else:
                print("Nada que hacer")    
                break
    else:
        continue
    
    #precio_pre_ex = vela_preex[CONS.close]
    precio_pre_ex = vela_preex[CONS.media]
    precio_ajustado = precio_pre_ex*(1+0.005*1.16) # precio ajustado con comisiones e iva de comisiones
    
    for i in range(idx+1,len(df_velas)):
        vela = df_velas.iloc[i]        
        #if vela[CONS.close] >= precio_ajustado : #precio_pre_ex:
        if vela[CONS.media] >= precio_ajustado :
            dias = (vela[CONS.timestamp]-tms_div)/86400
            if dias < periodo_dias:
                if dias in diasEspera:
                    diasEspera[dias]+=1
                else:
                    diasEspera[dias]=1
            else:
                if periodo_dias in diasEspera:
                    diasEspera[periodo_dias]+=1
                else:
                    diasEspera[periodo_dias]=1
            diastr = datetime.fromtimestamp(tms_div,tz=timezone.utc).strftime('%Y-%m-%d %A')
            print(diastr, " ", tms_div)
            break
    else:
        diastr = datetime.fromtimestamp(tms_div,tz=timezone.utc).strftime('%Y-%m-%d %A')
        print("Ya llegue al final con esta fecha:",diastr)
        if periodo_dias in diasEspera:
            diasEspera[periodo_dias]+=1
        else:
            diasEspera[periodo_dias]=1
        
#end for

keys = [int(k) for k in diasEspera.keys()]
values = [int(k) for k in diasEspera.values()]

print ("Media: " , st.mean(values))
print ("Desv. std.: " , st.variance(values))

# Graficamos
plt.bar(keys, values)
plt.xlabel('Categorías')
plt.ylabel('Valores')
plt.title('Dias espera para superar valor fecha pre-ex-derecho '+nombre_fibra)
plt.show()


    
#ya lo tengo calculado en var
#df_velas['retorno_diario'] = df_velas['close'].pct_change() 

# log_hl = np.log(df_velas[high_col] / df_velas[low_col])
# log_co = np.log(df_velas[close_col] / df_velas[open_col])

# df_velas['vol_Parkinson'] =df_velas['close']
# df_velas['vol_GK'] =


#df_dist['fecha_pago_str'] = pd.to_datetime(df_dist['fecha_pago'], unit='s')



# diasAño = np.zeros(366)


# for _,row in df_dist.iterrows():
#     valores = row
#     dia_año =  pd.to_datetime(valores['fecha_ex_dividendo'],unit='s').timetuple().tm_yday
#     print(dia_año)
#     diasAño[dia_año-1]+=1
    
#     fecha_exdiv_sec = fecha valores['fecha_ex_dividendo']
#     fecha_antes_exdiv = pd.to_datetime(fecha_exdiv_sec,unit='s') -pd.Timedelta(days=1)
#     fechas_posteriores = df_velas[df_velas['fecha']>=fecha_exdiv_sec]
    
#     precio_antes_exdiv = fechas_posteriores['close'][0]
    
    

    




# for _,row in df_dist.iterrows():
#     valores = row
#     dia_año =  pd.to_datetime(valores['fecha_pago'],unit='s').timetuple().tm_yday
#     print(dia_año)
#     diasAño[dia_año-1]+=1
    
    
# # Graficar el vector en 2D (como un plot de línea)
# plt.figure(figsize=(10, 2)) #10,2 son tamaño de la imagen en pulgadas
# plt.plot(range(len(diasAño)), diasAño) # Cambiado de scatter a plot
# plt.title('Vector en 2D (Plot de Línea)')
# plt.xlabel('Índice')
# plt.ylabel('Valor')
# plt.show()
    
    



