#SetupDzdRules pushes defined rules to SQL table for later use

import Config.Config as config
import pandas as pd
import Tables.CreateDzdRules as DZDtable

def createDzdTable():
    cmd = DZDtable.createTable
    cur = config.conn.cursor()
    cur.execute(cmd)
    config.conn.commit()

def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."DzdRules"(organism, susceptible, intermediatelow, intermediatehigh, resistant, antibiotic, method) VALUES (%s, %s, %s, %s, %s, %s, %s); """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into sql table
def pushData(df):
    for i,row in df.iterrows():
        insertData(row)

def pushDzdRules(mode): 
    dzdDictionary = {
     'organism': ['Escherichia coli'],
     'susceptible': ['4'],  
     'intermediatelow': ['4.01'],
     'intermediatehigh': ['16'], 
     'resistant': ['16.01'],  
     'antibiotic': ['Ceftazidime'],  
     'method': ['VITEK II']
     }
    df = pd.DataFrame(data=dzdDictionary)

    if(mode == 0):
        print(df)
    elif(mode == 1):
        pushData(df)
        config.CloseConnection()
    elif(mode == 2):
        createDzdTable()
        pushData(df)
        config.CloseConnection()

