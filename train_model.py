# Example: Training and saving a model
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import pickle

# Create a dummy dataset
X, y = make_classification(n_samples=100, n_features=256*256, random_state=42)

# Train a model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model to Pickle
with open('models/signature_model.pkl', 'wb') as f:
    pickle.dump(model, f)

