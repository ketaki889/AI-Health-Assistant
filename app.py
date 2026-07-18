from database import create_database, save_patient, get_patients
from flask import Flask, render_template, request, send_file
import joblib
import numpy as np
from datetime import datetime
from pdf_report import create_pdf

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


app = Flask(__name__)

create_database()


# Load model
model = joblib.load("model/model.pkl")



feature_names = [

    "Age",
    "Gender",
    "Chest Pain",
    "Blood Pressure",
    "Cholesterol",
    "Blood Sugar",
    "ECG",
    "Maximum Heart Rate",
    "Exercise Angina",
    "Old Peak",
    "Slope",
    "Major Vessels",
    "Thalassemia"

]



@app.route("/")
def home():

    return render_template("index.html")





@app.route("/predict", methods=["POST"])
def predict():


    age=float(request.form["age"])
    sex=float(request.form["sex"])
    cp=float(request.form["cp"])
    trestbps=float(request.form["trestbps"])
    chol=float(request.form["chol"])
    fbs=float(request.form["fbs"])
    restecg=float(request.form["restecg"])
    thalach=float(request.form["thalach"])
    exang=float(request.form["exang"])
    oldpeak=float(request.form["oldpeak"])
    slope=float(request.form["slope"])
    ca=float(request.form["ca"])
    thal=float(request.form["thal"])



    features=np.array([[

        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal

    ]])


    prediction=model.predict(features)[0]

    probability=model.predict_proba(features)[0]


    confidence=round(max(probability)*100,2)



    if prediction==1:

        risk="LOW RISK"
        color="success"

    else:

        risk="HIGH RISK"
        color="danger"



    health_score=int(probability[1]*100)



    # =========================
    # AI Explanation
    # =========================


    importance=model.feature_importances_

    explanation=[]


    for name,value in zip(feature_names,importance):

        explanation.append(

            (
                name,
                round(float(value)*100,2)
            )

        )


    explanation=sorted(

        explanation,
        key=lambda x:x[1],
        reverse=True

    )


    top_factors=explanation[:3]



    # =========================
    # Dashboard Chart
    # =========================


    labels=[]
    values=[]


    for factor,value in top_factors:

        labels.append(factor)
        values.append(value)



    plt.figure(figsize=(7,4))

    plt.bar(
        labels,
        values,
        color="#0d6efd"
    )


    plt.title("Top AI Risk Factors")

    plt.ylabel("Importance %")


    plt.xticks(
        rotation=30,
        ha="right"
    )


    plt.tight_layout()


    plt.savefig(
        "static/risk_chart.png"
    )

    plt.close()



    # =========================
    # Risk Factors
    # =========================


    risk_factors=[]


    if age>60:
        risk_factors.append(
            "Age related cardiovascular risk"
        )


    if trestbps>140:
        risk_factors.append(
            "High blood pressure"
        )


    if chol>240:
        risk_factors.append(
            "High cholesterol"
        )


    if exang==1:
        risk_factors.append(
            "Exercise induced chest discomfort"
        )


    if oldpeak>2:
        risk_factors.append(
            "Stress ECG abnormality"
        )



    if len(risk_factors)==0:

        risk_factors.append(
            "No major risk factors detected"
        )




    advice=[

        "Maintain balanced diet",

        "Exercise regularly",

        "Monitor blood pressure",

        "Control stress",

        "Consult healthcare professional"

    ]




    if prediction==0:

        emergency="⚠️ High risk detected. Medical consultation recommended."

    else:

        emergency="✅ Lower cardiovascular risk detected."





    patient={

        "age":age,

        "cholesterol":chol,

        "blood_pressure":trestbps,

        "heart_rate":thalach

    }




    # =========================
    # Create PDF
    # =========================


    pdf_data={

        "Risk":risk,

        "Confidence":str(confidence)+"%",

        "Health Score":str(health_score)+"%",

        "Age":age,

        "Blood Pressure":trestbps,

        "Cholesterol":chol,

        "Heart Rate":thalach,

        "Result":emergency

    }


    create_pdf(pdf_data)



    time=datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )



    # =========================
    # Save Database
    # =========================


    save_patient({

        "age":age,

        "blood_pressure":trestbps,

        "cholesterol":chol,

        "heart_rate":thalach,

        "risk":risk,

        "confidence":confidence,

        "health_score":health_score,

        "date":time

    })




    return render_template(

        "result.html",

        risk=risk,

        color=color,

        confidence=confidence,

        health_score=health_score,

        risk_factors=risk_factors,

        advice=advice,

        emergency=emergency,

        patient=patient,

        time=time,

        top_factors=top_factors,

        chart="risk_chart.png"

    )





@app.route("/download")
def download():

    return send_file(

        "AI_Health_Report.pdf",

        as_attachment=True

    )





@app.route("/history")
def history():

    patients=get_patients()

    return render_template(

        "history.html",

        patients=patients

    )





if __name__=="__main__":

    app.run(debug=True)