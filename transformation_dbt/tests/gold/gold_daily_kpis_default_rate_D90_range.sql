SELECT
  gk.*
FROM
  {{ ref('gold_daily_kpi') }} gk
WHERE
  default_rate_D90 < 0
  OR default_rate_D90 > 100
