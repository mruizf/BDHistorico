# -*- coding: utf-8 -*-
"""
Created on Sat Aug  2 20:23:41 2025

@author: M R
"""

#
#Script para descargar velas intradia de 30m y 60m de fibras. Y almacenarlas en 
#una base sqlite
#

import yfinance as yf
import typing as typ
import queries as qu
import sqlite3


l_fibras : typ.List[str] = ["DANHOS13.MX",
                            "FUNO11.MX",
                            "FMTY14.MX",
                            "FNOVA17.MX",
                            "FIHO12.MX",
                            "FCFE18.MX",
                            "FIBRAMQ12.MX",
                            "FIBRAPL14.MX",
                            "FHIPO14.MX"]
                            
                            
#Vamos a preparar la base de datos                             

dbName:str       ="historicoFibras.db"

for fibra in l_fibras:
    #df = yf.download(fibra, start, end,actions=True)
    
    df = yf.download(fibra, start="2025-08-20",end="2025-08-21", interval="30m",ignore_tz=True)
    df.to_csv(fibra[:-3]+"_30m.csv")
    
    
    with sqlite3.connect(dbName) as conn:
        select = qu.GetFibraID(fibra)
        resultado = select.execute(conn)
    
        if resultado:  
            id_fibra = resultado[0][0]   # fetalldone devuelve una lista de tuplas
            print("El id_fibra es:", id_fibra)
        else:
            print("No se encontró la fibra")
            
        print("Ahora insertamos las velas")
        
        df = yf.download(fibra, start="2025-08-20",end="2025-08-21", interval="60m",ignore_tz=True)
        for index,row in df.iterrows():
            print(row)
            valores = row
            insertVela = qu.InsertVela(valores)
            insertVela.execute(conn)

    
        #df.to_csv(fibra[:-3]+"_60m.csv")



# for fibra in l_fibras:
#     df = yf.download(fibra, period="1d", interval="30m")
    

#     df = yf.download(fibra, period="1d", interval="60m")