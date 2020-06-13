
import Config.Config as config


def delete():
    cur = config.conn.cursor()
    cmd = """
    DROP TABLE public."DzdRules", 
    public."MatchingRules", 
    public."AggregateTests",
    public."CollectionsData",
    public."PhenotypeData",
    public."MainTable",
    public."MainTableAll",
    public."MainTableNulls",
    public."OrganismResistance";
    """
    try:
        cur.execute(cmd)
        config.conn.commit()
    except Exception as err:
        print(err)
        config.conn.rollback()

def delete_all_tables(mode):
    if mode == 1:
        delete()

