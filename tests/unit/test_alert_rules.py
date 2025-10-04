import re
from pathlib import Path

import duckdb
import pytest

# Path to your DBT model
ALERT_SQL_FILE = Path(__file__).parent.parent / "../transformation_dbt" / "models" / "gold" / "gold_alerts_daily.sql"


@pytest.fixture
def duckdb_connection():
    """
    Returns an in-memory DuckDB connection with sample gold_daily_kpi data.
    """
    con = duckdb.connect(":memory:")

    # Create sample table
    con.execute("""
        CREATE TABLE gold_daily_kpi (
            loan_id INTEGER,
            funded_at DATE,
            funded_count INTEGER,
            avg_apr DOUBLE,
            principal_weighted_margin DOUBLE,
            default_rate_D90 DOUBLE
        )
    """)

    # Insert some sample rows
    sample_data = [
        (1, '2024-01-15', 3, 0.1, 0.0543, 33.33),
        (2, '2024-01-16', 2, 0.1, 0.0509, 0.0),
        (3, '2024-01-17', 2, 0.1, 0.065, 50.0),
        (4, '2024-01-18', 2, 0.13, 0.0808, 100.0),
        (5, '2024-01-19', 1, 0.08, 0.03, 100.0),
        (6, '2024-01-20', 1, 0.08, 0.03, None),
    ]
    con.executemany(
        "INSERT INTO gold_daily_kpi VALUES (?, ?, ?, ?, ?, ?)",
        sample_data
    )

    yield con
    con.close()


def test_alert_rules(duckdb_connection):
    """
    Test DBT alert SQL rules using in-memory DuckDB.
    """

    con = duckdb_connection

    # Read SQL from file and replace DBT ref
    alert_sql = ALERT_SQL_FILE.read_text()

    alert_sql = alert_sql.replace("{{ ref('gold_daily_kpi') }}", "gold_daily_kpi")
    sql_clean = re.sub(r"\{\{\s*ref\(['\"](.*?)['\"]\)\s*\}\}", r"\1", alert_sql)

    # Execute SQL
    result = con.execute(sql_clean).fetchall()

    expected = [
        ("2024-01-17", True, False),
        ("2024-01-18", True, False),
        ("2024-01-19", True, True),
        ("2024-01-20", None, True)  # include this row as returned by SQL
    ]

    # Convert actual DuckDB results to strings for comparison
    result = [(str(r[0]), r[1], r[2]) for r in result]

    assert result == expected, f"Expected {expected}, got {result}"
