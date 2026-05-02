import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from sklearn.preprocessing import StandardScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# =========================
# 1. Load Filtered Data
# =========================
df1 = pd.read_csv("Journalbearing_filtered_data.csv")

# Drop missing values
df1 = df1.dropna()

# =========================
# 2. Create Features
# =========================
df=df1.loc[
    ((df1['1BFPDTA_SPD_MV3.OUT.Average'] >4100) &
    (df1['1BFPDTA_SPD_MV3.OUT.Average'] <4200))]

# Combine discharge pressure (if both exist)
#if '1LAB21CP102XQ10.OUT.Average' in df.columns and '1LAB21CP101_XQ01.Out.Average' in df.columns:
 #   df['BFP_deT-loT'] = df[
  #      ['1LAB21CP102XQ10.OUT.Average', '1LAB21CP101_XQ01.Out.Average']
   # ].mean(axis=1)
df['BFP_deT-loT'] = df['1LAC01CT103XQ10.OUT.Average']-df['1BFPDTA_LO_TEMP.OUT.Average']
# =========================
# 3. Define Inputs (X)
# =========================
feature_cols = [
    #'1LOAD_ACTUAL_MV3.out.Average',
    '1ALO_HDR_PRES.out.Average',
    '1LAC01CT103XQ10.OUT.Average',
    '1LAC01CT104XQ10.OUT.Average',
    '1ASUCCFLOW_BOP.OUT.Average',
    '1BFPDTA_SPD_MV3.OUT.Average',
    '1BFPDTA_LO_TEMP.OUT.Average',
    '1LAB21CP102XQ10.OUT.Average',
    'BFP_deT-loT'

    #'Delta_Pressure'
]

# Keep only available columns
feature_cols = [col for col in feature_cols if col in df.columns]

X = df[feature_cols]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(X_scaled.mean())
print(np.mean(X, axis=0))
mean_vector = np.mean(X, axis=0)
std_vector = np.std(X, axis=0)
print(std_vector)
print(X.shape)

y=pd.read_excel("Journalbearing_test_data.xlsx")
y['BFP_deT-loT'] = y['1LAC01CT103XQ10.OUT.Average']-y['1BFPDTA_LO_TEMP.OUT.Average']
print(y[feature_cols])
z=y[feature_cols]-mean_vector
y_zscore = z/std_vector
print('deviation from mean:', z)
print('sd value', y_zscore)



