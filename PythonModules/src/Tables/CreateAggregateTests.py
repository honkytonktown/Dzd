CreateTable = """
CREATE TABLE public."AggregateTests"
(
    sampid character varying COLLATE pg_catalog."default",
    organism character varying COLLATE pg_catalog."default",
    test character varying COLLATE pg_catalog."default",
    antibiotic character varying COLLATE pg_catalog."default",
    value character varying COLLATE pg_catalog."default",
    antibioticinterpretation character varying COLLATE pg_catalog."default",
    method character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;
"""

InsertData = """
INSERT INTO public."AggregateTests" (sampid, organism, test, antibiotic, value, antibioticinterpretation, method)	
SELECT sampid, 
	   public."PhenotypeData".organism,
	   public."PhenotypeData".test, 
	   public."PhenotypeData".antibiotic, 
	   public."PhenotypeData".value, 
	   public."PhenotypeData".antibioticinterpretation, 
	   public."PhenotypeData".method
FROM public."CollectionsData"

JOIN public."PhenotypeData" ON (public."PhenotypeData".hid = public."CollectionsData".hid 
								AND public."PhenotypeData".isolate = public."CollectionsData".isolate );
"""