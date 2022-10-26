import csv
from flask import make_response

def createCSV(result):
    with open('socios.csv','w',newline='',encoding='utf-8') as file:
        writer= csv.writer(file,delimiter="")
        writer.writerows(result)

        response = make_response(file.close())
        response.headers.set("Content-Disposition","attachment",filename="socios.csv")
        response.headers.set('Content-Type', 'text/csv')
        return response