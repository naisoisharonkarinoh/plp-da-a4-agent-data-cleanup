# PLP Data Analytics A4 — Agent Data Cleanup

## Project Summary

This project cleans and validates agent transaction data using Python, Pandas, and NumPy.

The cleaning pipeline addresses data-quality issues across six dimensions:

- Completeness
- Validity
- Accuracy
- Consistency
- Uniqueness
- Timeliness

The pipeline removes duplicate transactions, standardizes transaction types, converts transaction amounts to numeric values, imputes missing or invalid amounts, flags outliers, converts transaction dates, and merges transaction data with agent information.

## How to Run

1. Run `generate_data.py` to generate the transaction and agent datasets.
2. Run `agent_cleanup.ipynb` from top to bottom.
3. The notebook imports `clean_agent_data()` from `cleaning_pipeline.py`.
4. The cleaned dataset is saved as:

`outputs/agent_transactions_clean.csv`

## Before-and-After Row Count

The generated transaction dataset contains **1001 rows** before cleaning.

The notebook reports the final row count after the cleaning pipeline and merge.

## Output

The final cleaned dataset includes:

- Transaction ID
- Agent ID
- Transaction type
- Amount
- Transaction date
- Amount imputation flag
- Outlier flag
- Agent information
- County
