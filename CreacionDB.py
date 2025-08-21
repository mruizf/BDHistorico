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


########################VARIABLES GLOBALES#############################
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

create_database = True
insertar_fibras:bool = True
insertar_distribuciones:bool =True
insertar_velas:bool =True



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

    if create_database:
        create_db()
        
    if insertar_fibras:
        for fibra in fibras:
            print(f"Fibra:{fibra}")
            #aqui vamos a insertar las velas
            with sqlite3.connect(dbName) as conn:
                insert = qu.InsertNewFibra(fibra)
                insert.execute(conn)
    
    if insertar_velas:
        hojas:dict[str,pd.DataFrame] = pd.read_excel("HistoricoVelasDesde2024.xlsx", sheet_name=None)        
    
        for fibra in fibras:
            print(f"Fibra:{fibra}")
            
            if fibra in hojas:
                dft = hojas[fibra]
                with sqlite3.connect(dbName) as conn:
                    print("Guardando la hoja"+fibra)
    
                    select = qu.GetFibraID(fibra)
                    resultado = select.execute(conn)
                    
                    if resultado:  
                        id_fibra = resultado[0][0]   # fetalldone devuelve una lista de tuplas
                        print("El id_fibra es:", id_fibra)
                    else:
                        print("No se encontró la fibra")
                        
                    print("Ahora insertamos las velas")
                                
                    columnNames= list(dft.columns.values)
                    for index,row in dft.iterrows():
                        temp = row["Vol."]
                        volume=-1
                        if (temp[-1]=="K"):
                            volume = float(temp[0:-1])*1000
                        elif (temp[-1]=="M"):
                            volume = float(temp[0:-1])*1000000
                        else:
                            print("Posfijo inesperado: "+temp)
                        
                        #volume:float  = temp
                        #var:float = row["% var."]
                                            
                        
                        #insertamos en la BD
                        valores = row
                        valores["Fecha"]=int(row["Fecha"].timestamp())
                        valores["Vol."]=volume
                        valores["id_fibra"]=id_fibra
                        valores["frecuencia"]="1D"
                        
                        insertVela = qu.InsertVela(valores)
                        insertVela.execute(conn)
                    conn.commit()
                print(f"Fibra '{fibra}' insertada con éxito.")



    if insertar_distribuciones:
        hojas:dict[str,pd.DataFrame] = pd.read_excel("Historico de Fibras.xlsx", header=1,sheet_name=None)
        
        for fibra in fibras:
            print(f"Fibra:{fibra}")
            if fibra in hojas:
                dft = hojas[fibra]
                with sqlite3.connect(dbName) as conn:
                    print("Guardando la hoja distribucion"+fibra)
                                        
                    select = qu.GetFibraID(fibra)
                    resultado = select.execute(conn)
        
                    id_fibra=-1
                    if resultado:  
                        id_fibra = resultado[0][0]   # fetalldone devuelve una lista de tuplas
                        print("El id_fibra es:", id_fibra)
                    else:
                        print("No se encontró la fibra")
                    
                    print("Ahora insertamos las distribuciones")
                    
                    for index,row in dft.iterrows():
                        #variables temporales
                        valores = row
                        valores["Fecha de pago"]=int(row["Fecha de pago"].timestamp())
                        valores["Fecha ex-dividendo"]=int(row["Fecha ex-dividendo"].timestamp())
                        valores["id_fibra"]=id_fibra
                        
                        #insertamos en la BD
                        insertDividendo = qu.InsertDividendo(valores)
                        insertDividendo.execute(conn)
                    
                    conn.commit()
                print(f"Fibra '{fibra}' insertada con éxito.")

    print(conn.close())