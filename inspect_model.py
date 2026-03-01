import tensorflow as tf
import os

model_path = 'ml-service/plant_disease_model.keras'

if os.path.exists(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully.")
        print("Input shape:", model.input_shape)
        
        # Try to find class names in metadata
        if hasattr(model, 'class_names'):
            print("Class names found in model:", model.class_names)
        else:
            print("No class_names attribute found.")
            
        # Check output layer units
        output_layer = model.layers[-1]
        print("Output units:", output_layer.units)
        
    except Exception as e:
        print("Error loading model:", e)
else:
    print("Model file not found at", model_path)
