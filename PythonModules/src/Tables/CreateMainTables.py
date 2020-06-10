
MainTable = """ 
CREATE TABLE public."MainTable"
(
    sampid character varying COLLATE pg_catalog."default",
    organism character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default; 

"""

InsertData = """ 
INSERT INTO public."MainTable" (sampid, organism)
SELECT DISTINCT sampid, 
	   public."PhenotypeData".organism
FROM public."CollectionsData"
INNER JOIN public."PhenotypeData" ON (public."PhenotypeData".hid = public."CollectionsData".hid 
								AND public."PhenotypeData".isolate = public."CollectionsData".isolate ); 
"""

MainTableAgg = """ 
CREATE TABLE public."MainTableAll"
(
    sampid character varying COLLATE pg_catalog."default",
    organism character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default; 
"""

InsertMainTableAll = """ 
INSERT INTO public."MainTableAll" (sampid, organism)
SELECT sampid, 
public."PhenotypeData".organism

FROM public."CollectionsData"

LEFT JOIN public."PhenotypeData" ON (public."PhenotypeData".hid = public."CollectionsData".hid 
								AND public."PhenotypeData".isolate = public."CollectionsData".isolate ); 
"""


MainTableNulls = """
CREATE TABLE public."MainTableNulls"
(
    sampid character varying COLLATE pg_catalog."default",
    organism character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default; 
"""

InsertMainTableNulls = """
INSERT INTO public."MainTableNulls" (sampid, organism)
SELECT *
FROM public."MainTableAll"
WHERE organism IS NULL
""" 