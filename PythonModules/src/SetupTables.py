import os
import psycopg2
import Tables.CreateAggregateTests as agt
import Tables.CreateMainTables as mt
import Tables.CreateOrganismResistance as ogr
import Config.Config as config

def create_main():
    """ create_main creates table w/ sampid, organism, unique values """ 
    cur = config.conn.cursor()
    cmd = mt.MainTable
    cur.execute(cmd)
    cmInsert = mt.InsertData
    cur.execute(cmInsert)
    config.conn.commit()

def create_main_aggregate():
    """ create_main_aggregate creates table w/ sampid, organism for every match (duplicate sampids)
        This table may be dropped as it's not essential """ 
    cur = config.conn.cursor()
    cmd = mt.MainTableAgg
    cur.execute(cmd)
    cmInsert = mt.InsertMainTableAll
    cur.execute(cmInsert)
    config.conn.commit()

def create_main_null():
    """ createMainNulls creates table w/ sampid, organism (with null organisms)
        This table is full of sampids that didn't match anything in the phenotype data set """ 
    cur = config.conn.cursor()
    cmd = mt.MainTableNulls
    cur.execute(cmd)
    cmInsert = mt.InsertMainTableNulls
    cur.execute(cmInsert)
    config.conn.commit()

def create_aggregate():
    """ create_aggregate creates table w/ sampid matched with every test
        its corresponding hid/isolate aligns with """
    cur = config.conn.cursor()
    cmd = agt.CreateTable
    cur.execute(cmd)
    cmInsert = agt.InsertData
    cur.execute(cmInsert)
    config.conn.commit()

def create_resistance():
    """ create_resistance creates table w/ organisms and the tests/results
        that have been run against them. """
    cur = config.conn.cursor()
    cmd = ogr.CreateTable
    cur.execute(cmd)
    cmInsert = ogr.InsertData
    cur.execute(cmInsert)
    config.conn.commit()

def table_handler(mode):
    """ table_handler generates SQL tables if enabled
        Tables can be found in the tables folder """ 
    print("Generating SQL tables...")
    if (mode == 1):
        create_main()
        #MainAggregate needs to be built before
        #MainNull because it builds from it
        create_main_aggregate()
        create_main_null()
        create_aggregate()
        create_resistance()
        print("Done generating SQL tables")
    else: 
        msg = "The mode is set to {}".format(mode)
        print (msg)
        