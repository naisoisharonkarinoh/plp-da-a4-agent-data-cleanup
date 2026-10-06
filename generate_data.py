import pandas as pd
import numpy as np

rng = np.random.default_rng(44)

n_txns = 1000
n_agents = 50

agent_ids = [f"A{str(i).zfill(3)}" for i in range(1, n_agents + 1)]

agents = pd.DataFrame({
    "agent_id": agent_ids,
    "agent_name": [f"Agent {i}" for i in range(1, n_agents + 1)],
    "county": rng.choice(
        ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu"],
        size=n_agents
    )
})

txn_types = rng.choice(
    ["Deposit", "Withdrawal"],
    size=n_txns,
    p=[0.6, 0.4]
)

txns = pd.DataFrame({
    "txn_id": [f"T{str(i).zfill(5)}" for i in range(1, n_txns + 1)],
    "agent_id": rng.choice(agent_ids, size=n_txns),
    "txn_type": txn_types,
    "amount": rng.uniform(100, 50000, size=n_txns),
    "txn_date": pd.date_range(
        "2026-01-01",
        periods=n_txns,
        freq="D"
    )
})

# Introduce data-quality issues
txns.loc[10, "amount"] = np.nan
txns.loc[25, "amount"] = "1,500"
txns.loc[40, "amount"] = "invalid"

txns.loc[60, "txn_type"] = "deposit"
txns.loc[75, "txn_type"] = "TRANSFER"

txns.loc[90, "txn_date"] = "2026/04/01"

# Duplicate transaction
txns = pd.concat(
    [txns, txns.iloc[[100]]],
    ignore_index=True
)

# High-value outlier
txns.loc[120, "amount"] = 200000

# Unknown agent
txns.loc[130, "agent_id"] = "A999"

agents.to_csv("agents.csv", index=False)
txns.to_csv("agent_transactions.csv", index=False)

print("Generated agent records:", len(agents))
print("Generated transaction records:", len(txns))