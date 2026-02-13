import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_dashboard():
    log_file = "methodology/kaizen_events/continuous_improvement_log.csv"
    output_dir = "data/visuals"
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found.")
        return

    df = pd.read_csv(log_file)
    
    # Set style
    plt.style.use('ggplot')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
    
    # Plot 1: Muda (Waste) Reduction
    ax1.plot(df.index, df['Waste_Muda_Hrs'], color='tomato', linewidth=2, label='Muda (Waste)')
    ax1.fill_between(df.index, df['Waste_Muda_Hrs'], color='tomato', alpha=0.2)
    ax1.set_title('Waste (Muda) Reduction Curve', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Hours')
    ax1.legend()
    
    # Plot 2: PCE % Progression
    ax2.plot(df.index, df['PCE_Percent'], color='seagreen', linewidth=2, label='PCE %')
    ax2.axhline(y=90, color='gray', linestyle='--', alpha=0.5, label='90% Target')
    ax2.set_title('Process Cycle Efficiency (PCE) Progression', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Efficiency %')
    ax2.legend()
    
    # Plot 3: Sigma Stability (Variance Tightening)
    ax3.plot(df.index, df['Total_Lead_Time'], color='dodgerblue', alpha=0.4, label='Total Lead Time')
    # Rolling mean for stability visualization
    ax3.plot(df.index, df['Total_Lead_Time'].rolling(window=10).mean(), color='navy', linewidth=2, label='10-Event Moving Avg')
    ax3.axhline(y=8.5, color='red', linestyle='-', alpha=0.3, label='Standard Mean (8.5h)')
    ax3.set_title('Process Stability & Variance Tightening', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Hours')
    ax3.set_xlabel('Kaizen Iteration')
    ax3.legend()
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "kaizen_dashboard.png")
    plt.savefig(output_path, dpi=150)
    print(f"Kaizen Dashboard generated: {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_dashboard()
