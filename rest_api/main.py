from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db_utils import query_as_dict, config

app = FastAPI(title=config["app"]["name"])

# ---------- Global Exception Handler ----------
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

@app.middleware("http")
async def add_no_cache_header_middleware(request: Request, call_next):
    response = await call_next(request)
    # Add the no-cache headers to every response
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ---------- API Endpoints ----------
@app.get("/api/kpis1")
def get_kpis(date: str):
    return {"date": date, "kpis": query_as_dict("SELECT * FROM dev.gold.gold_daily_kpi")}

@app.get("/api/kpis")
def get_kpis(date: str):
    return {"date": date}


@app.get("/api/alerts")
def get_alerts(date_from: str, date_to: str):
    return {
        "from": date_from,
        "to": date_to,
        "alerts": query_as_dict("SELECT * FROM alerts WHERE date BETWEEN ? AND ? ORDER BY date", [date_from, date_to])
    }

@app.get("/api/report")
def get_report(date_from: str, date_to: str):
    return {
        "from": date_from,
        "to": date_to,
        "reports": query_as_dict("SELECT * FROM reports WHERE date BETWEEN ? AND ? ORDER BY date", [date_from, date_to])
    }