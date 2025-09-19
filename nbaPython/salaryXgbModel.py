import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from joblib import dump
from xgboost import XGBRegressor

data = pd.read_csv("/Users/abhik/Desktop/nbaData/masterData1.csv",index_col=0)
data = data.drop(columns="Unnamed: 0")
data = data.dropna(subset=["Salary"])

feature_cols = ["PTS", "TRB", "AST", "STL", "BLK", "TOV", "FG%", "3P%", "Age", "Pos", "GS","YOE","BPM", "VORP","WS/48"]

X = data[feature_cols]
y = data["Salary"].astype(float)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

cat_features = ["Pos"] if "Pos" in X.columns else []
num_features = [c for c in X.columns if c not in cat_features]

preprocess = ColumnTransformer(transformers=[("Pos", OneHotEncoder(handle_unknown="ignore"), cat_features),("num", "passthrough", num_features)])

xgb = XGBRegressor(
    n_estimators=500,
    learning_rate=0.01,
    max_depth=5,
    subsample=0.9,
    colsample_bytree=0.8,
    reg_alpha=0.0,
    reg_lambda=1.0,
    tree_method="hist",
    random_state=42
)

pipe = Pipeline(steps=[
    ("prep", preprocess),
    ("model", xgb)
])

pipe.fit(X_train, y_train)

pred = pipe.predict(X_test)
r2 = r2_score(y_test, pred)
rmse = root_mean_squared_error(y_test, pred)
mae = mean_absolute_error(y_test, pred)

print(f"R²:   {r2:.3f}")
print(f"RMSE: {rmse:,.2f}")
print(f"MAE:  {mae:,.2f}")

cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="r2")
print(f"CV R²: mean={cv_scores.mean():.3f}, std={cv_scores.std():.3f}")

ohe = pipe.named_steps["prep"].named_transformers_.get("Pos")
ohe_names = list(ohe.get_feature_names_out(cat_features)) if ohe else []
feature_names = ohe_names + num_features

booster = pipe.named_steps["model"]
importances = booster.feature_importances_
imp_df = pd.DataFrame({"feature": feature_names, "importance": importances})
imp_df = imp_df.sort_values("importance", ascending=False)
# print("\nTop 10 features:")
# print(imp_df.head(10).to_string(index=False))
# print(imp_df)

# Use to Save model to joblib
# dump(pipe, "xgb_salary_model.joblib")
# print("\nSaved model to xgb_salary_model.joblib")

np = pd.DataFrame([{
    "PTS": 12.4,
    "TRB": 9.6,           # must match categories seen in training
    "AST": 5.4,
    "STL": 0.6,
    "BLK": 1.8,
    "TOV": 2.1,
    "FG%": 0.534,
    "3P%": 0.418,
    "Age": 27,
    "Pos": "Pos_C",
    "GS": 75,
    "YOE": 7,
    "BPM": 8.4,
    "VORP": 0.380,
    "WS/48": 0.100
}])


pred_salary = pipe.predict(np)[0]
print(f"Predicted Salary: ${pred_salary:,.2f}")

# "YOE", 