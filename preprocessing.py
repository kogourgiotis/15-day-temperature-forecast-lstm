import pandas as pd
import numpy as np

# Load and prepare data
df = pd.read_csv("dataset.csv", parse_dates=['date'])
df['day_of_year'] = df['date'].dt.dayofyear

# Add temperature delta and rolling mean features
df['temp_delta'] = df['temperature_2m_mean'].shift(1) - df['temperature_2m_mean'].shift(2)
df['rolling_mean_3'] = df['temperature_2m_mean'].shift(1).rolling(window=3).mean()
df['rolling_mean_7'] = df['temperature_2m_mean'].shift(1).rolling(window=7).mean()

# Train/test split
df = df.dropna().reset_index(drop=True)
train_data = df.iloc[:-15].copy()
test_data = df.iloc[-15:].copy()

# Validation split from train set
validation_percent = 0.1
validation_start_index = int(train_data.shape[0] * validation_percent)
val_data = train_data[-validation_start_index:].copy()
train_data = train_data[:-validation_start_index].copy()

# Cyclical encoding
for dataset in [train_data, val_data, test_data]:
    dataset['day_sin'] = np.sin(2 * np.pi * dataset['day_of_year'] / 365)
    dataset['day_cos'] = np.cos(2 * np.pi * dataset['day_of_year'] / 365)

# Select final columns
final_features = ['date', 'day_sin', 'day_cos',
    'temperature_2m_mean', 'temperature_2m_max', 'temperature_2m_min',
    'temp_delta', 'rolling_mean_3', 'rolling_mean_7']

train_df = train_data[final_features]
val_df = val_data[final_features]
test_df = test_data[final_features]

# Save to CSV
train_df.to_csv("train_set.csv", index=False)
val_df.to_csv("validation_set.csv", index=False)
test_df.to_csv("test_set.csv", index=False)