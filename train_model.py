import os
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.pipeline import Pipeline
import xgboost as xgb

SEED = 42
np.random.seed(SEED)

def generate_placement_dataset(n_samples=300):
    """Generates a generalized campus recruitment dataset across engineering, technology, management, & arts."""
    genders = np.random.choice(['M', 'F'], size=n_samples, p=[0.60, 0.40])
    ssc_b = np.random.choice(['Central', 'Others'], size=n_samples, p=[0.55, 0.45])
    hsc_b = np.random.choice(['Central', 'Others'], size=n_samples, p=[0.45, 0.55])
    hsc_s = np.random.choice(['Science', 'Commerce', 'Arts'], size=n_samples, p=[0.55, 0.38, 0.07])
    degree_t = np.random.choice(['Sci&Tech', 'Comm&Mgmt', 'Others'], size=n_samples, p=[0.50, 0.40, 0.10])
    workex = np.random.choice(['No', 'Yes'], size=n_samples, p=[0.60, 0.40])

    ssc_p = np.round(np.clip(np.random.normal(68.5, 10.5, n_samples), 40.0, 95.0), 2)
    hsc_p = np.round(np.clip(np.random.normal(67.0, 10.8, n_samples), 40.0, 98.0), 2)
    degree_p = np.round(np.clip(np.random.normal(67.8, 7.5, n_samples), 50.0, 95.0), 2)
    etest_p = np.round(np.clip(np.random.normal(73.5, 12.0, n_samples), 45.0, 99.0), 2)

    # Technical & Soft Skills Features
    coding_score = np.round(np.clip(np.random.normal(72.0, 14.0, n_samples), 35.0, 100.0), 1)
    communication_score = np.round(np.clip(np.random.normal(73.0, 12.0, n_samples), 40.0, 100.0), 1)
    projects_count = np.random.choice([0, 1, 2, 3, 4, 5], size=n_samples, p=[0.08, 0.22, 0.35, 0.22, 0.09, 0.04])
    certifications_count = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.15, 0.38, 0.30, 0.12, 0.05])

    # Realistic placement score calculation considering academics AND technical skills
    score = (
        0.06 * (ssc_p - 67) +
        0.05 * (hsc_p - 66) +
        0.07 * (degree_p - 66) +
        0.04 * (etest_p - 72) +
        0.08 * (coding_score - 70) +
        0.06 * (communication_score - 72) +
        0.50 * projects_count +
        0.40 * certifications_count +
        (1.5 if 'Yes' in workex else -0.4) +
        np.random.normal(0, 1.0, n_samples)
    )
    
    # Target: ~70% Placed, 30% Not Placed
    threshold = np.percentile(score, 30)
    status = np.where(score > threshold, 'Placed', 'Not Placed')

    # Expected CTC / Salary for placed candidates (in LPA / INR)
    salary = np.where(
        status == 'Placed',
        np.round(np.random.normal(320000, 70000, n_samples) + (coding_score * 1500) + (projects_count * 20000), -3),
        np.nan
    )

    df = pd.DataFrame({
        'sl_no': np.arange(1, n_samples + 1),
        'gender': genders,
        'ssc_p': ssc_p,
        'ssc_b': ssc_b,
        'hsc_p': hsc_p,
        'hsc_b': hsc_b,
        'hsc_s': hsc_s,
        'degree_p': degree_p,
        'degree_t': degree_t,
        'workex': workex,
        'etest_p': etest_p,
        'coding_score': coding_score,
        'communication_score': communication_score,
        'projects_count': projects_count,
        'certifications_count': certifications_count,
        'status': status,
        'salary': salary
    })
    return df

def main():
    csv_file = 'Placement_Data_Full_Class.csv'
    df = generate_placement_dataset()
    df.to_csv(csv_file, index=False)
    print(f"Dataset generated & saved to {csv_file}. Shape: {df.shape}")

    # Preprocessing
    data = df.drop(columns=['sl_no', 'salary'], errors='ignore').copy()

    # Target encoding: Placed=1, Not Placed=0
    target_le = LabelEncoder()
    data['status'] = target_le.fit_transform(data['status'])
    
    categorical_cols = ['gender', 'ssc_b', 'hsc_b', 'hsc_s', 'degree_t', 'workex']
    data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

    # Ensure all boolean columns are int (0 or 1)
    for col in data_encoded.columns:
        if data_encoded[col].dtype == bool:
            data_encoded[col] = data_encoded[col].astype(int)

    X = data_encoded.drop(columns=['status'])
    y = data_encoded['status']

    feature_cols = list(X.columns)
    print(f"Feature columns ({len(feature_cols)} total):", feature_cols)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    models = {}
    metrics_summary = {}

    # 1. Logistic Regression
    lr_grid = GridSearchCV(
        LogisticRegression(max_iter=1000, random_state=SEED),
        {'C': [0.01, 0.1, 1, 10], 'penalty': ['l2'], 'solver': ['lbfgs']},
        cv=cv, scoring='f1', n_jobs=-1
    )
    lr_grid.fit(StandardScaler().fit_transform(X_train), y_train)
    best_lr = lr_grid.best_estimator_
    models['Logistic Regression'] = ('scaled', best_lr)

    # 2. Random Forest
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=SEED),
        {'n_estimators': [100, 200], 'max_depth': [3, 5, 7, None], 'min_samples_split': [2, 5]},
        cv=cv, scoring='f1', n_jobs=-1
    )
    rf_grid.fit(X_train, y_train)
    best_rf = rf_grid.best_estimator_
    models['Random Forest'] = ('unscaled', best_rf)

    # 3. SVM
    svm_grid = GridSearchCV(
        SVC(probability=True, random_state=SEED),
        {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']},
        cv=cv, scoring='f1', n_jobs=-1
    )
    svm_grid.fit(StandardScaler().fit_transform(X_train), y_train)
    best_svm = svm_grid.best_estimator_
    models['SVM'] = ('scaled', best_svm)

    # 4. XGBoost
    xgb_grid = GridSearchCV(
        xgb.XGBClassifier(eval_metric='logloss', random_state=SEED),
        {'n_estimators': [100], 'max_depth': [3, 4], 'learning_rate': [0.05, 0.1]},
        cv=cv, scoring='f1', n_jobs=-1
    )
    xgb_grid.fit(X_train, y_train)
    best_xgb = xgb_grid.best_estimator_
    models['XGBoost'] = ('unscaled', best_xgb)

    scaler = StandardScaler().fit(X_train)
    X_test_scaled = scaler.transform(X_test)

    best_name = None
    best_f1 = -1

    for name, (scale_type, model) in models.items():
        X_eval = X_test_scaled if scale_type == 'scaled' else X_test
        y_pred = model.predict(X_eval)
        proba = model.predict_proba(X_eval)[:, 1] if hasattr(model, 'predict_proba') else y_pred
        
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        auc = float(roc_auc_score(y_test, proba))
        cm = confusion_matrix(y_test, y_pred).tolist()

        metrics_summary[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1': f1,
            'ROC-AUC': auc,
            'ConfusionMatrix': cm
        }

        print(f"[{name}] Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_name = name

    print(f"\nBest Performing Model: {best_name} (F1: {best_f1:.4f})")

    # Build production pipeline with Logistic Regression
    prod_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', models['Logistic Regression'][1])
    ])
    prod_pipeline.fit(X, y)

    # Feature importance
    lr_model = prod_pipeline.named_steps['classifier']
    coefs = lr_model.coef_[0].tolist()
    feature_importance = [
        {'feature': col, 'weight': round(float(w), 4)}
        for col, w in zip(feature_cols, coefs)
    ]
    feature_importance.sort(key=lambda x: abs(x['weight']), reverse=True)

    # Save Pipeline
    model_filename = 'placement_pipeline.joblib'
    joblib.dump(prod_pipeline, model_filename)
    print(f"Pipeline saved to {model_filename}")

    # Dataset Summary Statistics
    dataset_stats = {
        'total_students': len(df),
        'placed_count': int((df['status'] == 'Placed').sum()),
        'not_placed_count': int((df['status'] == 'Not Placed').sum()),
        'avg_ssc_p': round(float(df['ssc_p'].mean()), 2),
        'avg_hsc_p': round(float(df['hsc_p'].mean()), 2),
        'avg_degree_p': round(float(df['degree_p'].mean()), 2),
        'avg_etest_p': round(float(df['etest_p'].mean()), 2),
        'avg_coding_score': round(float(df['coding_score'].mean()), 2),
        'avg_communication_score': round(float(df['communication_score'].mean()), 2),
        'avg_projects': round(float(df['projects_count'].mean()), 1),
        'avg_salary_placed': round(float(df[df['status'] == 'Placed']['salary'].mean()), 0)
    }

    metadata = {
        'best_model': best_name,
        'feature_cols': feature_cols,
        'models_performance': metrics_summary,
        'feature_importance': feature_importance,
        'dataset_stats': dataset_stats
    }

    with open('model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print("Model metadata saved to model_metadata.json")

if __name__ == '__main__':
    main()
