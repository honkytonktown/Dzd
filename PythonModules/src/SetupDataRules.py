#SetupRules pushes defined rules to SQL table for later use
#insertData receives a row and inserts it into sql table

import Config.Config as config
import pandas as pd
import Tables.CreateMatchRules as MRtable

#createDataTable creates SQL table that will hold data matching rules
def createDataTable():
    cur = config.conn.cursor()
    cmd = MRtable.createTable
    cur.execute(cmd)
    config.conn.commit()

#insertData inserts data into data matching table
def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."MatchingRules"(columnname, replacementphrase, regexpattern) VALUES (%s, %s, %s); """
    data = (row[0], row[1], row[2])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into SQL table
def pushData(df):
    for i,row in df.iterrows():
        insertData(row)

#pushMatchingRules defines and then handles data matching rules.
#These rules are stored and then pulled when formatting CSV data later
#As wil the DZD rules table, you'd want to define these elsewhere in 
#production
def pushMatchingRules(mode): 
    print("Setting up data matching rules...")
    #You'd probably want a different insertion method,
    #but of that implementation would be easy.
    #Define rules -> insert into SQL table
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
    
