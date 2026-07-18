import sqlite3


def create_database():

    conn=sqlite3.connect("patients.db")

    cursor=conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age REAL,
        blood_pressure REAL,
        cholesterol REAL,
        heart_rate REAL,
        risk TEXT,
        confidence REAL,
        health_score REAL,
        date TEXT

    )
    """)


    conn.commit()
    conn.close()



def save_patient(data):

    conn=sqlite3.connect("patients.db")

    cursor=conn.cursor()


    cursor.execute("""
    INSERT INTO patients
    (
    age,
    blood_pressure,
    cholesterol,
    heart_rate,
    risk,
    confidence,
    health_score,
    date
    )

    VALUES (?,?,?,?,?,?,?,?)

    """,

    (
    data["age"],
    data["blood_pressure"],
    data["cholesterol"],
    data["heart_rate"],
    data["risk"],
    data["confidence"],
    data["health_score"],
    data["date"]
    ))


    conn.commit()
    conn.close()



def get_patients():

    conn=sqlite3.connect("patients.db")

    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()


    cursor.execute(
        "SELECT * FROM patients ORDER BY id DESC"
    )


    data=cursor.fetchall()


    conn.close()


    return data