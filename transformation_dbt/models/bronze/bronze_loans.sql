SELECT
    TRY_CAST(loan_id AS VARCHAR) AS loan_id,
    TRY_CAST(quote_id AS VARCHAR) AS quote_id,
    TRY_CAST(funded_at AS VARCHAR) AS funded_at,
    TRY_CAST(principal AS VARCHAR) AS principal,
    TRY_CAST(apr AS VARCHAR) AS apr,
    TRY_CAST(term_months AS VARCHAR) AS term_months,
    TRY_CAST(status AS VARCHAR) AS status,
    * EXCLUDE (loan_id,quote_id,funded_at,principal,apr,term_months,status)
FROM
    read_csv_auto('seeds/loans.csv', ignore_errors=true, sample_size = -1)