import base64
import io

import matplotlib
import numpy as np

from .alert_utils import add_alert_baseline_delta

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os


def generate_charts(kpi_data):
    if not kpi_data:
        return None, None

    dates = [row["funded_at"] for row in kpi_data]

    funded = [row.get("funded_count") for row in kpi_data]
    default_rate = [row.get("default_rate_D90") for row in kpi_data]

    # Replace None with np.nan
    funded_np = np.array([np.nan if v is None else v for v in funded], dtype=float)
    default_np = np.array([np.nan if v is None else v for v in default_rate], dtype=float)

    # --- Chart 1: Funded Count ---
    fig1, ax1 = plt.subplots()

    # solid line (with gaps)
    ax1.plot(dates, funded_np, marker="o", linestyle="-", color="blue", label="Funded Count")

    # dotted line connecting gaps (interpolated)
    funded_interp = np.copy(funded_np)
    isnan = np.isnan(funded_interp)
    if isnan.any():
        # simple linear interpolation across NaNs
        funded_interp[isnan] = np.interp(np.flatnonzero(isnan), np.flatnonzero(~isnan), funded_interp[~isnan])
        ax1.plot(dates, funded_interp, linestyle=":", color="blue")

    ax1.set_title("Funded Count Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Funded Count")
    fig1.autofmt_xdate()

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png")
    plt.close(fig1)
    chart1 = base64.b64encode(buf1.getvalue()).decode("utf-8")

    # --- Chart 2: Default Rate ---
    fig2, ax2 = plt.subplots()
    ax2.plot(dates, default_np, marker="o", linestyle="-", color="red", label="Default Rate")

    default_interp = np.copy(default_np)
    isnan2 = np.isnan(default_interp)
    if isnan2.any():
        default_interp[isnan2] = np.interp(np.flatnonzero(isnan2), np.flatnonzero(~isnan2), default_interp[~isnan2])
        ax2.plot(dates, default_interp, linestyle=":", color="red")

    ax2.set_title("Default Rate D90 Over Time")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Default Rate (%)")
    fig2.autofmt_xdate()

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png")
    plt.close(fig2)
    chart2 = base64.b64encode(buf2.getvalue()).decode("utf-8")

    return chart1, chart2


def render_html_report(from_date, to_date, kpis, alerts):
    """Render HTML report using Jinja template."""
    chart1, chart2 = generate_charts(kpis)

    funded_total = sum(row["funded_count"] or 0 for row in kpis)
    avg_apr = round(sum(row["avg_apr"] or 0 for row in kpis) / len(kpis), 2) if kpis else 0
    avg_margin = round(sum(row["principal_weighted_margin"] or 0 for row in kpis) / len(kpis), 2) if kpis else 0

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "../templates")))
    template = env.get_template("report.html")

    alerts_baseline_delta = add_alert_baseline_delta(alerts)

    return template.render(
        from_date=from_date,
        to_date=to_date,
        generated_at=ts,
        funded_total=funded_total,
        avg_apr=avg_apr,
        avg_margin=avg_margin,
        kpis=kpis,
        alerts=alerts_baseline_delta,
        chart1=chart1,
        chart2=chart2,
    )
