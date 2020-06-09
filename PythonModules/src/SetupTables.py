import Tables.CreateAggregateTests
import Tables.CreateMainTables
import Tables.CreateOrganismResistance
import Config as config

#createMain creates table w/ sampid, organism, (unique values)
def createMain():
    cur = config.conn.cursor()
    cmd = Tables.CreateMainTables.MainTable
    cur.execute(cmd)
    config.conn.commit()

#createMainNulls creates table w/ sampid, organism (with null organisms)
#This would be the table full of sampids that didn't match anything in
#the phenotype data set
def createMainNull():
    cur = config.conn.cursor()
    cmd = Tables.CreateMainTables.MainTableNulls
    cur.execute(cmd)
    config.conn.commit()

#createMainAggregate creates table w/ sampid, organism for every match (duplicate sampids)
#This table may be dropped as it's not essential
def createMainAggregate():
    cur = config.conn.cursor()
    cmd = Tables.CreateMainTables.MainTableAgg
    cur.execute(cmd)
    config.conn.commit()

#createAggregate creates table w/ sampid matched with every test
#its corresponding hid/isolate aligns with
def createAggregate():
    cur = config.conn.cursor()
    cmd = Tables.CreateAggregateTests.CreateTable
    cur.execute(cmd)
    config.conn.commit()

#createResistance creates table w/ organisms and the tests/results
#that have been run against them.
def createResistance():
    cur = config.conn.cursor()
    cmd = Tables.CreateOrganismResistance.CreateTable
    cur.execute(cmd)
    config.conn.commit()

#tableHandler generates SQL tables if enabled
#Tables can be found in the tables folder
def tableHandler(mode):
    if (mode == 1):
        createMain()
        #createMainAggregate needs to be built before
        #MainNull because it builds off it
        createMainAggregate()
        createMainNull()
        createAggregate()
        createResistance()
        config.CloseConnection()
    else: 
        msg = "The mode is set to {}".format(mode)
        print (msg)