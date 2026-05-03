import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# =========================
# 1. Load Filtered Data
# =========================
df1 = pd.read_csv("MDBFP_BRG - 2025Jun13 0000 to 2025Jun13  2300 @1 Min.csv")

# Drop missing values
df1 = df1.dropna()
df=df1.loc[
    ((df1['1LAC23CS101_XQ50.Out.Average'] >4100) &
    (df1['1LAC23CS101_XQ50.Out.Average'] <7200))]
# =========================
# 2. Create Features
# =========================




# 3. Define Inputs (X)
# =========================
feature_cols = [
    '1MdbfpC_SucFlAct.Out.Average',
    '1LAB23CP101_XQ01.Out.Average'
]

# Keep only available columns
feature_cols = [col for col in feature_cols if col in df.columns]

X = df[feature_cols]

# =========================
# 4. Define Outputs (Y)
# =========================
target_cols = [
    '1LAC03CT105_XQ02.Out.Average',
    '1LAC03CT106_XQ02.Out.Average',
    '1LAC03CT107_XQ02.Out.Average',
    '1LAC03CT108_XQ02.Out.Average'
]

Y = df[target_cols]

# =========================
# 5. Train-Test Split
# =========================
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# =========================
# 6. Model
# =========================
model = MultiOutputRegressor(
    RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
)

# Train
model.fit(X_train, Y_train)

# =========================
# 7. Prediction
# =========================
Y_pred = model.predict(X_test)

# =========================
# 8. Evaluation
# =========================
mae = mean_absolute_error(Y_test, Y_pred)
print("MAE:", mae)

# =========================
# 9. Save Model
# =========================
joblib.dump(model, "Mdbfp_thrust_model.pkl")

print("Model saved as mdbfp_model.pkl")