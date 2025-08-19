# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:12:44 2025

@author: M R
"""
import sqlite3
from abc import ABC, abstractmethod


class QueryBase(ABC):
    SQL=""

    @abstractmethod
    def params(self):
        """Debe devolver una tupla con los parámetros de la query"""
        pass

    def execute(self,conn):
        """Ejecuta la query usando el conector dado"""
        cursor = conn.cursor()
        cursor.execute(self.SQL, self.params())
        try:
            return cursor.fetchall()  # SELECT
        except sqlite3.ProgrammingError:
            # para INSERT/UPDATE/DELETE que no devuelven resultados
            return None

class InsertNewFibra(QueryBase):
    SQL = "INSERT INTO fibras (nombre) VALUES (?)"
    
    def __init__(self, nombre_fibra=""):
        self.nombre_fibra = nombre_fibra

    def params(self):
        return (self.nombre_fibra,)
    
class GetFibraID(QueryBase):
    SQL = "SELECT id_fibra FROM fibras WHERE nombre = ?"
    
    def __init__(self, id_fibra=-1):
        self.id_fibra = id_fibra

    def params(self):
        return (self.id_fibra,)
    
    # def execute(self,conn)->Integer:
    #     super().execute(conn)
    #     resultado = cursor.fetchone()
    #     id=-1
    #     if resultado:  
    #         id_fibra = resultado[0]   # fetchone devuelve una tupla
    #         print("El id_fibra es:", id_fibra)
    #     else:
    #         print("No se encontró la fibra")
    #     return int
    
class InsertDividendo(QueryBase):
    SQL = """
            insert into distribuciones (id_fibra,fecha_pago,fecha_ex_dividendo,tipo_dividendo,dividendo,rendimiento) 
            values (?,?,?,?,?,?)
            """
    def __init__(self, id_fibra =-1, fecha_pago = None , fecha_ex_dividendo = None,
                 tipo_dividendo = "", dividendo = -1, rendimiento =-1):
        self.id_fibra = id_fibra
        self.fecha_pago = fecha_pago
        self.fecha_ex_dividendo = fecha_ex_dividendo
        self.tipo_dividendo = tipo_dividendo
        self.dividendo = dividendo
        self.rendimiento = rendimiento

    def params(self):
        return (self.id_fibra,self.fecha_pago,self.fecha_ex_dividendo,
                self.tipo_dividendo,self.dividendo,self.rendimiento)