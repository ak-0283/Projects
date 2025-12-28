from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Required for flash messages

model = pickle.load(open("model/attendance_model.pkl", "rb"))
encoder = pickle.load(open("model/encoder.pkl", "rb"))

def predict_risk(attendance, marks, assignments, classes_missed):
    data = np.array([[attendance, marks, assignments, classes_missed]])
    result = model.predict(data)[0]
    risk = encoder.inverse_transform([result])[0]

    if risk == "Safe":
        suggestion = "Good performance. Maintain consistency."
    elif risk == "At Risk":
        suggestion = "Improve attendance and assignments."
    else:
        suggestion = "Immediate intervention required."

    return risk, suggestion

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dataset")
def dataset():
    return render_template("dataset.html")

@app.route("/model")
def model_page():
    return render_template("model.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = suggestion = None
    if request.method == "POST":
        prediction, suggestion = predict_risk(
            float(request.form["attendance"]),
            float(request.form["marks"]),
            float(request.form["assignments"]),
            float(request.form["classes_missed"])
        )
    return render_template("predict.html", prediction=prediction, suggestion=suggestion)

@app.route("/download-report")
def download_report():
    return send_file("static/model_report.txt", as_attachment=True)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        
        if not name or not email or not message:
            flash("All fields are required.", "error")
        elif "@" not in email:
            flash("Please enter a valid email address.", "error")
        else:
            # Here you could save to database, send email, etc.
            # For now, just acknowledge receipt
            flash(f"Thank you, {name}! Your message has been received. We'll respond to {email} soon.", "success")
            return redirect(url_for("contact"))
    
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
