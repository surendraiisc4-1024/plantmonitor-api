import pandas as pd
import numpy as np
import glob
import os

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# =========================
# 1. LOAD MULTIPLE FILES
# =========================

folder_path = r"C:\Users\User\PycharmProjects\stocks\Isolation forest for BFP parameters\BFP_Pump_Model\plant_data\New folder\mathemetical model\New Folder\MDBFP Data\MDBFP"   # 👈 CHANGE THIS

csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

all_dfs = []

# Read CSV files
for file in csv_files:
    try:
        df = pd.read_csv(file)
        if not df.empty:
            print(f"Loaded CSV: {file}, Shape: {df.shape}")
            all_dfs.append(df)
        else:
            print(f"Skipped empty CSV: {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Read Excel files
for file in excel_files:
    try:
        df = pd.read_excel(file)
        if not df.empty:
            print(f"Loaded Excel: {file}, Shape: {df.shape}")
            all_dfs.append(df)
        else:
            print(f"Skipped empty Excel: {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Combine all data
if len(all_dfs) == 0:
    raise ValueError("No valid data files found!")

df1 = pd.concat(all_dfs, ignore_index=True)

print("\nTotal combined data shape:", df1.shape)

# =========================
# 2. CLEAN DATA
# =========================

df1 = df1.dropna()

print("After dropna:", df1.shape)

# =========================
# 3. FILTER DATA
# =========================

df = df1.loc[
    ((df1['1LAC23CS101_XQ50.Out.Average'] > 1100) &
     (df1['1LAC23CS101_XQ50.Out.Average'] < 7200))
]

print("After filtering:", df.shape)

# =========================
# 4. DEFINE FEATURES (X)
# =========================

feature_cols = [
    '1MdbfpC_SucFlAct.Out.Average',
    '1LAB23CP101_XQ01.Out.Average'
]

# Ensure columns exist
feature_cols = [col for col in feature_cols if col in df.columns]

if len(feature_cols) == 0:
    raise ValueError("No valid feature columns found!")

X = df[feature_cols]

print("Feature columns:", feature_cols)

# =========================
# 5. DEFINE TARGETS (Y)
# =========================

target_cols = [
    '1LAC03CT105_XQ02.Out.Average',
    '1LAC03CT106_XQ02.Out.Average',
    '1LAC03CT107_XQ02.Out.Average',
    '1LAC03CT108_XQ02.Out.Average'
]

# Ensure all targets exist
target_cols = [col for col in target_cols if col in df.columns]

if len(target_cols) == 0:
    raise ValueError("No valid target columns found!")

Y = df[target_cols]

print("Target columns:", target_cols)

# =========================
# 6. FINAL CHECK
# =========================

print("X shape:", X.shape)
print("Y shape:", Y.shape)

if X.shape[0] == 0:
    raise ValueError("No data available after filtering!")

# =========================
# 7. TRAIN-TEST SPLIT
# =========================

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# =========================
# 8. MODEL
# =========================

model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
)

# Train
model.fit(X_train, Y_train)

# =========================
# 9. PREDICTION
# =========================

Y_pred = model.predict(X_test)

# =========================
# 10. EVALUATION
# =========================

mae = mean_absolute_error(Y_test, Y_pred)
print("\nModel MAE:", mae)

# =========================
# 11. SAVE MODEL
# =========================

model_path = "Mdbfp_thrust_model1.pkl"
joblib.dump(model, model_path)

print(f"\nModel saved as: {model_path}")