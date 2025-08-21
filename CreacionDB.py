# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 22:22:25 2025

@author: M R
"""

import pandas as pd
import sqlite3
import os
from typing import List,NoReturn
import queries as qu

fibras : List[str] = ["DANHOS13",
                    "FUNO11",
                    "FMTY14",
                    "FNOVA17",
                    "FINN13",
                    "FIHO12",
                    "FCFE18",
                    "FIBRAMQ12",
                    "FIBRAPL14",
                    "FSHOP13",
                    "FPLUS16",
                    "TERRA13",
                    "FHIPO14"]


dbName:str       ="historicoFibras.db"
schemaFile:str   ="schema.sql"


def create_db() -> NoReturn:
    if not os.path.exists(dbName):
        print("Base de datos no encontrada. Creando nueva...")
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()

        with open(schemaFile, "r", encoding="utf-8") as f:
            schema = f.read()
            cursor.executescript(schema)

        conn.commit()
        conn.close()
        print("Base de datos creada con éxito.")
    else:
        print("La base de datos ya existe, no se modificó.")


if __name__=="__main__":

    create_db()
    
    hojas:dict[str,pd.DataFrame] = pd.read_excel("HistoricoVelasDesde2024.xlsx", sheet_name=None)        

    for fibra in fibras:
        print(f"Fibra:{fibra}")
        
        if fibra in hojas:
            dft = hojas[fibra]
            with sqlite3.connect(dbName) as conn:
                print("Guardando la hoja"+fibra)
                
                #aqui vamos a insertar las velas
                insert = qu.InsertNewFibra(fibra)
                insert.execute(conn)

                select = qu.GetFibraID(fibra)
                resultado = select.execute(conn)
                
                if resultado:  
                    id_fibra = resultado[0][0]   # fetalldone devuelve una lista de tuplas
                    print("El id_fibra es:", id_fibra)
                else:
                    print("No se encontró la fibra")
                    
                print("Ahora insertamos las distribuciones")
                            
                for index,row in dft.iterrows():
                    #variables temporales
                    timestamp:int =int(row["Fecha"].timestamp())
                    open:float    = row["Apertura"]
                    high:float    = row["Máximo"]
                    low:float     = row["Mínimo"]
                    close:float   = row["Cierre"]
                    
                    temp = row["Vol."]
                    if (temp[-1]=="K"):
                        temp = float(temp[0:-1])*1000
                    elif (temp[-1]=="M"):
                        temp = float(temp[0:-1])*1000000
                    else:
                        print("Posfijo inesperado: "+temp)
                    
                    volume:float  = temp
                    var:float = row["% var."]
                                        
                    #insertamos en la BD
                    insertVela = qu.InsertVela(id_fibra,timestamp,
                                                    open,high,low,close,
                                                    volume,var,"1D")
                    insertVela.execute(conn)
                conn.commit()
            print(f"Fibra '{fibra}' insertada con éxito.")

    # hojas:dict[str,pd.DataFrame] = pd.read_excel("Historico de Fibras.xlsx", header=1,sheet_name=None)
    
    # for fibra in fibras:
    #     print(f"Fibra:{fibra}")
    #     if fibra in hojas:
    #         dft = hojas[fibra]
    #         with sqlite3.connect(dbName) as conn:
    #             print("Guardando la hoja"+fibra)
                
    #             #cursor.execute("insert into fibras (nombre) values (?)",(fibra,))
    #             insert = qu.InsertNewFibra(fibra)
    #             insert.execute(conn)
                
    #             select = qu.GetFibraID(fibra)
    #             resultado = select.execute(conn)
    
    #             id_fibra=-1
    #             if resultado:  
    #                 id_fibra = resultado[0][0]   # fetalldone devuelve una lista de tuplas
    #                 print("El id_fibra es:", id_fibra)
    #             else:
    #                 print("No se encontró la fibra")
                
    #             print("Ahora insertamos las distribuciones")
                
    #             for index,row in dft.iterrows():
    #                 #variables temporales
    #                 fecha_pago:int        =int(row["Fecha de pago"].timestamp())
    #                 fecha_ex_dividendo:int=int(row["Fecha ex-dividendo"].timestamp())
    #                 tipo_dividendo:str    =row["Tipo"]
    #                 dividendo:float       =row["Dividendo"]
    #                 rendimiento:float     =row["Rendimiento"]
    #                 #insertamos en la BD
    #                 insertDividendo = qu.InsertDividendo(id_fibra,fecha_pago,fecha_ex_dividendo,tipo_dividendo,dividendo,rendimiento)
    #                 insertDividendo.execute(conn)
                
    #             conn.commit()
    #         print(f"Fibra '{fibra}' insertada con éxito.")

