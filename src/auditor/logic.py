import numpy as np


def calculate_six_sigma_metrics(data, usl, lsl, target=None):
    """
    Calculate Six Sigma quality metrics: Cp, Cpk, and Sigma Level.
    """
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    if std == 0:
        return {
            "mean": mean,
            "std": std,
            "cp": float('inf'),
            "cpk": float('inf'),
            "sigma_level": float('inf')
        }
    
    cp = (usl - lsl) / (6 * std)
    cpk = min((usl - mean) / (3 * std), (mean - lsl) / (3 * std))
    
    # Sigma level is usually calculated as Z-score
    sigma_level = min((usl - mean) / std, (mean - lsl) / std)
    
    return {
        "mean": float(mean),
        "std": float(std),
        "cp": float(cp),
        "cpk": float(cpk),
        "sigma_level": float(sigma_level)
    }


def calculate_pce_metrics(value_add_time, total_lead_time):
    """
    Calculate Process Cycle Efficiency (PCE) and Muda (Waste).
    """
    if total_lead_time == 0:
        return {"pce_percent": 0.0, "muda_hrs": 0.0}
    
    pce = (value_add_time / total_lead_time) * 100
    muda = total_lead_time - value_add_time
    
    return {
        "pce_percent": float(pce),
        "muda_hrs": float(muda)
    }
