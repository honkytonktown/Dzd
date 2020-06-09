AlterTable = """
ALTER TABLE public."AggregateTests"
ADD COLUMN dzdinterpretation varchar;
"""

InsertData = """
INSERT INTO public."AggregateTests"(
	sampid, organism, test, antibiotic, value, antibioticinterpretation, method, dzdinterpretation)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?);

"""

CreateDzdTable = """
CREATE TABLE public."DzdRules"
(
    organism character varying COLLATE pg_catalog."default",
    susceptible character varying COLLATE pg_catalog."default",
    intermediate character varying COLLATE pg_catalog."default",
    resistant character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;
"""