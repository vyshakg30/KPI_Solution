import io
import base64
import matplotlib
matplotlib.use("Agg")   # ✅ headless backend (no GUI needed)
import matplotlib.pyplot as plt
from datetime import datetime


def generate_charts(kpi_data):
    """Generate two charts (funded_count & default_rate_D90 over time) as base64 images."""

    if not kpi_data:
        return None, None

    dates = [row["funded_at"] for row in kpi_data]
    funded = [row["funded_count"] for row in kpi_data]

    # --- Chart 1: Funded Count Over Time ---
    fig1, ax1 = plt.subplots()
    ax1.plot(dates, funded, marker="o", linestyle="-", color="blue")
    ax1.set_title("Funded Count Over Time")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Funded Count")
    fig1.autofmt_xdate()
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png")
    plt.close(fig1)
    chart1 = base64.b64encode(buf1.getvalue()).decode("utf-8")

    # --- Chart 2: Default Rate D90 Over Time ---
    default_rate = [row["default_rate_D90"] for row in kpi_data]

    fig2, ax2 = plt.subplots()
    ax2.plot(dates, default_rate, marker="o", linestyle="-", color="red")
    ax2.set_title("Default Rate D90 Over Time")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Default Rate (%)")
    fig2.autofmt_xdate()
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png")
    plt.close(fig2)
    chart2 = base64.b64encode(buf2.getvalue()).decode("utf-8")

    return chart1, chart2


def generate_html_report(from_date, to_date, kpis, alerts):
    """Generate an HTML report including summary KPIs, charts, and alerts."""

    chart1, chart2 = generate_charts(kpis)

    # --- Summary calculations ---
    funded_total = sum(row["funded_count"] for row in kpis if row.get("funded_count") is not None) if kpis else 0
    avg_apr = (
        sum(row["avg_apr"] for row in kpis if row.get("avg_apr") is not None) / len(kpis)
        if kpis else 0
    )
    avg_margin = (
        sum(row["principal_weighted_margin"] for row in kpis if row.get("principal_weighted_margin") is not None) / len(kpis)
        if kpis else 0
    )

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Build Alerts Table ---
    alerts_html = "<p>No alerts in this period.</p>"
    if alerts:
        rows = "".join(
            f"<tr><td>{a['alert_date']}</td><td>{a['default_spiked']}</td><td>{a['volume_droped']}</td></tr>"
            for a in alerts
        )
        alerts_html = f"""
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Date</th><th>Default Spiked</th><th>Volume Dropped</th></tr>
            {rows}
        </table>
        """

    # --- Build HTML ---
    html = f"""
    <html>
    <head>
        <title>KPI Report {from_date} - {to_date}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ margin-top: 30px; }}
            img {{ max-width: 600px; margin: 10px 0; }}
            ul {{ line-height: 1.6; }}
            table {{ border-collapse: collapse; margin-top: 15px; }}
            th, td {{ padding: 6px 12px; }}
            th {{ background: #f0f0f0; }}
        </style>
    </head>
    <body>
        <h1>KPI Report</h1>
        <p><b>Date Range:</b> {from_date} → {to_date}</p>
        <p><b>Generated at:</b> {ts}</p>
        
        <h2>Summary</h2>
        <ul>
          <li><b>Total Funded Count:</b> {funded_total}</li>
          <li><b>Average APR:</b> {avg_apr:.2f}</li>
          <li><b>Average Margin:</b> {avg_margin:.2f}</li>
        </ul>

        <h2>Charts</h2>
        <h3>Funded Count Over Time</h3>
        {"<img src='data:image/png;base64," + chart1 + "' />" if chart1 else "<p>No chart data</p>"}
        
        <h3>Default Rate D90 Over Time</h3>
        {"<img src='data:image/png;base64," + chart2 + "' />" if chart2 else "<p>No chart data</p>"}

        <h2>Alerts</h2>
        {alerts_html}
    </body>
    </html>
    """
    return html