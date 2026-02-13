import pandas as pd
import os
import re

STANDARDS_FILE = "methodology/standard_work/process_standards.md"
KAIZEN_LOG = "methodology/kaizen_events/continuous_improvement_log.csv"

def update_standards():
    if not os.path.exists(KAIZEN_LOG) or not os.path.exists(STANDARDS_FILE):
        print("Missing required files for PDCA Act phase.")
        return

    df = pd.read_csv(KAIZEN_LOG)
    if len(df) < 5:
        print("Not enough data to update standards (need 5+ events).")
        return

    # Analyze latest performance
    recent_events = df.tail(5)
    avg_value_add = recent_events["Value_Add_Hrs"].mean()
    avg_pce = recent_events["PCE_Percent"].mean()
    
    # We only update the standard if performance has stabilized at a better level
    # For this simulation, let's say "better" means Mean is closer to 8.0 or PCE is higher
    
    with open(STANDARDS_FILE, "r") as f:
        content = f.read()

    current_mean_match = re.search(r"Target Process Mean:\*\* ([\d.]+) Hours", content)
    if current_mean_match:
        current_mean = float(current_mean_match.group(1))
        
        # If stabilized performance is significantly different, update the standard (The Wedge)
        if abs(avg_value_add - current_mean) > 0.3:
            print(f"Detected performance shift: {current_mean}h -> {avg_value_add:.2f}h")
            new_content = re.sub(
                r"Target Process Mean:\*\* [\d.]+ Hours",
                f"Target Process Mean:** {avg_value_add:.2f} Hours",
                content
            )
            
            # Also update PCE benchmark in documentation if present (or just the timestamp)
            new_content = re.sub(
                r"_Ref: Page 254 - Preventing Quality Backslide_",
                f"_Ref: Page 254 - Updated Standardized Work at {pd.Timestamp.now().strftime('%Y-%m-%d')}_",
                new_content
            )
            
            with open(STANDARDS_FILE, "w") as f:
                f.write(new_content)
            print("Successfully updated process_standards.md (Standardization Wedge applied).")
        else:
            print("Performance stable. No update to standards required.")

if __name__ == "__main__":
    update_standards()
