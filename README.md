# Kaizen-Sigma Methodology: Lattice Auditor 🛡️📉

> **Continuous Improvement (PDCA) meets Statistical Rigor (Six Sigma).**

Welcome to the **Kaizen-Sigma Methodology** repository. This project is a specialized transformation of the Sigma Lattice Auditor, pivoted towards a Kaizen-centered framework for continuous measurement, waste reduction (**Muda**), and standardized work stability.

---

## 🏗️ The Kaizen-Sigma Framework

This repository implements the **Continuous Improvement Loop (PDCA)** as a core engine for process reliability:

1.  **Plan**: Analyze logs for variance and waste (Muda).
2.  **Do**: Execute iterative improvements and data generation.
3.  **Check**: Verify stability against the **Standardization Wedge**.
4.  **Act**: Update standards to prevent quality backslide.

---

## 📊 Core Components

### 🔄 PDCA Engine (`scripts/audit_engine/`)

An automated audit engine that models the evolution of process maturity.

- **`kaizen_data_gen.py`**: Generates synthetic audit logs.
- **`pdca_act.py`**: Automatically updates the "Standardization Wedge" when performance peaks are reached.
- **`kaizen_dashboard.py`**: Generates visual performance charts (Muda Decay, PCE Progression).
- **`generate_report.py`**: Creates a comprehensive `KAIZEN_SIGMA_REPORT.md` artifact.

### 📜 Methodology & Standards (`methodology/`)

- **`kaizen_events/`**: Stores continuous improvement logs (`continuous_improvement_log.csv`).
- **`standard_work/`**: Contains the **Process Standards Wedge** (`process_standards.md`), defining the current "Best Practice" benchmarks.

---

## 🚀 Getting Started

### 📦 Installation

Ensure you have Python 3.11+ and a virtual environment ready:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 🛠️ Running the Kaizen Cycle

1.  **Execute the Integrated Audit Pipeline**:

    ```powershell
    # Generate data and evaluate against standards
    python scripts/audit_engine/kaizen_data_gen.py
    $env:PYTHONPATH = "src"; python gatekeeper.py
    ```

2.  **Generate Visual Reports**:
    ```powershell
    python scripts/audit_engine/kaizen_dashboard.py
    python scripts/audit_engine/generate_report.py
    ```
    Review `data/KAIZEN_SIGMA_REPORT.md` for a full breakdown of Six Sigma and Kaizen metrics.

---

## 📈 Quality Metrics Verified

- **Cpk (Process Capability)**: Statistical rigor to ensure < 0.1% defect rate.
- **PCE % (Process Cycle Efficiency)**: Ratio of value-add time to total lead time.
- **Muda Reduction**: Exponential decay tracking of non-value-add hours.
- **Standardization Wedge**: Automated protection against quality backsliding.

---

## 🛡️ Governance & Safety

Powered by the **Antigravity AI Auditor**, enforcing a **"Stop-the-Line"** policy via the `antigravity.yaml` CI configuration.
Every commit is audited for statistical stability and process efficiency before being merged.

---

_Ref: Kaizen Continuous Improvement (Pages 247-254)_
