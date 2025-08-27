# Translating operational logs into business KPIs for Master Item AI Agent

import pandas as pd
import matplotlib.pyplot as plt

# Load logs
def load_logs(log_file):
    return pd.read_csv(log_file)

def calculate_kpis(logs):
    """
    Calculate business KPIs from logs.
    """
    kpis = {
        "Duplicate Prevention ROI": logs["duplicates_prevented"].sum() * 100,
        "Data Quality Impact on On-Time Delivery": logs["on_time_delivery"].mean(),
        "New Product Introduction Cycle Time": logs["cycle_time"].mean()
    }
    return kpis

def generate_dashboard(kpis):
    """
    Generate a dashboard for KPIs.
    """
    plt.bar(kpis.keys(), kpis.values())
    plt.title("Business KPIs")
    plt.show()

if __name__ == "__main__":
    # Example usage
    log_file = "../../logs/system_logs.csv"
    logs = load_logs(log_file)
    kpis = calculate_kpis(logs)
    print("KPIs:", kpis)
    generate_dashboard(kpis)
