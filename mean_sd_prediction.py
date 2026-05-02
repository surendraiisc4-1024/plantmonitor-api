import pandas as pd
import joblib
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Load test data
y = pd.read_excel("Journalbearing_test_data.xlsx")
y['BFP_deT-loT'] = y['1LAC01CT103XQ10.OUT.Average']-y['1BFPDTA_LO_TEMP.OUT.Average']

feature_cols = [
    '1ALO_HDR_PRES.out.Average',
    '1LAC01CT103XQ10.OUT.Average',
    '1LAC01CT104XQ10.OUT.Average',
    '1ASUCCFLOW_BOP.OUT.Average',
    '1BFPDTA_SPD_MV3.OUT.Average',
    '1BFPDTA_LO_TEMP.OUT.Average',
    '1LAB21CP102XQ10.OUT.Average',
    'BFP_deT-loT'
]

# Get speed value from test row
speed = y['1BFPDTA_SPD_MV3.OUT.Average'].iloc[0]

# Find correct band
band_start = int(speed // 100) * 100
band_end = band_start + 100

print(f"Using band: {band_start}-{band_end}")

# Load corresponding scaler
scaler = joblib.load(f"models/scaler_{band_start}_{band_end}.pkl")

# Apply scaling
y_selected = y[feature_cols]
z=y[feature_cols]-scaler["mean"]
y_zscore = z/scaler["std"]
print(y_selected)
print('deviation from mean:', z)
print('sd value', y_zscore)
