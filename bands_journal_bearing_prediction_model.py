import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

df1 = pd.read_csv("Journalbearing_filtered_data.csv").dropna()
df1['BFP_deT-loT'] = df1['1LAC01CT103XQ10.OUT.Average']-df1['1BFPDTA_LO_TEMP.OUT.Average']

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

feature_cols = [col for col in feature_cols if col in df1.columns]

os.makedirs("models", exist_ok=True)

for start in range(4000, 5200, 100):
    end = start + 100

    df = df1.loc[
        (df1['1BFPDTA_SPD_MV3.OUT.Average'] > start) &
        (df1['1BFPDTA_SPD_MV3.OUT.Average'] <= end)
    ]

    if df.empty:
        continue

    X = df[feature_cols]
    mean_vector = np.mean(X, axis=0)
    std_vector = np.std(X, axis=0)
    model_data = {
        "mean": mean_vector,
        "std": std_vector
    }

    filename = f"models/scaler_{start}_{end}.pkl"
    joblib.dump(model_data, filename)
    print(f"Saved model for band {start}-{end}")
