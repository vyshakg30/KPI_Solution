WITH gold_daily_kpi AS (
  SELECT
    *
  FROM
    {{ ref('gold_daily_kpi') }}
)
,
gold_daily_kpi_median AS (
  SELECT
    gdk.funded_at,
    MEDIAN(gdk2.default_rate_D90) AS median_default_rate_D90,
    MEDIAN(gdk2.funded_count) AS median_funded_count,
    LIST(gdk2.default_rate_D90) AS previous_defaults,
    LIST(gdk2.funded_count) AS previous_funded_counts,
    LIST(gdk2.funded_at) AS previous_qualified_dates,
    COUNT_IF(gdk2.funded_at IS NOT NULL) AS base_line_days
  FROM
    gold_daily_kpi gdk
    LEFT JOIN gold_daily_kpi gdk2 ON
        gdk2.funded_at BETWEEN (gdk.funded_at - interval 3 day) AND (gdk.funded_at - interval 1 day)
  GROUP BY
    gdk.funded_at
  ORDER BY
    gdk.funded_at
)
SELECT
  gdkm.funded_at AS alert_date,
  gdk.default_rate_D90 >= (1.5 * gdkm.median_default_rate_D90) AS default_spiked,
  gdk.funded_count <= (0.5 * gdkm.median_funded_count) AS volume_droped
FROM
  gold_daily_kpi_median gdkm
  LEFT JOIN gold_daily_kpi gdk ON gdkm.funded_at = gdk.funded_at
WHERE
  gdkm.base_line_days >= 2
