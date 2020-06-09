import InitialImport.UploadCollData as UploadCollData
import InitialImport.UploadPhenoData as UploadPhenoData
import ManipulateData.ManipulateData as manipData
import SetupTables
import SetupDataRules
import SetupDzdRules

phenoCSV = ""
collCSV = ""
phenoCSV = 'C:\\Users\\j839602\\Desktop\\SampleProject\\CsvFiles\\PhenotypeData.csv'
collCSV = 'C:\\Users\\j839602\\Desktop\\SampleProject\\CsvFiles\\CollectionsData.csv'

def setupRules(mode):
    print("Setting up rules")
    if(mode == 1):
        print("Setting up data matching rules...")
        SetupDataRules.pushMatchingRules(0)
        print("Done setting up data rules table")

        print("Setting up dzd specific rules...")
        SetupDzdRules.pushDzdRules(0)
        print("Done setting up dzd rules table")

def startup(mode):
    print("Starting initial setup...")
    if(mode == 1):
        print("Uploading CollectionsData...")
        UploadCollData.collDataHandler(0, collCSV)
        print("Done uploading CollectionsData")

        print("Uploading PhenotypeData...")
        UploadPhenoData.phenoDataHandler(0, phenoCSV)
        print("Done uploading PhenotypeData")

        print("Generating SQL tables...")
        Setupables.tableHandler(0)
        print("Done generating SQL tables")

        print("Done initializing data and SQL tables")
    
def manipulateData(mode):
    manipData.dataHandler(mode)

#setupRules(1)
#startup(0)
manipulateData(0)
