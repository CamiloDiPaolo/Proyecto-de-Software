import pandas as pd
from flask import make_response


def createCSV(data):
    df= pd.DataFrame(data)
    resp= make_response(df.to_csv())
    resp.headers["Content-Disposition"]="attachment; filename=export.csv"
    resp.headers["Content-Type"]="text/csv"
    return resp
