# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:12:44 2025

@author: M R
"""
import sqlite3
from abc import ABC, abstractmethod

#Query Objects
#Usados para leer datos de una hoja de excel e insertarlos en la base sqlite
#Para mantener esto sencillo tendremos una hoja de calculo por cada tabla

class QueryBase(ABC):
    SQL=""
    
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

class InsertDividendo(QueryBase):
    DB2EXCEL={"id_fibra":"id_fibra",
              "fecha_ex_dividendo":"Fecha ex-dividendo",
              "fecha_pago": "Fecha de pago",
              "tipo_dividendo": "Tipo",
              "dividendo": "Dividendo",
              "rendimiento": "Rendimiento"}
    
    def __init__(self,valores):
        cols = ",".join(self.DB2EXCEL.keys())
        placeholders = ",".join([f":{k}" for k in self.DB2EXCEL.keys()])
        
        self.SQL = f"INSERT INTO distribuciones ({cols}) VALUES ({placeholders})"
        for k in self.DB2EXCEL.keys():
             self.registro[k]=valores[self.DB2EXCEL[k]]
    
class InsertVela(QueryBase):
    DB2EXCEL={ "id_fibra":"id_fibra",
               "timestamp":"Fecha",
               "open":"Apertura",
               "high":"Máximo",
               "low":"Mínimo",
               "close":"Cierre",
               "volume":"Vol.",
               "var":"% var.",
               "frecuencia":"frecuencia"}
    
    def __init__(self, valores):
        cols = ",".join(self.DB2EXCEL.keys())
        placeholders = ",".join([f":{k}" for k in self.DB2EXCEL.keys()])
      
        self.SQL = f"INSERT INTO velas ({cols}) VALUES ({placeholders})"
        
        for k in self.DB2EXCEL.keys():
             self.registro[k]=valores[self.DB2EXCEL[k]]