import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# -------------------------------
# LOAD DATASET
# -------------------------------
df = pd.read_csv("data/student-mat.csv", sep=";")

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------
df["attendance"] = 100 - df["absences"]
df["attendance"] = df["attendance"].clip(0, 100)

df["marks"] = (df["G1"] / 20) * 100

df["assignments"] = df["studytime"].map({
    1: 25,
    2: 50,
    3: 75,
    4: 100
})

df["classes_missed"] = df["absences"]

# -------------------------------
# TARGET VARIABLE
# -------------------------------
def assign_risk(g3):
    if g3 >= 14:
        return "Safe"
    elif g3 >= 10:
        return "At Risk"
    else:
        return "Critical"

df["risk_level"] = df["G3"].apply(assign_risk)

# -------------------------------
# SELECT FEATURES
# -------------------------------
X = df[["attendance", "marks", "assignments", "classes_missed"]]
y = df["risk_level"]

# -------------------------------
# ENCODE TARGET
# -------------------------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# -------------------------------
# TRAIN TEST SPLIT
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# -------------------------------
# TRAIN MODEL
# -------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------------------------------
# TEST MODEL
# -------------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

report = classification_report(
    y_test, y_pred, target_names=encoder.classes_
)

# -------------------------------
# SAVE MODEL & ENCODER
# -------------------------------
pickle.dump(model, open("model/attendance_model.pkl", "wb"))
pickle.dump(encoder, open("model/encoder.pkl", "wb"))

# -------------------------------
# SAVE REPORT
# -------------------------------
with open("static/model_report.txt", "w") as f:
    f.write("MODEL EVALUATION REPORT\n\n")
    f.write(f"Accuracy: {round(accuracy*100,2)}%\n\n")
    f.write(report)

# -------------------------------
# ACCURACY CHART
# -------------------------------
plt.figure()
plt.bar(["Accuracy"], [accuracy])
plt.ylim(0, 1)
plt.title("Model Accuracy")
plt.savefig("static/accuracy.png")
plt.close()

# -------------------------------
# CONFUSION MATRIX
# -------------------------------
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=encoder.classes_)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.savefig("static/confusion_matrix.png")
plt.close()

print("Training complete. Files saved.")
