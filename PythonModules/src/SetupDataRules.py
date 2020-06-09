#SetupRules pushes defined rules to SQL table for later use
#insertData receives a row and inserts it into sql table

import Config.Config as config
import pandas as pd
import Tables.CreateMatchRules as MRtable

def createDataTable():
    cmd = MRtable.createTable
    cur = config.conn.cursor()
    cur.execute(cmd)
    config.conn.commit()

def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."MatchingRules"(replacementphrase, regexpattern) VALUES (%s, %s); """
    data = (row[0], row[1])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into sql table
def pushData(df):
    for i,row in df.iterrows():
        insertData(row)

def pushMatchingRules(mode): 
    matchDictionary = {
     'replacementphrase': ['Trimethoprim/Sulfamethoxazole', 'Trimethoprim/Sulfamethoxazole'],
     'regexpattern': ['Trimeth', 'Sulfa'] 
     }
    df = pd.DataFrame(data=matchDictionary)
    
    if(mode == 0):
        print(df)
    elif(mode == 1):
        pushData(df)
        config.CloseConnection()
    elif(mode == 2):
        createDataTable()
        pushData(df)
        config.CloseConnection()
    
