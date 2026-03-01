import tensorflow as tf
import numpy as np
from PIL import Image
import os

print("Loading AI model...")
# Using the correct path relative to the ml-service directory or project root
MODEL_PATH = "ml-service/model.keras"
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")

CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]

IMG_SIZE = (224, 224)

def preprocess(image):
    image = image.resize(IMG_SIZE)
    img = np.array(image)
    # Check if normalization is needed (the user's code didn't have /255.0, 
    # but many Keras models expect it. I'll stick to their exact snippet first.)
    img = np.expand_dims(img, axis=0)
    return img

def predict_disease(file):
    image = Image.open(file).convert("RGB")
    img = preprocess(image)

    predictions = model.predict(img)

    index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))

    # Mapping to the frontend's expected format while keeping the user's logic
    disease_name = CLASS_NAMES[index]
    
    # We add the extra fields the frontend needs for a better UI experience
    severity = "Medium"
    if "healthy" in disease_name.lower():
        severity = "Low"
    elif confidence > 0.8:
        severity = "High"

    return {
        "disease": disease_name.replace("___", " ").replace("__", " ").replace("_", " "),
        "confidence": round(confidence * 100, 2),
        "severity": severity,
        "treatment": get_treatment_advice(disease_name),
        "affectedCrops": get_affected_crops(disease_name),
        "prevention": get_prevention_tips(disease_name),
        "nextSteps": get_next_steps(disease_name)
    }

def get_treatment_advice(disease):
    d = disease.lower()
    if "healthy" in d: return "No treatment needed."
    if "blight" in d: return "Apply copper-based fungicides and remove infected leaves."
    if "bacterial_spot" in d: return "Use streptomycin or copper-based sprays; avoid overhead watering."
    if "mold" in d: return "Improve ventilation and reduce humidity."
    if "virus" in d: return "Remove infected plants; control whitefly/aphid populations."
    if "mite" in d: return "Use miticides or neem oil; increase humidity around the plant."
    return "Consult a local agriculture expert for specific pesticide recommendations."

def get_affected_crops(disease):
    d = disease.lower()
    if "tomato" in d: return "Tomato, Potato, Pepper"
    if "potato" in d: return "Potato, Tomato"
    if "pepper" in d: return "Pepper, Chili"
    return "Solanaceous crops"

def get_prevention_tips(disease):
    if "healthy" in disease.lower(): return "Maintain regular irrigation and soil nutrient levels."
    return "Use disease-resistant seeds, ensure proper spacing for airflow, and sanitize tools."

def get_next_steps(disease):
    if "healthy" in disease.lower(): return ["Regular inspection", "Monitor for pests"]
    return ["Isolate infected plants", "Decontaminate tools", "Apply treatment promptly"]
