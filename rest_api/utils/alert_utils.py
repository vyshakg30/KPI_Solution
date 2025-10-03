from typing import List, Dict


def add_alert_baseline_delta(alerts: List[Dict], keys: List[str] = ["default_spiked", "volume_droped"]):
    """
    Add baseline and delta for boolean alert flags.
    
    alerts: list of alert dicts with 'alert_date' and boolean keys
    keys: list of alert keys to compute baseline/delta
    """
    # Keep track of previous values
    prev = {k: None for k in keys}

    for alert in alerts:
        for k in keys:
            current = alert.get(k)
            alert[f"{k}_baseline"] = prev[k]

            if prev[k] is None or current is None:
                alert[f"{k}_delta"] = None
            else:
                # True->False = -1, False->True = 1, same = 0
                alert[f"{k}_delta"] = int(current) - int(prev[k])

            # update previous
            if current is not None:
                prev[k] = current

    return alerts
