import InitialImport.UploadCollData
import InitialImport.UploadPhenoData
import ManipulateData.ManipulateData 
import SetupTables
import SetupDataRules
import SetupDzdRules
import Config.Config as config

phenoCSV = ""
collCSV = ""
phenoCSV = 'C:\\Users\\j839602\\Desktop\\SampleProject\\CsvFiles\\PhenotypeData.csv'
collCSV = 'C:\\Users\\j839602\\Desktop\\SampleProject\\CsvFiles\\CollectionsData.csv'

#setupRules creates sql tables to hold data rules that are applied later
#0 = print rules, 1 = insert rules, 2 = createtable + insert
def setupRules(mode):
    print("Setting up rules...")
    SetupDataRules.pushMatchingRules(mode)
    SetupDzdRules.pushDzdRules(mode)
    print("Done setting up rules")

#setupSQLTables imports csv files, formats them, and stores them in db
#once csv data is inserted, other SQL tables are built off the inserted data
def setupSQLTables(mode):
    print("Starting initial setup...")
    InitialImport.UploadCollData.collDataHandler(mode, collCSV)
    InitialImport.UploadPhenoData.phenoDataHandler(mode, phenoCSV)
    SetupTables.tableHandler(mode)
    print("Done initializing data and SQL tables")

#manipulateData is where you'd existing data
#in this case, this is where you could apply DZD specific interpretation
#of resistances values
def manipulateData(mode):
    print("Manipulating data to apply dzd rules...")
    ManipulateData.ManipulateData.dataHandler(mode)
    print("Done applying dzd rules")

def main():
    #setupRules(2)
    #setupSQLTables(1)
    manipulateData(1)
    config.CloseConnection()
    print("Process done")

if __name__ == "__main__":
    main()
