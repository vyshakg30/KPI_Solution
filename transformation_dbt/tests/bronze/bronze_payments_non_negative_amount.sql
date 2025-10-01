{{ config(severity = 'warn') }}
SELECT
   bp.*
FROM
  {{ ref('bronze_payments') }} bp
INNER JOIN {{ ref('bronze_loans') }} bl on
  TRIM(bp.loan_id) = TRIM(bl.loan_id)
WHERE
  TRIM(LOWER(bp.status)) = 'success' AND TRY_CAST(bp.amount AS DOUBLE) < 0