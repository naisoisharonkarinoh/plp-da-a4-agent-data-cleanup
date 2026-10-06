import pandas as pd
import numpy as np


def clean_agent_data(txns, agents):
    """
    Clean transaction data and merge it with agent information.

    Returns:
        clean_df: cleaned transaction DataFrame
        log: list of cleaning actions performed
    """

    log = []

    # Make copies so the original data is not changed
    out = txns.copy()
    agents_clean = agents.copy()

    # 1. Remove duplicate transactions using txn_id
    before_rows = len(out)

    out = out.drop_duplicates(subset=["txn_id"]).copy()

    removed_duplicates = before_rows - len(out)

    log.append(
        f"Removed {removed_duplicates} duplicate transaction rows"
    )

    # 2. Clean transaction type
    out["txn_type"] = (
        out["txn_type"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    valid_types = ["Deposit", "Withdrawal"]

    invalid_type_mask = ~out["txn_type"].isin(valid_types)

    invalid_types = int(invalid_type_mask.sum())

    log.append(
        f"Found {invalid_types} invalid transaction types"
    )

    # Keep only valid transaction types
    out = out[out["txn_type"].isin(valid_types)].copy()

    # 3. Convert amount to numeric
    out["amount"] = (
        out["amount"]
        .astype("string")
        .str.replace(",", "", regex=False)
    )

    out["amount"] = pd.to_numeric(
        out["amount"],
        errors="coerce"
    )

    # Create the required imputation flag BEFORE filling
    out["amount_imputed"] = out["amount"].isna()

    missing_amounts = int(out["amount_imputed"].sum())

    # Fill missing/invalid amounts with the median
    if missing_amounts > 0:
        median_amount = out["amount"].median()
        out["amount"] = out["amount"].fillna(median_amount)

    log.append(
        f"Imputed {missing_amounts} missing or invalid amounts with the median"
    )

    # 4. Detect outliers using the IQR method
    q1 = out["amount"].quantile(0.25)
    q3 = out["amount"].quantile(0.75)

    iqr = q3 - q1

    lower_fence = q1 - (1.5 * iqr)
    upper_fence = q3 + (1.5 * iqr)

    out["is_outlier"] = (
        (out["amount"] < lower_fence)
        | (out["amount"] > upper_fence)
    )

    outlier_count = int(out["is_outlier"].sum())

    log.append(
        f"Flagged {outlier_count} amount outliers for review"
    )

    # 5. Convert transaction date to datetime
    out["txn_date"] = pd.to_datetime(
        out["txn_date"],
        errors="coerce"
    )

    invalid_dates = int(out["txn_date"].isna().sum())

    log.append(
        f"Found {invalid_dates} invalid transaction dates"
    )

    # 6. Remove duplicate agent records
    agents_clean = agents_clean.drop_duplicates(
        subset=["agent_id"]
    ).copy()

    # 7. Merge transactions with agent information
    clean_df = out.merge(
        agents_clean[["agent_id", "agent_name", "county"]],
        on="agent_id",
        how="left",
        validate="many_to_one"
    )

    # 8. Check transactions with unknown agents
    unknown_agents = int(clean_df["county"].isna().sum())

    log.append(
        f"Found {unknown_agents} transactions with unknown agents"
    )

    return clean_df, log