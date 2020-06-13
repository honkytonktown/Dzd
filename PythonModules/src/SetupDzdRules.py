#SetupDzdRules pushes defined rules to SQL table for later use

import Config.Config as config
import pandas as pd
import Tables.CreateDzdRules as DZDtable


def create_dzd_table():
    """ create_dzd_table creates SQL table that will hold dzd rules """
    cur = config.conn.cursor()
    cmd = DZDtable.createTable
    try:
        cur.execute(cmd)
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()
    


def insert_data(row):
    """ insert_data inserts data into dzd rules SQL table """
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."DzdRules"(organism, susceptible, intermediatelow, 
    intermediatehigh, resistant, antibiotic, method) VALUES (%s, %s, %s, %s, %s, %s, %s); """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    try:
        cur.execute(SQLInsert, data) 
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()


def push_data(df):
    """ push_data iterates over df rows and calls insertData
        to insert them into SQL table """
    for i,row in df.iterrows():
        insert_data(row)


def push_dzd_rules(mode): 
    """ push_dzd_rules, for simplicity, defines dzd rules and then calls various
        functions on them. In production, you'd want these defined and handled outside
        of this application. I imagine you'd want them used on multiple datasets. """
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
        push_data(df)
    elif(mode == 2):
        create_dzd_table()
        push_data(df)
    print("Done setting up dzd rules table")
