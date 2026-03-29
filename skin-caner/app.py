from flask import Flask, render_template, request
import base64
import io
import os
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from PIL import Image


# ------------------------------------------------
# APP SETUP
# ------------------------------------------------

app = Flask(__name__)

# ------------------------------------------------
# LOAD MODEL (VERY FAST with .keras)
# ------------------------------------------------

MODEL_PATH = "models/pretrained/efficientb3.h5"
MODEL_KERAS_PATH = "models/pretrained/skin_cancer.keras"
MODEL_HYBRID_PATH = "models/hybrid/hybrid_model.keras"
MODEL_HYBRID_H5_PATH = "models/hybrid/hybrid_model.h5"
MODEL_CUSTOM_PATH = "models/custom/custom_cnn_model.keras"
MODEL_CUSTOM_H5_PATH = "models/custom/custom_cnn_model.h5"

# Update these with your actual evaluation results
PRETRAINED_ACCURACY = 0.89
HYBRID_ACCURACY = 0.68
CUSTOM_ACCURACY = 0.92

print("Loading model...")

# Try keras format first, fall back to h5
model = None
if os.path.exists(MODEL_KERAS_PATH):
    try:
        model = load_model(MODEL_KERAS_PATH)
        print("[OK] Keras model loaded!")
    except Exception as e:
        print(f"[WARN] Keras model failed: {str(e)[:80]}")

# If keras failed, try building and loading h5 weights
if model is None and os.path.exists(MODEL_PATH):
    try:
        # Build EfficientNetB3 model with 3 input channels
        base_model = EfficientNetB3(input_shape=(224, 224, 3), include_top=False, weights=None)
        x = GlobalAveragePooling2D()(base_model.output)
        outputs = Dense(3, activation='softmax')(x)  # 3 classes: BKL, MEL, NV
        model = Model(inputs=base_model.input, outputs=outputs)
        
        # Load weights
        model.load_weights(MODEL_PATH, by_name=True, skip_mismatch=True)
        print("[OK] Model built and weights loaded!")
    except Exception as e:
        print(f"[ERROR] Failed to load h5: {str(e)[:80]}")
        raise

if model is None:
    raise RuntimeError("Could not load any model file!")

hybrid_model = None
if os.path.exists(MODEL_HYBRID_PATH):
    try:
        hybrid_model = load_model(MODEL_HYBRID_PATH)
        print("[OK] Hybrid model loaded!")
    except Exception as e:
        print(f"[WARN] Hybrid model failed: {str(e)[:80]}")

if hybrid_model is None and os.path.exists(MODEL_HYBRID_H5_PATH):
    try:
        hybrid_model = load_model(MODEL_HYBRID_H5_PATH)
        print("[OK] Hybrid model (h5) loaded!")
    except Exception as e:
        print(f"[WARN] Hybrid model h5 failed: {str(e)[:80]}")

custom_model = None
if os.path.exists(MODEL_CUSTOM_PATH):
    try:
        custom_model = load_model(MODEL_CUSTOM_PATH)
        print("[OK] Custom model loaded!")
    except Exception as e:
        print(f"[WARN] Custom model failed: {str(e)[:80]}")

if custom_model is None and os.path.exists(MODEL_CUSTOM_H5_PATH):
    try:
        custom_model = load_model(MODEL_CUSTOM_H5_PATH)
        print("[OK] Custom model (h5) loaded!")
    except Exception as e:
        print(f"[WARN] Custom model h5 failed: {str(e)[:80]}")


# ------------------------------------------------
# LOAD CLASS INDICES (BEST PRACTICE)
# ------------------------------------------------

CLASS_PATH = "models/pretrained/class_indices.json"

if os.path.exists(CLASS_PATH):
    with open(CLASS_PATH, "r") as f:
        class_indices = json.load(f)

    CLASSES = list(class_indices.keys())

else:
    # fallback if json not present
    CLASSES = ['BKL', 'MEL', 'NV']

CLASS_DISPLAY = {
    'BKL': 'Benign Keratosis-like Lesion',
    'MEL': 'Melanoma',
    'NV': 'Nevus (Mole)'
}


# ------------------------------------------------
# PREDICTION FUNCTION
# ------------------------------------------------

def predict_image_with_model(pil_image, model_instance, preprocess_mode="efficientnet"):

    img = pil_image.convert("RGB").resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    if preprocess_mode == "efficientnet":
        img_array = preprocess_input(img_array)
    else:
        img_array = img_array / 255.0

    prediction = model_instance.predict(img_array, verbose=0)
    prediction = np.squeeze(prediction)

    confidence = float(np.max(prediction)) * 100
    pred_index = int(np.argmax(prediction))

    class_labels = CLASSES
    if len(prediction) != len(CLASSES):
        class_labels = [f"Class {i}" for i in range(len(prediction))]

    label = class_labels[pred_index]

    scores = []
    for idx, score in enumerate(prediction):
        scores.append({
            "label": class_labels[idx],
            "value": round(float(score) * 100, 2)
        })

    scores = sorted(scores, key=lambda x: x["value"], reverse=True)

    return label, round(confidence, 2), scores


# ------------------------------------------------
# ROUTES
# ------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/training')
def training():
    return render_template('training.html')


@app.route('/detect', methods=['GET', 'POST'])
def detect():

    prediction = None
    prediction_display = None
    pretrained_prediction = None
    hybrid_prediction = None
    custom_prediction = None
    pretrained_scores = None
    hybrid_scores = None
    custom_scores = None
    confidence = None
    img_path = None
    error = None

    if request.method == 'POST':

        file = request.files.get('file')

        if file and file.filename != "":
            try:
                file_bytes = file.read()
                if file_bytes:
                    pil_image = Image.open(io.BytesIO(file_bytes))
                    pretrained_prediction, confidence, pretrained_scores = predict_image_with_model(
                        pil_image,
                        model,
                        preprocess_mode="efficientnet"
                    )

                    prediction = pretrained_prediction

                    if hybrid_model is not None:
                        hybrid_prediction, hybrid_confidence, hybrid_scores = predict_image_with_model(
                            pil_image,
                            hybrid_model,
                            preprocess_mode="efficientnet"
                        )
                        prediction = hybrid_prediction
                        confidence = hybrid_confidence

                    if custom_model is not None:
                        custom_prediction, custom_confidence, custom_scores = predict_image_with_model(
                            pil_image,
                            custom_model,
                            preprocess_mode="rescale"
                        )
                        prediction = custom_prediction
                        confidence = custom_confidence

                    prediction_display = CLASS_DISPLAY.get(prediction, prediction)
                    img_path = f"data:image/jpeg;base64,{base64.b64encode(file_bytes).decode('utf-8')}"
            except Exception as e:
                error = f"Error processing image: {str(e)}"
        else:
            error = "No file selected or invalid filename"

    return render_template(
        'detect.html',
        prediction=prediction,
        prediction_display=prediction_display,
        pretrained_prediction=pretrained_prediction,
        hybrid_prediction=hybrid_prediction,
        custom_prediction=custom_prediction,
        pretrained_scores=pretrained_scores,
        hybrid_scores=hybrid_scores,
        custom_scores=custom_scores,
        confidence=confidence,
        img_path=img_path,
        error=error,
        pretrained_accuracy=PRETRAINED_ACCURACY,
        hybrid_accuracy=HYBRID_ACCURACY,
        custom_accuracy=CUSTOM_ACCURACY
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')


# ------------------------------------------------
# RUN SERVER
# ------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)