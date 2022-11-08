import pandas as pd
import json
from flask import make_response,jsonify, request

def createCSV(result):


    df= pd.DataFrame(result) #columns=('nro_socio','email','nombre','apellido','tipo_documento','nro_documento'))
    df.to_csv('listado.csv', index=False, header=False, encoding='utf-8')
    #response = make_response(df)
    #response.headers.set('Content Type', 'text/csv')
    #response.headers.set("Content-Disposition","attachment",filename="listado.csv")
    return ('<h1> descargado </h1>')
