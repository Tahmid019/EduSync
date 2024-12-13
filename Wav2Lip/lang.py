import fasttext

# Path to the downloaded model file
model_path = '/home/oem/LIPSYNC/reactdb new try/reactdb1 (1)/reactdb/client/Wav2Lip/lid.176.bin'

# Load the model
model = fasttext.load_model(model_path)

# Example transliterated Bengali text
text = "ami jabo"

# Predict the language
predictions = model.predict(text)

# Extract the predicted language and confidence
predicted_language = predictions[0][0].replace("__label__", "")
confidence = predictions[1][0]

print(f"Detected language: {predicted_language}")
print(f"Confidence: {confidence}")


