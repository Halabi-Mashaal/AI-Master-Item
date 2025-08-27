# Inventory optimization code for Master Item AI Agent

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load dataset
data = pd.read_csv("../../data/master_item_dataset/sample_master_item_data.csv")

# Example: Time-series analysis for inventory optimization
item_usage = data["usage"]

# Fit model
model = ExponentialSmoothing(item_usage, seasonal="add", seasonal_periods=12)
fit = model.fit()

# Forecast
forecast = fit.forecast(12)
print("Forecast:", forecast)
