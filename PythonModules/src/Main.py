import InitialImport.UploadCollData
import InitialImport.UploadPhenoData
import ManipulateData.ManipulateData 
import SetupTables
import SetupDataRules
import SetupDzdRules
import DropTables
import Config.Config as config

phenoCSV = ""
collCSV = ""
#normally you'd pass these in via cmd line
phenoCSV = '/home/joe/Desktop/dzd/OriginalCSV/PhenotypeData.csv'
collCSV = '/home/joe/Desktop/dzd/OriginalCSV/CollectionsData.csv'

#setupRules creates sql tables to hold data rules that are applied later
#mode - 0 = print rules, 1 = insert rules, 2 = createtable + insert
def setupRules(mode):
    print("Setting up rules...")
    SetupDataRules.pushMatchingRules(mode)
    SetupDzdRules.pushDzdRules(mode)
    print("Done setting up rules")

#importCSVData imports csv files, formats them, and stores them in db
#mode - 0 = print data, 1 = push data to SQL table
def importCSVData(mode):
    print("Starting import data...")
    InitialImport.UploadCollData.collDataHandler(mode, collCSV)
    InitialImport.UploadPhenoData.phenoDataHandler(mode, phenoCSV)

    print("Data has been imported into postgres DB")

#setupSQLTables creates additional tables from existing SQL data
#mode - 0 = nothing, 1 = creates tables
def setupSQLTables(mode):
    print("Setting up SQL tables...")
    SetupTables.tableHandler(mode)
    print("Done setting up SQL table")

#manipulateData is where you'd existing data
#in this case, this is where you could apply DZD specific interpretation
#of resistances values
#mode: 0 = pull modified data, dont push back to SQL
#      1 = pull modified data, push back to SQL
#      2 = pull unmodified data, push back to SQL
def manipulateData(mode):
    print("Manipulating data to apply dzd rules...")
    ManipulateData.ManipulateData.dataHandler(mode)
    #once this has run, you can use validation test in SQlCmds.py to check
    print("Done applying dzd rules")

def dropTables(mode):
    print("Dropping tables...")
    DropTables.deleteAllTables(mode)
    print("Tables dropped")

def main():
    setupRules(2)
    importCSVData(1)
    setupSQLTables(1)
    manipulateData(2) 

    #dropTables(1) #enable this to drop all tables
    config.CloseConnection()
    print("Process done")

if __name__ == "__main__":
    main()
