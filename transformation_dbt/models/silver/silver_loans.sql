WITH silver_loans_raw AS (
  SELECT
    TRIM(loan_id) AS loan_id,
    TRIM(quote_id) AS quote_id,
    TRY_CAST(funded_at AS DATE) AS funded_at,
    TRY_CAST(principal AS INTEGER) AS principal,
    TRY_CAST(apr AS DOUBLE) AS apr,
    TRY_CAST(term_months AS INTEGER) AS term_months,
    TRIM(status) AS status
  FROM
    {{ ref('bronze_loans') }}
  WHERE
    TRIM(loan_id) IS NOT NULL
    AND TRIM(loan_id) <> '' QUALIFY ROW_NUMBER() OVER(PARTITION BY loan_id ORDER BY funded_at DESC,loan_id) = 1
)
SELECT
  sl.*
FROM
  silver_loans_raw sl
  INNER JOIN {{ ref('silver_quotes') }} sq ON sl.quote_id = sq.quote_id
