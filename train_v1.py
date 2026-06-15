import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

def main():
    csv_path = 'f1_v1_data.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please run the fetch_data_v1.py script first.")
        return
        
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Dataset loaded. Total rows: {len(df)}")
    
    # Define target classes:
    # 0: Top 3 (Podium)
    # 1: Top 10 (Points)
    # 2: Outside Top 10 (No points)
    def classify_outcome(pos):
        if pos <= 3:
            return 0
        elif pos <= 10:
            return 1
        else:
            return 2
            
    df['target'] = df['finish_position'].apply(classify_outcome)
    
    # Display class distribution
    print("\nClass Distribution:")
    print(df['target'].value_counts(normalize=True))
    
    # Split chronologically: Train on 2021-2024, Test on 2025-2026
    # If 2025/2026 data is small or empty, we will fall back to a standard random split.
    test_seasons = [2025, 2026]
    has_test_seasons = df['season'].isin(test_seasons).sum() > 20
    
    if has_test_seasons:
        print(f"\nSplitting data chronologically: Train (<2025) vs Test (>=2025)...")
        train_df = df[~df['season'].isin(test_seasons)]
        test_df = df[df['season'].isin(test_seasons)]
    else:
        print("\nNot enough data in 2025/2026 for testing. Falling back to a 80-20 random train/test split...")
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['target'])
        
    features = ['season', 'circuit', 'team', 'grid_position']
    X_train = train_df[features]
    y_train = train_df['target']
    X_test = test_df[features]
    y_test = test_df['target']
    
    print(f"Training size: {len(X_train)} rows")
    print(f"Testing size: {len(X_test)} rows")
    
    # Preprocessing pipeline
    categorical_features = ['circuit', 'team']
    numerical_features = ['grid_position', 'season']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # Define pipeline with RandomForestClassifier
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42,
            class_weight='balanced'  # handles class imbalance
        ))
    ])
    
    # Train the model
    print("\nTraining RandomForestClassifier...")
    pipeline.fit(X_train, y_train)
    
    # Predictions
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    print(f"\nOverall Test Accuracy: {acc:.4f}")
    
    print("\nClassification Report:")
    target_names = ['Top 3 (Podium)', 'Top 10 (Points)', 'Outside Top 10']
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature Importances (from classifier)
    # We can inspect feature names from the column transformer
    ohe = pipeline.named_steps['preprocessor'].named_transformers_['cat']
    cat_encoder_features = ohe.get_feature_names_out(categorical_features).tolist()
    feature_names = numerical_features + cat_encoder_features
    
    importances = pipeline.named_steps['classifier'].feature_importances_
    indices = np.argsort(importances)[::-1]
    
    print("\nTop 10 Feature Importances:")
    for f in range(min(10, len(feature_names))):
        print(f"{f + 1}. {feature_names[indices[f]]}: {importances[indices[f]]:.4f}")
        
    # Save the trained pipeline to a file
    model_filename = 'f1_model_v1.pkl'
    joblib.dump(pipeline, model_filename)
    print(f"\nTrained model pipeline saved successfully as '{model_filename}'")
    
if __name__ == '__main__':
    main()
