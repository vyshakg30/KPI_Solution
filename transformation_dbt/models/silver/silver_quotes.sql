SELECT
  TRIM(quote_id) AS quote_id,
  TRY_CAST(created_at AS DATE) AS created_at,
  TRIM(UPPER(band)) AS band,
  TRY_CAST(system_size_kw AS INTEGER) AS system_size_kw,
  TRY_CAST(down_payment AS INTEGER) AS down_payment,
  TRY_CAST(system_price AS INTEGER) AS system_price,
  TRIM(email) AS email
FROM
  {{ ref('bronze_quotes') }}
WHERE
  TRIM(UPPER(band)) IN ('A','B','C')
  AND TRIM(quote_id) IS NOT NULL
  AND TRIM(quote_id) <> '' QUALIFY ROW_NUMBER() OVER(PARTITION BY quote_id ORDER BY created_at DESC,quote_id) = 1
