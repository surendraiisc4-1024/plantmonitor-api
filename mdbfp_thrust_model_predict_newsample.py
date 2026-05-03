import pandas as pd
import joblib
import numpy as np

# =========================
# 1. Load Model
# =========================
model = joblib.load("Mdbfp_thrust_model1.pkl")

# =========================
# 2. Read Sample Excel File
# =========================
sample_file = "sample_data.csv"

df1 = pd.read_csv(sample_file)

# Clean column names
df1.columns = df1.columns.str.strip()
df = df1.loc[
    ((df1['1LAC23CS101_XQ50.Out.Average'] > 1100) &
     (df1['1LAC23CS101_XQ50.Out.Average'] < 7200))
]

# =========================
# 3. Create Required Features
# =========================




# =========================
# 4. Select Features (same as training)
# =========================
feature_cols = [
    '1MdbfpC_SucFlAct.Out.Average',
    '1LAB23CP101_XQ01.Out.Average'
]

# Ensure all exist
feature_cols = [col for col in feature_cols if col in df.columns]

X = df[feature_cols]

# =========================
# 5. Predict
# =========================
predictions = model.predict(X)

# =========================
# 6. Compare with Actual
# =========================
target_cols = [
    '1LAC03CT105_XQ02.Out.Average',
    '1LAC03CT106_XQ02.Out.Average',
    '1LAC03CT107_XQ02.Out.Average',
    '1LAC03CT108_XQ02.Out.Average'
]

if all(col in df.columns for col in target_cols):

    actual = df[target_cols].values
    deviation = actual - predictions

    for i in range(len(df)):
        print(f"\n--- Sample {i + 1} ---")

        for j in range(4):
            print(f"Bearing {j + 1}: Pred={predictions[i][j]:.2f}, "
                  f"Actual={actual[i][j]:.2f}, Dev={deviation[i][j]:.2f}")

            if abs(deviation[i][j]) > 7:
                print("  → 🔴 Critical")
            elif abs(deviation[i][j]) > 3:
                print("  → 🟠 Warning")
            else:
                print("  → 🟢 Normal")

# =========================
# 7. Save Results
# =========================
result_df = df.copy()

for i in range(4):
    result_df[f'Pred_Temp_{i + 1}'] = predictions[:, i]

result_df.to_excel("prediction_results.xlsx", index=False)

print("\n✅ Results saved to prediction_results.xlsx")