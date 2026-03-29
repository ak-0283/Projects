# 🩺 Skin Cancer Detection

A simple Flask web app for skin lesion image classification using multiple deep learning models.

This is a **BCA 6th Semester Major Project**.

## 📌 Overview

SkinCare AI allows users to upload a skin lesion image and get predictions from:

- 🧠 Pretrained model (**EfficientNetB3**)
- ⚙️ Hybrid model
- 🔬 Custom model

The app shows predicted class labels with confidence scores and model comparison cards.

## ✨ Features

- 📤 Image upload and preview
- 🤖 Multi-model prediction pipeline
- 🧠 Pretrained prediction using EfficientNetB3
- 📊 Confidence score visualization
- 📈 Training results page with model plots
- 🎨 Clean, responsive UI

## 🛠️ Tech Stack

- Python
- Flask
- TensorFlow / Keras
- NumPy
- Pillow
- HTML / CSS / JavaScript

## 🗂️ Project Structure

```text
skin-caner/
├── app.py
├── requirements.txt
├── dataset/
├── models/
│   ├── pretrained/
│   ├── hybrid/
│   └── custom/
├── static/
│   ├── css/
│   ├── js/
│   ├── pre/
│   ├── hybrid/
│   └── custom/
└── templates/
```

## 🚀 Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.

```bash
pip install -r requirements.txt
```

## ▶️ Run

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

## 📝 Notes

- Keep model files (`.h5`, `.keras`) in the correct `models/` subfolders.
- Pretrained model is based on **EfficientNetB3** (`models/pretrained/efficientb3.h5` / `models/pretrained/skin_cancer.keras`).
- Ensure static result images exist in `static/pre`, `static/hybrid`, and `static/custom`.
- Accuracy values shown on UI are configured in `app.py`.

## ⚠️ Disclaimer

This project is for educational and awareness purposes only. It is not a medical diagnosis tool.
