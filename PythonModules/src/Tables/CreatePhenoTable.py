createTable = """
CREATE TABLE public."PhenotypeData"
(
    hid character varying COLLATE pg_catalog."default",
    isolate character varying COLLATE pg_catalog."default",
    received character varying COLLATE pg_catalog."default",
    organism character varying COLLATE pg_catalog."default",
    source character varying COLLATE pg_catalog."default",
    antibiotic character varying COLLATE pg_catalog."default",
    antibioticinterpretation character varying COLLATE pg_catalog."default",
    method character varying COLLATE pg_catalog."default",
    test character varying COLLATE pg_catalog."default",
    value character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

"""