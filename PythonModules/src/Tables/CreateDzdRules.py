createTable = """
CREATE TABLE public."DzdRules"
(
    organism character varying COLLATE pg_catalog."default",
    susceptible character varying COLLATE pg_catalog."default",
    intermediatelow character varying COLLATE pg_catalog."default",
    intermediatehigh character varying COLLATE pg_catalog."default",
    resistant character varying COLLATE pg_catalog."default",
    antibiotic character varying COLLATE pg_catalog."default",
    method character varying COLLATE pg_catalog."default"
)
TABLESPACE pg_default;
"""


