SELECT
    TRY_CAST(payment_id AS VARCHAR) as payment_id,
    TRY_CAST(loan_id AS VARCHAR) as loan_id,
    TRY_CAST(payment_dt AS VARCHAR) as payment_dt,
    TRY_CAST(amount AS VARCHAR) as amount,
    TRY_CAST(status AS VARCHAR) as status,
    * EXCLUDE(payment_id,loan_id,payment_dt,amount,status)
FROM
    read_csv_auto('seeds/payments.csv', ignore_errors=true, sample_size = -1 )