import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Load dataset
csv_path = os.path.join("notebook", "Crop_recommendation.csv")
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

df = pd.read_csv(csv_path)

# Features and Target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']


# Train Random Forest
print("Training Random Forest Classifier...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Evaluate simple accuracy
acc = rf_model.score(X, y)
print(f"Model Accuracy on training data: {acc:.4f}")

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("Model saved as model.pkl")

# Create dummy or remove scalers? 
# We will update app_modern.py to not utilize them, but to be safe against 
# immediate file not found errors before the code update, we can leave them 
# or just ignore them.
