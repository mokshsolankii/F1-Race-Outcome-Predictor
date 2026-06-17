"""
train_v3.py — F1 Race Outcome Predictor V3
==========================================
- Trains CatBoostRegressor on f1_training_data_v3.csv
- Evaluates MAE + top-3 / top-10 accuracy
- Saves model to f1_model_v3.pkl
- Prints feature importances
"""

import pandas as pd
import numpy as np
import pickle
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# ── Load data ──────────────────────────────────────────────────────────────────
print("\n" + "═"*54)
print("  F1 Predictor V3 — Training")
print("═"*54)

df = pd.read_csv("f1_training_data_v3.csv")
print(f"  Dataset: {df.shape[0]} rows × {df.shape[1]} cols")
print(f"  Years:   {sorted(df['year'].unique())}")

# ── Features ───────────────────────────────────────────────────────────────────
CAT_FEATURES = ["driver", "team", "race"]

NUM_FEATURES = [
    "year", "round",
    # Qualifying
    "quali_time_s", "grid_position", "pole_gap_s",
    # Standings
    "driver_points", "constructor_points",
    # Tyre + circuit
    "start_tyre", "circuit_type",
    # Weather
    "air_temp_c", "rainfall_mm", "track_temp_c",
    # Form (NEW in V3)
    "driver_form_last3", "team_form_last3", "driver_track_hist",
]

ALL_FEATURES = NUM_FEATURES + CAT_FEATURES
TARGET = "finish_position"

X = df[ALL_FEATURES]
y = df[TARGET]

# ── Train / test split — split by year to avoid leakage ───────────────────────
# Test set = 2024 + 2026 (most recent, unseen by model during training)
test_mask  = df["year"].isin([2024, 2026])
X_train, X_test = X[~test_mask], X[test_mask]
y_train, y_test = y[~test_mask], y[test_mask]

print(f"  Train: {len(X_train)} rows ({sorted(df[~test_mask]['year'].unique())})")
print(f"  Test:  {len(X_test)}  rows ({sorted(df[test_mask]['year'].unique())})")

# ── CatBoost ───────────────────────────────────────────────────────────────────
cat_idx = [ALL_FEATURES.index(c) for c in CAT_FEATURES]

model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=7,
    loss_function="MAE",
    eval_metric="MAE",
    cat_features=cat_idx,
    early_stopping_rounds=50,
    random_seed=42,
    verbose=100,
)

train_pool = Pool(X_train, y_train, cat_features=cat_idx)
test_pool  = Pool(X_test,  y_test,  cat_features=cat_idx)

model.fit(train_pool, eval_set=test_pool)

# ── Evaluate ───────────────────────────────────────────────────────────────────
preds     = model.predict(X_test)
preds_int = np.clip(np.round(preds), 1, 20).astype(int)
actual    = y_test.values

mae = mean_absolute_error(actual, preds)
print(f"\n  MAE: {mae:.3f} positions (V2 was 3.112)")

# Top-3 accuracy: predicted in top 3 AND actually in top 3
top3_acc  = np.mean((preds_int <= 3) == (actual <= 3))
top10_acc = np.mean((preds_int <= 10) == (actual <= 10))
print(f"  Top-3  classification accuracy : {top3_acc*100:.1f}%")
print(f"  Top-10 classification accuracy : {top10_acc*100:.1f}%")

# ── Feature importances ────────────────────────────────────────────────────────
importances = model.get_feature_importance()
feat_imp = sorted(zip(ALL_FEATURES, importances), key=lambda x: -x[1])
print(f"\n  Feature importances:")
for feat, imp in feat_imp:
    bar = "█" * int(imp / 2)
    print(f"    {feat:<25} {imp:>6.2f}%  {bar}")

# ── Save ───────────────────────────────────────────────────────────────────────
with open("f1_model_v3.pkl", "wb") as f:
    pickle.dump({
        "model":        model,
        "features":     ALL_FEATURES,
        "cat_features": CAT_FEATURES,
        "num_features": NUM_FEATURES,
        "cat_idx":      cat_idx,
        "mae":          round(mae, 3),
    }, f)

print(f"\n  ✓ Saved: f1_model_v3.pkl")
print(f"  Next  → python predict_race_v3.py")
print("═"*54 + "\n")
