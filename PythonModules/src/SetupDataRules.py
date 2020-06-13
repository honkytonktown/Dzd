#SetupRules pushes defined rules to SQL table for later use
#insertData receives a row and inserts it into sql table

import Config.Config as config
import pandas as pd
import psycopg2
import Tables.CreateMatchRules as MRtable


def create_data_table():
    """ createDataTable creates SQL table that will hold data matching rules """
    cur = config.conn.cursor()
    cmd = MRtable.createTable
    try:
        cur.execute(cmd)
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()


def insert_data(row):
    """ insert_data inserts data into data matching table """
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."MatchingRules"(columnname, replacementphrase, regexpattern) VALUES (%s, %s, %s); """
    data = (row[0], row[1], row[2])
    try:
        cur.execute(SQLInsert, data) 
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()
        

def push_data(df):
    """ push_data iterates over df rows and calls insert_data
        to insert them into SQL table """
    for i, row in df.iterrows():
        insert_data(row)

def push_matching_rules(mode): 
    """ pushMatchingRules defines and then handles data matching rules.
        These rules are stored and then pulled when formatting CSV data later
        As wil the DZD rules table, you'd want to define these elsewhere in 
        production """
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
    df = df.applymap(lambda x: x.strip())

    if(mode == 0):
        print(df)
    elif(mode == 1):
        push_data(df)
    elif(mode == 2):
        create_data_table()
        push_data(df)
    print("Done setting up data rules table")
    
