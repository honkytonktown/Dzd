#My feeling is any manipulation done on data should be stored in a new table
import os
import psycopg2
import Config.Config as config
import pandas as pd
import ManipulateData.DzdLogic as dzd
import ManipulateData.SqlCmds as SqlCmds

#insertData inserts modified data into the sql table.
#For this module, it the same data that was pulled but with
#the additional dzdinterpretation column
def insertData(row):
    cur = config.conn.cursor()
    SQLInsert = """ INSERT INTO public."AggregateTests"(sampid, organism, test, antibiotic, value, antibioticinterpretation, method, dzdinterpretation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """
    data = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
    cur.execute(SQLInsert, data) 
    config.conn.commit()

#getData pulls data from sql table for manipulation
def getData():
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."AggregateTests" """, config.conn)
    df = pd.DataFrame(SQLSelect, columns=['sampid', 'organism','test','antibiotic','value', 'antibioticinterpretation', 'method' ])
    return df

def getDzdRules():
    SQLSelect = pd.read_sql_query(""" SELECT * FROM public."DzdRules" """, config.conn)
    dfRules = pd.DataFrame(SQLSelect, columns=['organism', 'susceptible', 'intermediatelow', 'intermediatehigh', 'resistant', 'antibiotic', 'method'])
    return dfRules

#alterTable creates a column within the sql table to allow 
#new dzd column
def alterTable(): 
    cur = config.conn.cursor()
    cmd = SqlCmds.AlterTable
    cur.execute(cmd)
    config.conn.commit()

#createNewCol creates new column for dzd to insert
#their own interpretation of results
def generateDzdValues(df, dfRules):
    df['dzdinterpretation'] = df.apply(lambda x: dzd.applyLogic(x.value, x.organism, x.method, x.antibiotic, dfRules), axis=1)

#clearTable truncates the table to allow easy insertion
def clearTable():
    cur = config.conn.cursor()
    #there might be a cleaner way to insert new data
    #this is brute force time saver
    SQLClear = """ TRUNCATE public."AggregateTests" """
    cur.execute(SQLClear)
    config.conn.commit()

#pushData iterates over df rows and calls insertData
#to insert them into sql table
#For this particular case, it also truncates the table to
#bypassing insert matching. Would not do this in production, 
#but its a simple solution for now
def pushData(df):
    clearTable()
    for i,row in df.iterrows():
        insertData(row)

#dataHandler is main func of this module
#if mode == 1, it pull data, modify it and push it back to the sql table
#if mode == 0 itll pull data, and modify the dataframe only
def dataHandler(mode):
    #pd.set_option('display.max_rows', None)
    df = getData()
    dfRules = getDzdRules()
    print("Dataframe column names: ")
    print(df.columns.values)

    print("Creating new column with Dzd modification...")
    generateDzdValues(df, dfRules)
    #pd.set_option('display.max_rows', None)
    #print(df)
    if (mode == 1):
        alterTable()
        pushData(df)
        config.CloseConnection()



