SELECT
  TRY_CAST(quote_id AS VARCHAR) AS quote_id,
  TRY_CAST(created_at AS VARCHAR) AS created_at,
  TRY_CAST(band AS VARCHAR) AS band,
  TRY_CAST(system_size_kw AS VARCHAR) AS system_size_kw,
  TRY_CAST(down_payment AS VARCHAR) AS down_payment,
  TRY_CAST(system_price AS VARCHAR) AS system_price,
  TRY_CAST(email AS VARCHAR) AS email,
  * EXCLUDE(quote_id,created_at,band,system_size_kw,down_payment,system_price,email)
FROM
  READ_CSV_AUTO('seeds/quotes.csv',ignore_errors = TRUE,sample_size = -1)
