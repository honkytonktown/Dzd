# DZD project: Overview

Note: to install packages run *pip3 install -r requirements.txt* in src folder

## SQL Tables:
PhenotypeData and CollectionsData are basically copies of the csv data, with applied formatting.

MainTable: 
This table contains only unique sampid and organism columns. If you want to get all
tests run for a specific sampid, you'd query the sampid against the AggregateTests table.
If you want to check an organisms resistance to antibiotics regardless of sampid, you'd just query
the organism against the OrganismResistance table. 

Because some sampids do not match anything in PhenotypeData, I also felt it would be good to create
a table of sampid and organism that only held these values. Maybe more PhenotypeData comes in later
in the week and you only want to test against sampids that haven't been test already. 

MainTable, MainTableNulls, PhenotypeData, CollectionsData, and AggregateTests are all specific to provided 
CSV files.<br />
OrganismResistance, DzdRules, MatchingRules could be used for multiple datasets. 


## Modules:
Main.py contains the basic sequence of events.<br />

setupRules: <br />
Create tables to insert DZD interpretations and formatting rules -- <br />
DZD interpretation table is used in manipulateData. <br />
Formatting rules are used on initial CSV import. <br />
My thinking here was that you might have some external database that holds these rules
so they can be used on multiple datasets. For real use, this would be done outside the 
sequence of events defined in Main.py.

importCSVData: <br />
Import CSV data, format it, then push it into SQL tables. Matching rules from above
are called in from SQL table and applied to PhenotypeData. This is one area where more effort/time
would be beneficial. The more rules you have defined, the cleaner the data will be. 
As I do not know what other rules you'd want, I only did a few. But the process would be the 
same for any such rules. Define rule -> find cell that fits parameters -> apply rule. 

setupSQLTables: <br />
Once data is stored, additional SQL tables are generated from Pheno and Collections data. Since 
by this point the data is already cleaned up a bit, and the additional tables are just
different combinations of PhenotypeData and CollectionsData columns, there is nothing that 
needs to be done outside of SQL. I tried to get away from CSV stuff as quickly as possible.

manipulateData: <br />
This is for the bonus portion. If you want to reinterpret results,
pull rules from DZD rules table, pull data, run data through rules and 
push it back into SQL. My guess is this is a precursor to how you'd run the data
through ML modules. My thinking is that you want to get a stable set of the data,
cleaned and sorted into useful tables/columns before even worrying about using it.

## Areas of for improvement:
Some assumptions need to be made about the data. Flexibility is good but within reason.
One area that could be improved would be to have some sort of data rules for column names. 
This would help arrange columns in a consistent way. Regex patterns could be used the same way
they're used on the actual rows of the data. 

Error handling:  <br />
Error handling and logging is minimal throughout the program. Ensuring connection to
Postgre database is open, rolling back changes if necessary, etc... could be expanded on. 
Depending on the situation you'd maybe want to redirect all the print statements to log files. 

SQL queries: <br />
The SQL queries are all hard coded in. In production, you'd likely want to write stored procedures and call those.
That would provide more protection against SQL injection. Though considering it's mostly professionals working on this data,
I can't imagine anyone would purposefully try to mess up the data in such a way. But always best to be safe. 
