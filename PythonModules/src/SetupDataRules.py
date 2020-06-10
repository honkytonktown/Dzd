#SetupRules pushes defined rules to SQL table for later use
#insertData receives a row and inserts it into sql table

import Config.Config as config
import pandas as pd
import Tables.CreateMatchRules as MRtable

def createDataTable():
    cur = config.conn.cursor()
    cmd = MRtable.createTable
    cur.execute(cmd)
    config.conn.commit()

def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."MatchingRules"(columnname, replacementphrase, regexpattern) VALUES (%s, %s, %s); """
    data = (row[0], row[1], row[2])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into sql table
def pushData(df):
    for i,row in df.iterrows():
        insertData(row)

def pushMatchingRules(mode): 
    print("Setting up data matching rules...")
    matchDictionary = {
    'columnname': ['antibiotic'],
    'replacementphrase': ['Trimethoprim/Sulfamethoxazole'],
    'regexpattern': ['/.*\\b(Trimeth.*|Sulfa.*)\\b.*'] 
    }
    df = pd.DataFrame(data=matchDictionary)
    df = df.astype(str)
    df = df.apply(lambda x: x.str.strip())

    if(mode == 0):
        print(df)
    elif(mode == 1):
        pushData(df)
    elif(mode == 2):
        createDataTable()
        pushData(df)
    print("Done setting up data rules table")
    
