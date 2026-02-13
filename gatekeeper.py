import pandas as pd
import os
import sys
import re
from auditor.logic import calculate_six_sigma_metrics, calculate_pce_metrics

# Specification Limits for Six Sigma Audit
USL = 103.0
LSL = 97.0
TARGET = 100.0
MIN_CPK_THRESHOLD = 1.33  # Four Sigma Quality gate

def parse_standards():
    standards_file = "methodology/standard_work/process_standards.md"
    if not os.path.exists(standards_file):
        print(f"Warning: Standards file {standards_file} not found.")
        return None
    
    with open(standards_file, "r") as f:
        content = f.read()
    
    standards = {}
    # Extract values using regex - looking for the specific format in process_standards.md
    mean_match = re.search(r"Target Process Mean:\*\* ([\d.]+) Hours", content)
    std_match = re.search(r"Standard Deviation Limit:\*\* ([\d.]+) Hours", content)
    muda_match = re.search(r"Muda Threshold:\*\* Any 'Waste_Muda_Hrs' > ([\d.]+)h", content)
    
    if mean_match: standards["target_mean"] = float(mean_match.group(1))
    if std_match: standards["std_limit"] = float(std_match.group(1))
    if muda_match: standards["muda_threshold"] = float(muda_match.group(1))
    
    return standards

def run_gatekeeper():
    input_file = "data/raw_measurements.csv"
    kaizen_file = "methodology/kaizen_events/continuous_improvement_log.csv"
    output_file = "data/quality_audit_results.csv"
    
    print("\n" + "="*50)
    print("KAIZEN-SIGMA GATEKEEPER: INTEGRATED AUDIT")
    print("="*50)

    # 1. Six Sigma Audit
    if not os.path.exists(input_file):
        print(f"Error: Raw measurements file {input_file} not found.")
        sys.exit(1)
        
    df = pd.read_csv(input_file)
    measurements = df["measurement"].values
    sigma_metrics = calculate_six_sigma_metrics(measurements, USL, LSL, TARGET)
    cpk = sigma_metrics["cpk"]
    
    # 2. Kaizen & PCE Audit
    if os.path.exists(kaizen_file):
        kaizen_df = pd.read_csv(kaizen_file)
        latest_kaizen = kaizen_df.iloc[-1]
        pce_metrics = calculate_pce_metrics(latest_kaizen["Value_Add_Hrs"], latest_kaizen["Total_Lead_Time"])
        
        # Longitudinal check (last 10 events)
        avg_pce = kaizen_df.tail(10)["PCE_Percent"].mean()
    else:
        pce_metrics = {"pce_percent": 0.0, "muda_hrs": 0.0}
        avg_pce = 0.0

    # 3. PDCA Standards Verification
    standards = parse_standards()
    pdca_passed = True
    pdca_reasons = []

    if standards and os.path.exists(kaizen_file):
        # Check against Muda threshold
        muda = pce_metrics["muda_hrs"]
        # In methodology/standard_work/process_standards.md, it's actually:
        # 1. **Target Process Mean:** 8.5 Hours
        # 2. **Standard Deviation Limit:** 1.2 Hours
        # 3. **Muda Threshold:** Any 'Waste_Muda_Hrs' > 5h triggers a Kaizen Blitz.
        
        if muda > standards.get("muda_threshold", 5.0):
            pdca_passed = False
            pdca_reasons.append(f"Muda ({muda:.2f}h) exceeds limit ({standards['muda_threshold']}h)")
        
        # Check against Mean stability (latest value vs target)
        latest_mean = latest_kaizen["Value_Add_Hrs"]
        if abs(latest_mean - standards.get("target_mean", 8.5)) > 0.5:
            pdca_passed = False
            pdca_reasons.append(f"Latest Mean ({latest_mean:.2f}h) drifted from standard ({standards['target_mean']}h)")

    # Reporting
    passed = (cpk >= MIN_CPK_THRESHOLD) and pdca_passed
    
    print(f"--- Six Sigma Results ---")
    print(f"Measured Cpk:  {cpk:.4f} (Threshold: {MIN_CPK_THRESHOLD})")
    print(f"Sigma Level:   {sigma_metrics['sigma_level']:.2f}")
    
    print(f"\n--- Kaizen/PCE Results ---")
    print(f"Latest PCE:    {pce_metrics['pce_percent']:.2f}%")
    print(f"Latest Muda:   {pce_metrics['muda_hrs']:.2f}h")
    print(f"Rolling PCE:   {avg_pce:.2f}% (last 10 events)")
    
    print(f"\n--- PDCA Status ---")
    if pdca_passed:
        print("Standards Verification: PASSED")
    else:
        print("Standards Verification: FAILED")
        for reason in pdca_reasons:
            print(f"   - {reason}")

    print("\n" + "="*50)
    print(f"OVERALL STATUS: {'PASSED' if passed else 'FAILED'}")
    print("="*50 + "\n")

    # Export metrics for pipeline
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a") as f:
            f.write(f"MEASURED_CPK={cpk:.4f}\n")
            f.write(f"MEASURED_PCE={pce_metrics['pce_percent']:.2f}\n")
    
    # Save results
    results_df = pd.DataFrame([{**sigma_metrics, **pce_metrics, "overall_status": "PASSED" if passed else "FAILED"}])
    if not os.path.exists("data"):
        os.makedirs("data")
    results_df.to_csv(output_file, index=False)
    
    if not passed:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    run_gatekeeper()
