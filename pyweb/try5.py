import numpy as np
import librosa
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def extract_features(audio_path):
    y, sr = librosa.load(audio_path)
    pitch, _ = librosa.piptrack(y=y, sr=sr)
    pitches = pitch[pitch > 0]
    median_pitch = np.median(pitches)
    return median_pitch

# Load your dataset (audio files and labels)
audio_files = ["C:/Users/maina/Downloads/bengali.wav", "C:/Users/maina/Downloads/aud2.wav", "C:/Users/maina/Downloads/bengali.wav", "C:/Users/maina/Downloads/nptel_audio_english.wav"]  # Add paths to your dataset
labels = [1, 0, 1, 0]  # 1 for male, 0 for female

# Ensure you have a balanced dataset
if len(set(labels)) < 2:
    raise ValueError("The dataset must contain at least two classes (male and female)")

# Extract features from the dataset
features = [extract_features(file) for file in audio_files]

# Reshape the features array
features = np.array(features).reshape(-1, 1)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train a classifier
classifier = SVC(kernel='linear')
classifier.fit(X_train, y_train)

# Evaluate the classifier
y_pred = classifier.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Save the trained model
joblib.dump(classifier, 'gender_classifier.pkl')
print("Model saved as gender_classifier.pkl")
