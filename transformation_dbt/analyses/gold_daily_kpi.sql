WITH silver_loans AS (
    SELECT
        *
    FROM {{ ref('silver_loans') }}
    WHERE status NOT IN ('cancelled','withdrawn')
),

-- Calculate If for each loan Id are there any defaults in last 90 days
silver_loan_defaults AS (
    SELECT
        sl.funded_at,
        sl.loan_id,
        CASE
            WHEN
                COUNT_IF(
                           sp.status IN ('failed', 'missed') AND
                           sp.payment_dt BETWEEN sl.funded_at AND (sl.funded_at + INTERVAL 90 DAY)
                        ) > 0 THEN true
            ELSE FALSE
        END AS has_defaults
    FROM
        silver_loans AS sl
    LEFT JOIN {{ ref('silver_payments')}} AS sp ON
        sl.loan_id = sp.loan_id
    GROUP BY
        sl.funded_at,sl.loan_id
),

-- Calculate default percentage for each day.
silver_loan_defaults_percentage AS (
    SELECT
        sld.funded_at,
        ROUND( (COUNT_IF(has_defaults) / count(*)) * 100, 2) AS default_rate_D90
    FROM
        silver_loan_defaults sld
    GROUP BY
        sld.funded_at
),

-- Calculate aggregations
silver_loan_aggregated AS (
    SELECT
        funded_at,
        count(*) AS funded_count,
        AVG(apr) AS avg_apr,
        sum(principal * (apr - 0.05)) / sum(principal) AS principal_weighted_margin
    FROM
        silver_loans AS sl
    GROUP BY
        sl.funded_at
    Order BY
        sl.funded_at
)

SELECT
    slg.*,
    sldp.default_rate_D90
FROM
    silver_loan_aggregated slg
LEFT JOIN silver_loan_defaults_percentage sldp ON
    slg.funded_at =  sldp.funded_at
ORDER BY
    slg.funded_at
