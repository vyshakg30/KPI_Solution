SELECT
  gk.*
FROM
  {{ ref('gold_daily_kpi') }} gk
WHERE
  funded_count < 0
