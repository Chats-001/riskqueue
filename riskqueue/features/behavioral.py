from __future__ import annotations

from collections import defaultdict, deque

import numpy as np
import pandas as pd


def add_behavioral_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Build historical features one row at a time, updating state only afterward.

    PaySim ``step`` is an hour. Equal-step rows deliberately cannot see one another:
    features for an hour are computed from state frozen at the start of that hour.
    """
    data = frame.sort_values("step", kind="stable").copy()
    output: dict[str, list[float]] = defaultdict(list)
    sender_history: dict[str, deque[tuple[int, float, str]]] = defaultdict(deque)
    recipient_history: dict[str, deque[tuple[int, float, str]]] = defaultdict(deque)
    sender_all_amounts: dict[str, list[float]] = defaultdict(list)
    sender_last: dict[str, int] = {}
    recipient_last: dict[str, int] = {}
    pair_count: dict[tuple[str, str], int] = defaultdict(int)

    for step, group in data.groupby("step", sort=True):
        pending = []
        for _, row in group.iterrows():
            sender, recipient, amount = str(row.nameOrig), str(row.nameDest), float(row.amount)
            sh = sender_history[sender]
            rh = recipient_history[recipient]
            prior_24 = [x for x in sh if x[0] >= step - 24]
            rec_24 = [x for x in rh if x[0] >= step - 24]
            counts = {h: sum(x[0] >= step - h for x in sh) for h in (1, 6, 24)}
            median = (
                float(np.median(sender_all_amounts[sender])) if sender_all_amounts[sender] else 0.0
            )
            output["sender_count_1h"].append(float(counts[1]))
            output["sender_count_6h"].append(float(counts[6]))
            output["sender_count_24h"].append(float(counts[24]))
            output["sender_total_amount_24h"].append(sum(x[1] for x in prior_24))
            output["sender_average_amount_24h"].append(
                float(np.mean([x[1] for x in prior_24])) if prior_24 else 0.0
            )
            output["sender_historical_median_amount"].append(median)
            output["sender_unique_recipients_24h"].append(float(len({x[2] for x in prior_24})))
            output["sender_hours_since_prior"].append(
                float(step - sender_last[sender]) if sender in sender_last else -1.0
            )
            output["amount_to_sender_median"].append(amount / median if median > 0 else 1.0)
            output["recipient_incoming_count_24h"].append(float(len(rec_24)))
            output["recipient_unique_senders_24h"].append(float(len({x[2] for x in rec_24})))
            output["recipient_total_received_24h"].append(sum(x[1] for x in rec_24))
            output["recipient_hours_since_prior"].append(
                float(step - recipient_last[recipient]) if recipient in recipient_last else -1.0
            )
            seen = pair_count[(sender, recipient)]
            output["prior_pair_count"].append(float(seen))
            output["first_time_recipient"].append(float(seen == 0))
            pending.append((sender, recipient, amount))
        for sender, recipient, amount in pending:
            sender_history[sender].append((int(step), amount, recipient))
            recipient_history[recipient].append((int(step), amount, sender))
            sender_all_amounts[sender].append(amount)
            sender_last[sender] = int(step)
            recipient_last[recipient] = int(step)
            pair_count[(sender, recipient)] += 1
    for column, values in output.items():
        data[column] = values
    return data.sort_index()
