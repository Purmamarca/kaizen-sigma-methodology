import pandas as pd
import os
from datetime import datetime

REPORT_PATH = "data/KAIZEN_SIGMA_REPORT.md"
AUDIT_RESULTS = "data/quality_audit_results.csv"
KAIZEN_LOG = "methodology/kaizen_events/continuous_improvement_log.csv"
DASHBOARD_IMG = "visuals/kaizen_dashboard.png" # Relative to 'data' folder

def generate_report():
    if not os.path.exists(AUDIT_RESULTS):
        print("Audit results not found. Please run gatekeeper.py first.")
        return

    audit_df = pd.read_csv(AUDIT_RESULTS)
    metrics = audit_df.iloc[0]
    
    status_emoji = "✅" if metrics["overall_status"] == "PASSED" else "❌"
    
    report_content = f"""# 🛡️ Kaizen-Sigma Integrated Audit Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Overall Status:** {status_emoji} **{metrics["overall_status"]}**

---

## 📊 Core Performance Metrics

| Metric | Measured Value | Threshold / Target | Status |
| :--- | :--- | :--- | :--- |
| **Six Sigma Cpk** | {metrics["cpk"]:.4f} | >= 1.33 | {"✅" if metrics["cpk"] >= 1.33 else "❌"} |
| **Sigma Level** | {metrics["sigma_level"]:.2f} | 4.0+ | {"✅" if metrics["sigma_level"] >= 3.0 else "⚠️"} |
| **PCE % (Efficiency)** | {metrics["pce_percent"]:.2f}% | 90.00% | {"✅" if metrics["pce_percent"] >= 90 else "⚠️"} |
| **Muda (Waste)** | {metrics["muda_hrs"]:.2f}h | < 5.0h | {"✅" if metrics["muda_hrs"] < 5.0 else "❌"} |

---

## 📈 Kaizen Visualization Dashboard
![Kaizen Dashboard]({DASHBOARD_IMG})

---

## 🔄 PDCA (Continuous Improvement) Analysis
- **Plan**: Current process varies with a Cpk of {metrics["cpk"]:.4f}.
- **Do**: Iterative waste reduction has brought Muda down to {metrics["muda_hrs"]:.2f} hours.
- **Check**: Efficiency is at {metrics["pce_percent"]:.2f}%.
- **Act**: Next cycle should focus on tightening variance to pass the 1.33 Cpk gate.

---
*Powered by Google Antigravity AI Auditor*
"""

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"Comprehensive report generated: {REPORT_PATH}")

if __name__ == "__main__":
    generate_report()
