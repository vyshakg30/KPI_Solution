# Analytics pipeline

## Architecture

### ETL Approach
We employ a "Best Effort Load" approach for loading raw data, ignoring invalid or redundant points in favor of 
"Error Quarantining" over an "All or Nothing" method. During testing, invalid entries are easily identified.

Strict data integrity constraints are maintained for all KPI and Alert data stores.



### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
