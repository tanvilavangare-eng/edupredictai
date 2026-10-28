import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app
from database import get_db_connection

def run_tests():
    client = app.test_client()
    print("1. Testing Home Page (/) ...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert b"AI-Based Student Performance Prediction System" in res.data
    print("   -> Home Page OK!")

    print("2. Testing Login Page (/login) ...")
    res = client.get("/login")
    assert res.status_code == 200
    assert b"Academic Portal Access" in res.data
    print("   -> Login Page GET OK!")

    print("3. Testing Sign In POST (/login) ...")
    res = client.post("/login", data={
        "action_type": "login",
        "username": "teacher",
        "password": "teacher123"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Institutional Performance Dashboard" in res.data
    print("   -> Teacher Login & Redirect to Dashboard OK!")

    print("4. Testing Dashboard (/dashboard) ...")
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert b"Total Students" in res.data
    assert b"Students at Risk" in res.data
    print("   -> Dashboard OK!")

    print("5. Testing Prediction Page GET & POST (/prediction) ...")
    res = client.get("/prediction")
    assert res.status_code == 200
    
    # POST prediction test
    pred_res = client.post("/prediction", data={
        "student_name": "Test Student Alpha",
        "attendance_pct": "88.0",
        "internal_marks": "82.0",
        "assignment_marks": "85.0",
        "previous_exam_marks": "80.0",
        "study_hours_per_day": "4.5"
    })
    assert pred_res.status_code == 200
    assert b"Performance Dossier" in pred_res.data
    assert b"Low Risk" in pred_res.data or b"Good" in pred_res.data or b"Excellent" in pred_res.data
    print("   -> AI Prediction POST & Inference OK!")

    print("6. Testing Add Student POST (/add-student) ...")
    add_res = client.post("/add-student", data={
        "action_mode": "create",
        "student_id": "TEST9999",
        "name": "Kavita Test",
        "class_course": "B.Tech CS 3rd Year",
        "age": "20",
        "gender": "Female",
        "phone": "+91 9999988888",
        "father_phone": "+91 9999977777",
        "mother_phone": "+91 9999966666",
        "attendance_pct": "91.0",
        "internal_marks": "85.0",
        "assignment_marks": "88.0",
        "previous_exam_marks": "84.0",
        "study_hours_per_day": "5.0"
    }, follow_redirects=True)
    assert add_res.status_code == 200
    assert b"TEST9999" in add_res.data
    print("   -> Add Student & Automatic AI Evaluation OK!")

    print("7. Testing Reports Page (/reports) ...")
    rep_res = client.get("/reports")
    assert rep_res.status_code == 200
    assert b"TEST9999" in rep_res.data
    print("   -> Reports Page OK!")

    print("8. Testing Teacher Backend (/teacher-backend) ...")
    tb_res = client.get("/teacher-backend")
    assert tb_res.status_code == 200
    assert b"Feature Importance" in tb_res.data
    print("   -> Teacher Backend OK!")

    print("9. Testing Logout (/logout) ...")
    logout_res = client.get("/logout", follow_redirects=True)
    assert logout_res.status_code == 200
    assert b"securely logged out" in logout_res.data
    print("   -> Logout OK!")

    print("\nALL 9 AUTOMATED INTEGRATION TESTS PASSED SUCCESSFULLY! :)")

if __name__ == "__main__":
    run_tests()
