import os

import duckdb, yaml
from duckdb import CatalogException

# load config once
with open(os.path.dirname(__file__) + "/../config.yml", "r") as f:
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


def get_alerts_from_db(date_from: str, date_to: str):
    return query_as_dict(f"select * FROM dev.gold.gold_alerts_daily where alert_date between '{date_from}' and '{date_to}'")

def get_kpi_from_db(date_from: str, date_to: str):
    return query_as_dict(f"select * FROM dev.gold.gold_daily_kpi where funded_at between '{date_from}' and '{date_to}'")

