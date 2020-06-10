createTable = """
CREATE TABLE public."MatchingRules"
(
    columnname character varying COLLATE pg_catalog."default",
    replacementphrase character varying COLLATE pg_catalog."default",
    regexpattern character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;
"""