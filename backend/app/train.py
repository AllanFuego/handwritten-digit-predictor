# ============================================
# CELL 2: Import Libraries
# ============================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import os
import cv2
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyngrok import ngrok
import uvicorn
import warnings
import time
import requests
import subprocess
import sys
warnings.filterwarnings('ignore')
print("✅ All libraries imported!")

# ============================================
# CELL 3: Load and Explore MNIST Dataset
# ============================================
print("="*60)
print("LOADING MNIST DATASET")
print("="*60)

# Load dataset
print("Loading MNIST dataset...")
X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False, parser='pandas')
X = np.array(X)
y = np.array(y, dtype=int)

print(f"Dataset shape: {X.shape}")
print(f"Labels: {np.unique(y)}")

# Display sample images
fig, axes = plt.subplots(2, 5, figsize=(12, 6))
for i, ax in enumerate(axes.ravel()):
    idx = np.random.randint(0, len(X))
    ax.imshow(X[idx].reshape(28, 28), cmap='gray')
    ax.set_title(f'Digit: {y[idx]}')
    ax.axis('off')
plt.tight_layout()
plt.show()
print(f"\n✅ Dataset loaded successfully!")

# ============================================
# CELL 4: Data Preprocessing
# ============================================
print("="*60)
print("DATA PREPROCESSING")
print("="*60)

# Normalize pixel values
X = X / 255.0

# Split data (70% train, 15% validation, 15% test)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

print(f"Training set:   {X_train.shape[0]} samples")
print(f"Validation set: {X_val.shape[0]} samples")
print(f"Test set:       {X_test.shape[0]} samples")
print("\n✅ Data preprocessing complete!")

# ============================================
# CELL 5: Train KNN Classifier
# ============================================
print("="*60)
print("TRAINING KNN CLASSIFIER")
print("="*60)

# Use subset for faster training
n_samples = 10000
print(f"Training KNN with {n_samples} samples...")

knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
knn.fit(X_train[:n_samples], y_train[:n_samples])

# Evaluate
y_pred_knn = knn.predict(X_val)
knn_acc = accuracy_score(y_val, y_pred_knn)

print(f"KNN Validation Accuracy: {knn_acc:.4f}")
print("\n✅ KNN training complete!")

# ============================================
# CELL 6: Train SVM Classifier
# ============================================
print("="*60)
print("TRAINING SVM CLASSIFIER")
print("="*60)

# Use subset for faster training
n_samples = 5000
print(f"Training SVM with {n_samples} samples...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[:n_samples])
X_val_scaled = scaler.transform(X_val)

svm = SVC(kernel='rbf', C=10, gamma='scale', random_state=42)
svm.fit(X_train_scaled, y_train[:n_samples])

# Evaluate
y_pred_svm = svm.predict(X_val_scaled)
svm_acc = accuracy_score(y_val, y_pred_svm)

print(f"SVM Validation Accuracy: {svm_acc:.4f}")
print("\n✅ SVM training complete!")

# ============================================
# CELL 7: Model Comparison and Selection
# ============================================
print("="*60)
print("MODEL COMPARISON")
print("="*60)

print(f"KNN Accuracy: {knn_acc:.4f}")
print(f"SVM Accuracy: {svm_acc:.4f}")

# Select best model and train on full dataset
if knn_acc >= svm_acc:
    print("\n✅ KNN is the best model!")
    print("Training KNN on full dataset...")
    best_model = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
    best_model.fit(X_train, y_train)
    model_name = 'KNN'
    scaler_final = None
else:
    print("\n✅ SVM is the best model!")
    print("Training SVM on full dataset...")
    scaler_final = StandardScaler()
    X_train_full_scaled = scaler_final.fit_transform(X_train)
    best_model = SVC(kernel='rbf', C=10, gamma='scale', random_state=42)
    best_model.fit(X_train_full_scaled, y_train)
    model_name = 'SVM'

print(f"\n🏆 Best Model: {model_name}")
print("\n✅ Model selection complete!")

# ============================================
# CELL 8: Model Evaluation
# ============================================
print("="*60)
print("MODEL EVALUATION")
print("="*60)

# Make predictions on test set
if model_name == 'KNN':
    y_pred = best_model.predict(X_test)
else:
    X_test_scaled = scaler_final.transform(X_test)
    y_pred = best_model.predict(X_test_scaled)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"📊 Model Performance:")
print(f"   Accuracy:  {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall:    {recall:.4f}")
print(f"   F1-Score:  {f1:.4f}")

# Classification Report
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=range(10), yticklabels=range(10))
plt.title(f'Confusion Matrix - {model_name}', fontsize=14)
plt.xlabel('Predicted', fontsize=12)
plt.ylabel('Actual', fontsize=12)
plt.tight_layout()
plt.show()

# ============================================
# CELL 9: Save Models
# ============================================
print("="*60)
print("SAVING MODELS")
print("="*60)

# Create models directory
os.makedirs('models', exist_ok=True)

# Save best model
joblib.dump(best_model, 'models/best_model.pkl')
print(f"✅ Model saved: models/best_model.pkl")

# Save scaler if SVM
if model_name == 'SVM':
    joblib.dump(scaler_final, 'models/scaler.pkl')
    print(f"✅ Scaler saved: models/scaler.pkl")

# Save model info
model_info = {
    'model_name': model_name,
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1_score': f1
}
joblib.dump(model_info, 'models/model_info.pkl')
print(f"✅ Model info saved: models/model_info.pkl")

print("\n✅ All models saved successfully!")