# -*- coding: utf-8 -*-

#Vamos a hacer un script que lea la base de datos de distribuciones y genere un mapa
#de calor de posibles fechas de pago. Que se  interactivo de ser posible

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

class CONSFIBRAS:
    nombre    = 'nombre'
    id_fibra  = 'id_fibra'
    nameFileDB= "historicoFibras.db"

class CONSVELAS:
    timestamp = 'timestamp'
    open      = 'open'
    high      = 'high'
    low       = 'low'
    close     = 'close'
    media     = 'media'
    fecha     = 'fecha'

class CONSDIST:
    dt_exdiv  = 'fecha_ex_dividendo'
    dt_pago   = 'fecha_pago'


def cargarDatosDistribuciones():
    # Conectar a la base de datos
    conn = sqlite3.connect(CONSFIBRAS.nameFileDB)
    
    # Leer la tabla de fibras
    fibras = pd.read_sql_query("SELECT * FROM fibras", conn)
    
    # Lees la tabla de distribuciones
    dist = pd.read_sql_query("SELECT * FROM distribuciones", conn)
    
    conn.close()

    return fibras,dist



if __name__=="__main__":
    #fibras que queremos ver
    FIBRAS_USADAS = ["DANHOS13","FUNO11","FMTY14","FIBRAMQ12","FIBRAPL14","FNOVA17"]
    
    df_fibras,df_distribuciones = cargarDatosDistribuciones()
    
    acumulado = np.zeros(366)

    df_distribuciones["diaAnio"] = pd.to_datetime(df_distribuciones[CONSDIST.dt_exdiv]).dt.dayofyear
    
    for it_name_fibra in FIBRAS_USADAS:
        
        #obtenemos el id de la fibra
        df_fila = df_fibras[df_fibras[CONSFIBRAS.nombre] == it_name_fibra]
        id_fibra = df_fila[CONSFIBRAS.id_fibra].iloc[0]

        #filtramos por id de la fibra
        df_distribucion_fibra = df_distribuciones[df_distribuciones[CONSFIBRAS.id_fibra] == id_fibra]
        dias_del_anio = pd.to_datetime(df_distribucion_fibra[CONSDIST.dt_exdiv],unit='s').dt.dayofyear
        
        acumulado[dias_del_anio]+=1
        acumulado[(dias_del_anio-1) % 366]+=0.7
        acumulado[(dias_del_anio+1) % 366]+=0.7
        acumulado[(dias_del_anio-2) % 366]+=0.1
        acumulado[(dias_del_anio+2) % 366]+=0.1
        
        
            
    # #Graficamos 
    # plt.figure(figsize=(12, 2))
    # plt.imshow(acumulado.reshape(1, -1), cmap="hot", aspect="auto")
    # plt.colorbar(label="Intensidad de fechas ex-dividendo")
    # plt.yticks([])
    # plt.xlabel("Día del año")
    # plt.show()
    
       
    df_final =pd.DataFrame({
                'dia_del_año': range(1, 367),
                'conteo': acumulado
    })
    
    # 2. Generar la columna de fechas completas para el tooltip
    df_final['fecha_completa'] = pd.to_datetime(df_final['dia_del_año'] - 1, unit='D', origin='2025-01-01')
    
    # 3. Generar el mapa de calor unidimensional con Plotly
    fig = go.Figure( data=go.Heatmap(
    z=[df_final['conteo']],
    y=['Conteo de Eventos'],
    x=df_final['dia_del_año'],
    colorscale='Viridis',
    hovertemplate="<b>Día:</b> %{x}<br><b>Fecha:</b> %{customdata}<br><b>Conteo:</b> %{z}<extra></extra>",
    
    customdata=[df_final['fecha_completa'].dt.strftime('%d-%b')]
    ))

    # Personalizar el diseño del gráfico
    fig.update_layout(
        title='Mapa de Calor de Eventos (1D)',
        xaxis_title='Día del Año (1-366)',
        yaxis_title=''
    )
    
    fig.show()

#end main        
        
    