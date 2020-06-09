CreateTable = """
CREATE TABLE public."OrganismResistance"
(
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
INSERT INTO public."OrganismResistance" (organism, test, antibiotic, value, antibioticinterpretation, method)	
SELECT organism, test, 
	   antibiotic, 
	   value, 
	   antibioticinterpretation, 
	   method
FROM public."PhenotypeData"

"""