import numpy as np
from predictive_model import PredictiveModel

# Generate some sample data
X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
y = np.array([1, 2, 3, 4])

# Instantiate the model
model = PredictiveModel(model_type='linear')

# Train the model
model.train(X, y)

# Make a prediction
predictions = model.predict(np.array([[5, 6]]))

# Print the predictions
print("Predictions:", predictions)
