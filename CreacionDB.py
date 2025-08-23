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
FIBRAS : List[str] = ["DANHOS13",
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


DBNAME:str       ="historicoFibras.db"
SCHEMAFILE:str   ="schema.sql"

EXCEL_FILE_DIVIDENDOS:str ="Historico de Fibras.xlsx"
EXCEL_FILE_VELAS_DIARIAS:str ="HistoricoVelasDesde2024.xlsx"

CREATE_DATABASE = True
INSERTAR_FIBRAS:bool = True
INSERTAR_DISTRIBUCIONES:bool =True
INSERTAR_VELAS:bool =True



def create_db() -> NoReturn:
    if not os.path.exists(DBNAME):
        print("Base de datos no encontrada. Creando nueva...")
        conn = sqlite3.connect(DBNAME)
        cursor = conn.cursor()

        with open(SCHEMAFILE, "r", encoding="utf-8") as f:
            schema = f.read()
            cursor.executescript(schema)

        conn.commit()
        conn.close()
        print("Base de datos creada con éxito.")
    else:
        print("La base de datos ya existe, no se modificó.")




if __name__=="__main__":

    if CREATE_DATABASE:
        create_db()
        
    if INSERTAR_FIBRAS:
        for fibra in FIBRAS:
            print(f"Fibra:{fibra}")
            #aqui vamos a insertar las velas
            with sqlite3.connect(DBNAME) as conn:
                insert = qu.InsertNewFibra(fibra)
                insert.execute(conn)
    
    if INSERTAR_VELAS:
        hojas:dict[str,pd.DataFrame] = pd.read_excel(EXCEL_FILE_VELAS_DIARIAS, sheet_name=None)        
    
        for fibra in FIBRAS:
            print(f"Fibra:{fibra}")
            
            if fibra in hojas:
                dft = hojas[fibra]
                with sqlite3.connect(DBNAME) as conn:
                    print("Guardando la hoja"+fibra)
    
                    select = qu.GetFibraID(fibra)
                    id_fibra = select.execute(conn)
                    
                        
                    print("Ahora insertamos las velas")
                    for index,row in dft.iterrows():
                        valoresRaw = qu.BuildOriginalDataRow(id_fibra,row)
                        insertVela = qu.InsertVela(valoresRaw)
                        insertVela.execute(conn)
                    conn.commit()
                print(f"Fibra '{fibra}' insertada con éxito.")



    if INSERTAR_DISTRIBUCIONES:
        hojas:dict[str,pd.DataFrame] = pd.read_excel(EXCEL_FILE_DIVIDENDOS, header=1,sheet_name=None)
        
        for fibra in FIBRAS:
            print(f"Fibra:{fibra}")
            if fibra in hojas:
                dft = hojas[fibra]
                with sqlite3.connect(DBNAME) as conn:
                    print("Guardando la hoja distribucion"+fibra)
                                        
                    select = qu.GetFibraID(fibra)
                    id_fibra= select.execute(conn)
                    
                    print("Ahora insertamos las distribuciones")
                    
                    for index,row in dft.iterrows():
                        #variables temporales
                        valores = row
                        valores[qu.EXC_DIV.FECHA_PAGO]=int(row[qu.EXC_DIV.FECHA_PAGO].timestamp())
                        valores[qu.EXC_DIV.FECHA_EX_DIV]=int(row[qu.EXC_DIV.FECHA_EX_DIV].timestamp())
                        valores[qu.EXC_DIV.ID_FIBRA]=id_fibra
                        
                        #insertamos en la BD
                        insertDividendo = qu.InsertDividendo(valores)
                        insertDividendo.execute(conn)
                    
                    conn.commit()
                print(f"Fibra '{fibra}' insertada con éxito.")

    print(conn.close())