SELECT
  TRY_CAST(payment_id AS VARCHAR) AS payment_id,
  TRY_CAST(loan_id AS VARCHAR) AS loan_id,
  TRY_CAST(payment_dt AS VARCHAR) AS payment_dt,
  TRY_CAST(amount AS VARCHAR) AS amount,
  TRY_CAST(status AS VARCHAR) AS status,
  * EXCLUDE(payment_id,loan_id,payment_dt,amount,status)
FROM
  READ_CSV_AUTO('seeds/payments.csv',ignore_errors = TRUE,sample_size = -1)
