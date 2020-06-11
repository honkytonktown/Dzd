#SetupDzdRules pushes defined rules to SQL table for later use

import Config.Config as config
import pandas as pd
import Tables.CreateDzdRules as DZDtable

#createDzdTable creates SQL table that will hold dzd rules
def createDzdTable():
    cur = config.conn.cursor()
    cmd = DZDtable.createTable
    try:
        cur.execute(cmd)
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()
    

#insertData inserts data into dzd rules SQL table
def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."DzdRules"(organism, susceptible, intermediatelow, intermediatehigh, resistant, antibiotic, method) VALUES (%s, %s, %s, %s, %s, %s, %s); """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    try:
        cur.execute(SQLInsert, data) 
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()

#pushData iterates over df rows and calls insertData
#to insert them into SQL table
def pushData(df):
    for i,row in df.iterrows():
        insertData(row)

#pushDzdRules, for simplicity, defines dzd rules and then calls various
#functions on them. In production, you'd want these defined and handled outside
#of this application. I imagine you'd want them used on multiple datasets. 
def pushDzdRules(mode): 
    print("Setting up dzd specific rules...")
    #You'd probably want a different insertion method,
    #but implementation would be easy
    dzdDictionary = {
     'organism': ['Escherichia coli', 'Staphylococcus capitis'], 
     'susceptible': ['4', '4'],  
     'intermediatelow': ['4', '4'],
     'intermediatehigh': ['16', '16'], 
     'resistant': ['16', '16'],  
     'antibiotic': ['Ceftazidime', 'Penicillin G'],  
     'method': ['VITEK II', 'VITEK II']
     }
    df = pd.DataFrame(data=dzdDictionary)
    df = df.astype(str)
    df = df.applymap(lambda x: x.strip())

    if(mode == 0):
        print(df)
    elif(mode == 1):
        pushData(df)
    elif(mode == 2):
        createDzdTable()
        pushData(df)
    print("Done setting up dzd rules table")
