import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix

def train_and_save_model(data_path, model_dir):
    print("Loading student dataset...")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Please run generate_data.py first.")
        
    df = pd.read_csv(data_path)
    
    # Define features and target
    X = df[['Subject', 'Attendance_Rate', 'Study_Hours', 'Midterm_Score', 'Past_Score']]
    y = df['At_Risk']
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training set size: {X_train.shape[0]} rows")
    print(f"Testing set size: {X_test.shape[0]} rows")
    
    # Preprocessing pipelines for numerical and categorical features
    numeric_features = ['Attendance_Rate', 'Study_Hours', 'Midterm_Score', 'Past_Score']
    categorical_features = ['Subject']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )
    
    # Define the individual classifiers
    rf_clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=6,
        random_state=42,
        class_weight='balanced'
    )
    
    lr_clf = LogisticRegression(
        random_state=42,
        class_weight='balanced',
        max_iter=1000
    )
    
    # Define the soft voting ensemble
    ensemble = VotingClassifier(
        estimators=[('rf', rf_clf), ('lr', lr_clf)],
        voting='soft',
        weights=[1.2, 0.8]  # Give slightly more weight to RF
    )
    
    # Create the complete pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', ensemble)
    ])
    
    print("Training Random Forest + Logistic Regression Ensemble Model...")
    pipeline.fit(X_train, y_train)
    
    # Predictions and evaluation
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_proba)
    
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC Score: {auc_score:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Ensure models directory exists
    os.makedirs(model_dir, exist_ok=True)
    
    # Save the pipeline
    model_path = os.path.join(model_dir, "ensemble_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
        
    print(f"\nModel pipeline successfully saved to: {model_path}")

if __name__ == "__main__":
    train_and_save_model(
        "D:/lenovo LEAP/Capstone Project/data/student_data.csv",
        "D:/lenovo LEAP/Capstone Project/models"
    )
