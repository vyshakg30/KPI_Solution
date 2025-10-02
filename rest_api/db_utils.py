import duckdb, yaml
from duckdb import CatalogException

# load config once
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

DB_FILE = config["database"]["duckdb_file"]

def query_as_dict(sql: str, params=None):
    if params is None:
        params = []
    try:
        with duckdb.connect(DB_FILE) as con:
            cur = con.execute(sql, params)
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    except CatalogException:
        # if file replaced, reconnect fresh
        with duckdb.connect(DB_FILE) as con:
            cur = con.execute(sql, params or [])
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]