with gold_daily_kpi as (
    select
        *
    from {{ ref('gold_daily_kpi') }}
),

gold_daily_kpi_median AS (
    select
        gdk.funded_at,
        median(gdk2.default_rate_D90) as median_default_rate_D90,
        median(gdk2.funded_count) as median_funded_count,
        LIST(gdk2.default_rate_D90) as previous_defaults,
        LIST(gdk2.funded_count) as previous_funded_counts,
        LIST(gdk2.funded_at) as previous_qualified_dates,
        COUNT_IF(gdk2.funded_at is not null) as base_line_days
    from
        gold_daily_kpi gdk
    left join gold_daily_kpi gdk2 on
        gdk2.funded_at between (gdk.funded_at - interval 3 day) and (gdk.funded_at - interval 1 day)
    group by gdk.funded_at
        order by gdk.funded_at
)

select
    gdkm.funded_at as alert_date,
    gdk.default_rate_D90 >= (1.5 * gdkm.median_default_rate_D90) as default_spiked,
    gdk.funded_count <= (0.5 * gdkm.median_funded_count) as volume_droped,
FROM
    gold_daily_kpi_median gdkm
LEFT JOIN gold_daily_kpi gdk ON
    gdkm.funded_at = gdk.funded_at
WHERE
    gdkm.base_line_days >= 2