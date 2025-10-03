import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from rest_api.utils.db_utils import query_as_dict, config, get_kpi_from_db, get_alerts_from_db
from rest_api.utils.report_utils import render_html_report

app = FastAPI(title=config["app"]["name"])

# Resolve absolute path to "templates/static"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "templates", "static")

# Mount static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


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

@app.get("/api/kpis")
def get_kpis(date: str):
    return {
        "date": date,
        "kpis": get_kpi_from_db(date, date)
    }


@app.get("/api/alerts")
def get_alerts(date_from: str, date_to: str):
    return {
        "from": date_from,
        "to": date_to,
        "alerts": get_alerts_from_db(date_from, date_to)
    }


@app.get("/api/report")
def get_report(date_from: str, date_to: str):
    kpis = get_kpi_from_db(date_from, date_to)
    alerts = get_alerts_from_db(date_from, date_to)
    return HTMLResponse(content=render_html_report(date_from, date_to, kpis, alerts))


@app.get("/api/report_json")
def get_report(date_from: str, date_to: str):
    return {
        "from": date_from,
        "to": date_to,
        "kpi": get_kpi_from_db(date_from, date_to),
        "alerts": get_alerts_from_db(date_from, date_to)
    }


@app.get("/api/kpisall")
def get_kpis():
    return {"kpis": query_as_dict("SELECT * FROM dev.gold.gold_daily_kpi limit 100000")}
