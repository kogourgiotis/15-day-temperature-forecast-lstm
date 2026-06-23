# Daily Average Temperature Prediction

This project predicts the daily average temperature for the next 15 days using a machine learning pipeline based on an LSTM model.

## Project Structure

- `data_collection.py`: Collects and stores daily raw temperature data from the past 5 years.
- `preprocessing.py`: Adds temperature delta and rolling mean features, applies cyclical date encoding, and splits the data into training, validation, and test sets.
- `model.py`: Trains the model and performs predictions.

## Install dependencies (Python 3.12 required for TensorFlow)
   ```bash
   py -3.12 -m pip install --upgrade pip
   py -3.12 -m pip install openmeteo-requests pandas requests-cache retry-requests scikit-learn tensorflow matplotlib
   ```
## How to Run

1. **Set the latitude and longitude values in `data_collection.py` to match the target location.**
   
2. **Collect Data**
   ```bash
   py -3.12 data_collection.py
   ```
3. **Pre-process Data**
   ```bash
   py -3.12 preprocessing.py
   ```
4. **Train Model and Predict**
   ```bash
   py -3.12 model.py
   ```
## Prediction Summary and Visualizations

After running the model, check the **Results** folder for:

- The **predictions.csv** file containing the predicted daily average temperatures.
- The training metrics plot visualizing MAE and MSE over epochs.
