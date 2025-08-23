# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:12:44 2025

@author: M R
"""
import sqlite3

#Query Objects
#Usados para leer datos de una hoja de excel e insertarlos en la base sqlite
#Para mantener esto sencillo tendremos una hoja de calculo por cada tabla



class DB_DIV:
    ID_FIBRA    ="id_fibra"
    FECHA_EX_DIV="fecha_ex_dividendo"
    FECHA_PAGO  ="fecha_pago"
    TIPO        ="tipo_dividendo"
    DIVIDENDO   ="dividendo"
    RENDIMIENTO ="rendimiento"
class EXC_DIV:
    ID_FIBRA    ="id_fibra"
    FECHA_EX_DIV="Fecha ex-dividendo"
    FECHA_PAGO  ="Fecha de pago"
    TIPO        ="Tipo"
    DIVIDENDO   ="Dividendo"
    RENDIMIENTO ="Rendimiento"

DB_DIVIDENDOS_2_EXCEL={
    DB_DIV.ID_FIBRA    : EXC_DIV.ID_FIBRA,
    DB_DIV.FECHA_EX_DIV: EXC_DIV.FECHA_EX_DIV,
    DB_DIV.FECHA_PAGO  : EXC_DIV.FECHA_PAGO,
    DB_DIV.TIPO        : EXC_DIV.TIPO,
    DB_DIV.DIVIDENDO   : EXC_DIV.DIVIDENDO,
    DB_DIV.RENDIMIENTO : EXC_DIV.RENDIMIENTO
    }

class DB_VELAS:
    ID_FIBRA  ="id_fibra"
    TIMESTAMP ="timestamp"
    OPEN      ="open"
    HIGH      ="high"
    LOW       ="low"
    CLOSE     ="close"
    VOLUME    ="volume"
    VAR       ="var"
    FRECUENCIA="frecuencia"

class EXC_VELAS:
    ID_FIBRA  ="id_fibra"
    TIMESTAMP ="Fecha"
    OPEN      ="Apertura"
    HIGH      ="Máximo"
    LOW       ="Mínimo"
    CLOSE     ="Cierre"
    VOLUME    ="Vol."
    VAR       ="% var."
    FRECUENCIA="frecuencia"
    
DB_VELAS_2_EXCEL={
    DB_VELAS.ID_FIBRA  :EXC_VELAS.ID_FIBRA  ,
    DB_VELAS.TIMESTAMP :EXC_VELAS.TIMESTAMP ,
    DB_VELAS.OPEN      :EXC_VELAS.OPEN      ,
    DB_VELAS.HIGH      :EXC_VELAS.HIGH      ,
    DB_VELAS.LOW       :EXC_VELAS.LOW       ,
    DB_VELAS.CLOSE     :EXC_VELAS.CLOSE     ,
    DB_VELAS.VOLUME    :EXC_VELAS.VOLUME    ,
    DB_VELAS.VAR       :EXC_VELAS.VAR       ,
    DB_VELAS.FRECUENCIA:EXC_VELAS.FRECUENCIA}


def getColsAndPlaceholders(MapaLlaves)-> tuple[str ,str] :
    cols = ",".join(MapaLlaves.keys())
    placeholders = ",".join([f":{k}" for k in MapaLlaves.keys()])
    return cols,placeholders

def BuildOriginalDataRow(id_fibra,row):
    temp = row[EXC_VELAS.VOLUME]
    volume=-1
    if (temp[-1]=="K"):
        volume = float(temp[0:-1])*1000
    elif (temp[-1]=="M"):
        volume = float(temp[0:-1])*1000000
    else:
        print("Posfijo inesperado: "+temp)
    
    
    valores = row
    valores[EXC_VELAS.TIMESTAMP]=int(row[EXC_VELAS.TIMESTAMP].timestamp())
    valores[EXC_VELAS.VOLUME]=volume
    valores[EXC_VELAS.ID_FIBRA]=id_fibra
    valores[EXC_VELAS.FRECUENCIA]="1D"
    
    return valores


class QueryBase():
    SQL=""
    #mapa de objetos, cuyas llaves estan en el query en formato named parameters 
    #(parámetros con nombre)
    registro={}

    def execute(self,conn):
        """Ejecuta la query usando el conector dado"""
        cursor = conn.cursor()
        cursor.execute(self.SQL, self.registro)
        try:
            return cursor.fetchall()  # SELECT
        except (sqlite3.ProgrammingError, sqlite3.IntegrityError) as e:
            # para INSERT/UPDATE/DELETE que no devuelven resultados
            print("Error al lanzar la query:"+self.SQL+"---",e)
            return None

class InsertNewFibra(QueryBase):
    def __init__(self, nombre_fibra=""):
        #self.SQL = "INSERT INTO fibras (nombre) VALUES (?)"
        self.registro={"nombre":nombre_fibra}
        self.SQL = "INSERT INTO fibras (nombre) VALUES (:nombre)"
        #self.nombre_fibra = nombre_fibra
    
class GetFibraID(QueryBase):
    def __init__(self, id_fibra=-1):
        self.registro={"id_fibra":id_fibra}
        self.SQL = "SELECT id_fibra FROM fibras WHERE nombre = :id_fibra"
        
    def execute(self,conn):
        """Aqui llamamos a la ejecución de la query y pelamos el resultado"""
        resultados = super().execute(conn)
        
        if resultados:  
            id_fibra = resultados[0][0]   # fetalldone devuelve una lista de tuplas
            return id_fibra
        else:
            print("No se encontró la fibra")
            return None


class InsertDividendo(QueryBase):
    def __init__(self,valores):      
        cols, placeholders = getColsAndPlaceholders(DB_DIVIDENDOS_2_EXCEL)
        self.SQL = f"INSERT INTO distribuciones ({cols}) VALUES ({placeholders})"
        
        for k in DB_DIVIDENDOS_2_EXCEL.keys():
             self.registro[k]=valores[DB_DIVIDENDOS_2_EXCEL[k]]
    
class InsertVela(QueryBase):
    def __init__(self, valores):
        cols, placeholders = getColsAndPlaceholders(DB_VELAS_2_EXCEL)
        self.SQL = f"INSERT INTO velas ({cols}) VALUES ({placeholders})"
        
        for k in DB_VELAS_2_EXCEL.keys():
             self.registro[k]=valores[DB_VELAS_2_EXCEL[k]]