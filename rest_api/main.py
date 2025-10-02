from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db_utils import query_as_dict, config

app = FastAPI(title=config["app"]["name"])

#  Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "path": str(request.url),
            "type": exc.__class__.__name__,
        },
    )



# API Endpoints
@app.get("/api/kpisall")
def get_kpis():
    return {"kpis": query_as_dict("SELECT * FROM dev.gold.gold_daily_kpi limit 100000")}

@app.get("/api/kpis")
def get_kpis(date: str):
    return {"date": date, "kpis": query_as_dict(f"SELECT * FROM dev.gold.gold_daily_kpi where funded_at = '{date}'")}

@app.get("/api/alerts")
def get_alerts(date_from: str, date_to: str):
    return {
        "from": date_from,
        "to": date_to,
        "alerts": query_as_dict(f"SELECT * FROM dev.gold.gold_alerts_daily where alert_date between '{date_from}' AND '{date_to}'")
    }

@app.get("/api/report")
def get_report(date_from: str, date_to: str):


    return {
        "from": date_from,
        "to": date_to,
        "reports": query_as_dict("SELECT * FROM reports WHERE date BETWEEN ? AND ? ORDER BY date", [date_from, date_to])
    }