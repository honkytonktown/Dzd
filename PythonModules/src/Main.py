import InitialImport.UploadCollData
import InitialImport.UploadPhenoData
import ManipulateData.ManipulateData 
import SetupTables
import SetupDataRules
import SetupDzdRules
import DropTables
import Config.Config as config

#normally you'd pass these in via cmd line
phenoCSV =  r'C:\Users\j839602\Desktop\SampleProject\OriginalCSV\PhenotypeData.csv'
collCSV = r'C:\Users\j839602\Desktop\SampleProject\OriginalCSV\CollectionsData.csv'

def setup_rules(mode):
    """ setup_rules creates sql tables to hold data rules that are applied later
        mode - 0 = print rules, 1 = insert rules, 2 = createtable + insert """
    print("Setting up rules...")
    SetupDataRules.push_matching_rules(mode)
    SetupDzdRules.push_dzd_rules(mode)
    print("Done setting up rules")

def import_csv_data(mode):
    """ import_csv_data imports csv files, formats them, and stores them in db
        mode - 0 = print data, 1 = push data to SQL table """ 
    print("Starting import data...")
    InitialImport.UploadCollData.coll_data_handler(mode, collCSV)
    InitialImport.UploadPhenoData.pheno_data_handler(mode, phenoCSV)

    print("Data has been imported into postgres DB")

def setup_sql_tables(mode):
    """ setup_sql_tables creates additional tables from existing SQL data
        mode - 0 = nothing, 1 = creates tables """
    print("Setting up SQL tables...")
    SetupTables.table_handler(mode)
    print("Done setting up SQL table")

def manipulate_data(mode):
    """ manipulate_data is where you'd modify existing data
        in this case, this is where you could apply DZD specific interpretation
        of resistances values
        mode: 0 = pull modified data, dont push back to SQL
            1 = pull modified data, push back to SQL
            2 = pull unmodified data, push back to SQL""" 
    print("Manipulating data to apply dzd rules...")
    ManipulateData.ManipulateData.data_handler(mode)
    #once this has run, you can use validation test in SQlCmds.py to check
    print("Done applying dzd rules")

def drop_tables(mode):
    """ drop_tables drops all tables """
    print("Dropping tables...")
    DropTables.delete_all_tables(mode)
    print("Tables dropped")

def main():
    """ main is the root of the application. Other modules are accessible through it """ 
    setup_rules(2)
    import_csv_data(1)
    setup_sql_tables(1)
    manipulate_data(2) 

    #drop_tables(1) #enable this to drop all tables
    config.close_connection()
    print("Process done")

if __name__ == "__main__":
    main()
