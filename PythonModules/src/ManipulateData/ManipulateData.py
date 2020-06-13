#My feeling is any manipulation done on data should be stored in a new table
import os
import psycopg2
import Config.Config as config
import pandas as pd
import ManipulateData.DzdLogic as dzd
import ManipulateData.SqlCmds as SqlCmds


def insert_data(row):
    """ insert_data inserts modified data into the sql table.
        For this module, it the same data that was pulled but with
        the additional dzdinterpretation column """ 
    cur = config.conn.cursor()
    SQLInsert = """ 
    INSERT INTO public."AggregateTests"
    (sampid, organism, test, antibiotic, value, antibioticinterpretation, method, dzdinterpretation) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s); 
    """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

def get_modified_data(): 
    """ get_modified_data is used when a dzdinterpretation columna already exists """
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."AggregateTests" """, config.conn)
    df = pd.DataFrame(SQLSelect, columns=['sampid', 'organism','test',
    'antibiotic','value', 'antibioticinterpretation', 'method', 'dzdinterpretation'])
    return df

def get_data():
    """ get_data pulls data from sql table for manipulation """
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."AggregateTests" """, config.conn)
    df = pd.DataFrame(SQLSelect, columns=['sampid', 'organism','test','antibiotic','value', 
    'antibioticinterpretation', 'method' ])
    return df

def get_dzd_rules():
    """ get_dzd_rules pulls dzd rules from specified SQL table """
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."DzdRules" """, config.conn)
    dfRules = pd.DataFrame(SQLSelect, columns=['organism', 'susceptible', 'intermediatelow', 
    'intermediatehigh', 'resistant', 'antibiotic', 'method'])
    return dfRules


def alter_table(): 
    """ alter_table creates a column within the sql table to allow new dzd column """
    cur = config.conn.cursor()
    cmd = SqlCmds.AlterTable
    cur.execute(cmd)
    config.conn.commit()


def generate_dzd_values(df, dfRules):
    """ #generate_dzd_values creates new column for dzd to insert
        their own interpretation of results """
    df['dzdinterpretation'] = df.apply(lambda x: dzd.apply_logic(x.value, x.organism, x.method, x.antibiotic, dfRules), axis=1)

def clear_table():
    """ clear_table truncates the table to allow easy insertion """
    cur = config.conn.cursor()
    #there might be a cleaner way to insert new data
    #this is brute force time saver
    SQLClear = """ TRUNCATE public."AggregateTests" """
    cur.execute(SQLClear)
    config.conn.commit()


def push_data(df):
    """ push_data iterates over df rows and calls insertData
        to insert them into sql table
        For this particular case, it also truncates the table to
        bypassing insert matching. Would not do this in production, 
        but its a simple solution for now """
    clear_table()
    for i,row in df.iterrows():
        insert_data(row)


def data_handler(mode):
    """ data_handler is main func of this module
        if mode == 1, it pull data, modify it and push it back to the sql table
        if mode == 0 itll pull data, and modify the dataframe only """
    #pd.set_option('display.max_rows', None)

    #pull modified data, dont push back to SQL
    if (mode == 0):
        df = get_data()
        dfRules = get_dzd_rules()
        print("Dataframe column names: ")
        print(df.columns.values)
        generate_dzd_values(df, dfRules)
        print(df)

    #pull modified data, push back to SQL
    elif (mode == 1):
        df = get_modified_data()
        dfRules = get_dzd_rules()
        print("Dataframe column names: ")
        print(df.columns.values)
        generate_dzd_values(df, dfRules)
        clear_table()
        push_data(df)

    #pull unmodified data, push back to SQL
    elif(mode == 2):
        df = get_data()
        dfRules = get_dzd_rules()
        print("Dataframe column names: ")
        print(df.columns.values)
        generate_dzd_values(df, dfRules)
        print("Modified dataframe column names: ")
        print(df.columns.values)
        clear_table()
        alter_table()
        push_data(df)
    #pd.set_option('display.max_rows', None)

        



