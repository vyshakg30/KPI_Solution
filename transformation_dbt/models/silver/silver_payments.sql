WITH silver_payments_raw AS (
    SELECT
        TRIM(payment_id) AS payment_id,
        TRIM(loan_id) AS loan_id,
        TRY_CAST(payment_dt AS DATE) AS payment_dt,
        TRY_CAST(amount AS DOUBLE) AS amount,
        TRIM(LOWER(status)) AS status,
    FROM
        {{ ref('bronze_payments') }}
    WHERE
        TRIM(payment_id) IS NOT NULL AND TRIM(payment_id) <> ''
    QUALIFY row_number() over (
        partition by payment_id
        order by payment_id
    ) = 1

)

SELECT
   sp.*
FROM
  silver_payments_raw sp
INNER JOIN {{ ref('silver_loans') }} sl on
  sp.loan_id = sl.loan_id
WHERE
    (
        CASE
            WHEN sp.status='success' AND sp.amount < 0 THEN FALSE
            ELSE TRUE
        END
    )
    AND
    sl.principal > 0



