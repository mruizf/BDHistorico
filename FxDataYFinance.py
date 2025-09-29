# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 16:08:26 2025

@author: M R
"""


import yfinance as yf
import pandas as pd
import queries as qu

FX = {"EUR/USD":"EURUSD=X","USD/MXN":"USDMXN=X"}

INDICE_FIBRAS = "FIBRATC14.MX"

# Descargar datos diarios de EUR/USD
df_eur_usd = yf.download( FX["EUR/USD"], start="2024-01-01", end="2025-08-22",ignore_tz=True)
df_eur_usd_flat=df_eur_usd.copy()

#Con esta linea estamos "aplanando" el nombre de las columnas, cambiamos algo jerarquico por una
#etiquera 
df_eur_usd_flat.columns =  [f"{a}" for a, b in df_eur_usd.columns]


df_usd_mxn = yf.download(FX["USD/MXN"], start="2024-01-01", end="2025-08-22",ignore_tz=True)
print(df_eur_usd_flat.head())
print(df_usd_mxn.head())

df_ipc_mxn = yf.download( INDICE_FIBRAS, start="2024-01-01", end="2025-08-22",ignore_tz=True,group_by=None)

print(df_ipc_mxn.head())
print(df_ipc_mxn.columns.tolist())


print(df_eur_usd.columns.tolist())

for index,row in df_eur_usd.iterrows():
    print(row,"---")

for index,row in df_eur_usd.iterrows():
    print(type(index))
print(type(row))

[f"{a}" for a, b in data_eur_usd.columns]

print (data_eur_usd.columns)

#if __name__=="__main__":
    
    