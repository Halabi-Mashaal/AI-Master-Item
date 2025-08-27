# Error pattern detection for Master Item AI Agent

import pandas as pd

def detect_recurring_errors(log_file):
    """
    Detect recurring errors from a log file.
    """
    logs = pd.read_csv(log_file)
    error_counts = logs["error_message"].value_counts()
    recurring_errors = error_counts[error_counts > 1]
    return recurring_errors

def trace_error_sources(log_file, error_message):
    """
    Trace the sources of a specific error message.
    """
    logs = pd.read_csv(log_file)
    error_sources = logs[logs["error_message"] == error_message]["source"]
    return error_sources

if __name__ == "__main__":
    # Example usage
    log_file = "../../logs/system_logs.csv"
    print("Recurring Errors:", detect_recurring_errors(log_file))
    print("Error Sources:", trace_error_sources(log_file, "Sample Error"))
