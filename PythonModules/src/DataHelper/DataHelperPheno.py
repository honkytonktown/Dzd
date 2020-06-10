#DataHelper parses data to apply rules from rules table
import Config.Config as config
import DataHelper.ApplyRules
import pandas as pd

def getMatchingRules():
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."MatchingRules" """, config.conn)
    dfRules = pd.DataFrame(SQLSelect, columns=['columnname','replacementphrase', 'regexpattern'])
    return dfRules

#removeISO helper function to remove ISO from isolate
def removeISO(item):
    item = item.replace("ISO", "")
    return item

#formatData is where the raw csv data is modified to match db standards
def formatColsPheno(df): 
    df.columns = ["hid", "isolate", "received", "organism", "source", "test","antibiotic", "value", "antibioticinterpretation", "method"]

def formatRowsPheno(df, dfRules): 
    df['isolate'] = df['isolate'].apply(removeISO)
    #df = df.applymap(lambda x: DataHelper.ApplyRules.handler(x, dfRules))
    df['antibiotic'] = df['antibiotic'].apply(lambda x: DataHelper.ApplyRules.handler(x, dfRules, 'antibiotic'))
    df['organism'] = df['organism'].apply(lambda x: DataHelper.ApplyRules.handler(x, dfRules, 'organism'))
    df = df.astype(str)
    df = df.apply(lambda x: x.str.strip())

def dataHandlerPheno(df):
    dfRules = getMatchingRules()
    formatColsPheno(df)
    formatRowsPheno(df, dfRules)
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_columns', None)
    #print(df)
    return df
