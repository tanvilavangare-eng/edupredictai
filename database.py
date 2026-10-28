"""
Database management module for AI-Based Student Performance Prediction System.
Handles SQLite connection, schema creation, user authentication, and student records.
"""

import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "student_prediction.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table (supports teachers, administrators, and students with personal & parents details)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password_hash VARCHAR(256) NOT NULL,
        full_name VARCHAR(120) NOT NULL,
        role VARCHAR(20) DEFAULT 'teacher', -- 'teacher', 'admin', 'student'
        phone VARCHAR(20),
        father_phone VARCHAR(20),
        mother_phone VARCHAR(20),
        class_course VARCHAR(80),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(120) NOT NULL,
        class_course VARCHAR(80) NOT NULL,
        age INTEGER DEFAULT 19,
        gender VARCHAR(20) DEFAULT 'Other',
        phone VARCHAR(20),
        father_phone VARCHAR(20),
        mother_phone VARCHAR(20),
        attendance_pct REAL NOT NULL,
        internal_marks REAL NOT NULL,
        assignment_marks REAL NOT NULL,
        previous_exam_marks REAL NOT NULL,
        study_hours_per_day REAL NOT NULL,
        predicted_score REAL,
        predicted_category VARCHAR(50),
        risk_level VARCHAR(20),
        recommendations TEXT,
        improvement_areas TEXT,
        created_by VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # AI Training Logs / Model Stats table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name VARCHAR(100),
        accuracy_score REAL,
        r2_score REAL,
        mae_score REAL,
        training_samples INTEGER,
        trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Seed initial teacher and sample students if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        seed_users(cursor)

    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        seed_students(cursor)

    conn.commit()
    conn.close()

def seed_users(cursor):
    # Default Teacher Account
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, full_name, role, phone, father_phone, mother_phone, class_course)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'teacher',
        'teacher@college.edu',
        hash_password('teacher123'),
        'Dr. Sarah Jenkins (Professor)',
        'teacher',
        '+1 555-0199',
        '+1 555-0101',
        '+1 555-0102',
        'Computer Science Dept'
    ))

    # Default Admin Account
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, full_name, role, phone, father_phone, mother_phone, class_course)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        'admin',
        'admin@college.edu',
        hash_password('admin123'),
        'Academic Administrator',
        'admin',
        '+1 555-0188',
        '+1 555-0103',
        '+1 555-0104',
        'Administration'
    ))

def seed_students(cursor):
    sample_students = [
        # (student_id, name, class_course, age, gender, phone, father_phone, mother_phone, attendance, internal, assignment, prev_exam, study_hrs)
        ('STU1001', 'Aarav Sharma', 'B.Tech CS 3rd Year', 20, 'Male', '+91 9876543210', '+91 9876543211', '+91 9876543212', 92.5, 88.0, 91.0, 85.0, 5.5),
        ('STU1002', 'Priya Patel', 'B.Tech CS 3rd Year', 20, 'Female', '+91 9876543220', '+91 9876543221', '+91 9876543222', 88.0, 84.0, 89.0, 82.0, 4.5),
        ('STU1003', 'Rohan Gupta', 'B.Tech CS 3rd Year', 21, 'Male', '+91 9876543230', '+91 9876543231', '+91 9876543232', 58.0, 42.0, 50.0, 45.0, 1.5),
        ('STU1004', 'Ananya Iyer', 'B.Tech IT 3rd Year', 20, 'Female', '+91 9876543240', '+91 9876543241', '+91 9876543242', 95.0, 94.0, 96.0, 92.0, 6.0),
        ('STU1005', 'Vikram Singh', 'B.Tech CS 3rd Year', 21, 'Male', '+91 9876543250', '+91 9876543251', '+91 9876543252', 62.0, 51.0, 55.0, 48.0, 2.0),
        ('STU1006', 'Sneha Kulkarni', 'B.Tech CS 3rd Year', 20, 'Female', '+91 9876543260', '+91 9876543261', '+91 9876543262', 78.0, 72.0, 75.0, 70.0, 3.5),
        ('STU1007', 'Karan Malhotra', 'B.Tech IT 3rd Year', 20, 'Male', '+91 9876543270', '+91 9876543271', '+91 9876543272', 51.0, 38.0, 42.0, 40.0, 1.0),
        ('STU1008', 'Neha Verma', 'B.Tech CS 3rd Year', 19, 'Female', '+91 9876543280', '+91 9876543281', '+91 9876543282', 85.0, 79.0, 83.0, 78.0, 4.0),
        ('STU1009', 'Aditya Joshi', 'B.Tech IT 3rd Year', 21, 'Male', '+91 9876543290', '+91 9876543291', '+91 9876543292', 45.0, 35.0, 38.0, 36.0, 0.8),
        ('STU1010', 'Pooja Nair', 'B.Tech CS 3rd Year', 20, 'Female', '+91 9876543300', '+91 9876543301', '+91 9876543302', 91.0, 86.0, 90.0, 84.0, 5.0),
        ('STU1011', 'Rahul Deshmukh', 'BCA 2nd Year', 19, 'Male', '+91 9876543310', '+91 9876543311', '+91 9876543312', 74.0, 68.0, 70.0, 65.0, 3.0),
        ('STU1012', 'Tanvi Chawla', 'BCA 2nd Year', 19, 'Female', '+91 9876543320', '+91 9876543321', '+91 9876543322', 89.0, 82.0, 85.0, 80.0, 4.2),
        ('STU1013', 'Devendra Reddy', 'B.Tech CS 3rd Year', 20, 'Male', '+91 9876543330', '+91 9876543331', '+91 9876543332', 54.0, 44.0, 46.0, 42.0, 1.2),
        ('STU1014', 'Meera Rao', 'B.Tech IT 3rd Year', 20, 'Female', '+91 9876543340', '+91 9876543341', '+91 9876543342', 96.0, 95.0, 98.0, 94.0, 6.5),
        ('STU1015', 'Siddharth Jain', 'BCA 2nd Year', 20, 'Male', '+91 9876543350', '+91 9876543351', '+91 9876543352', 68.0, 60.0, 64.0, 58.0, 2.5),
        ('STU1016', 'Kavita Menon', 'B.Tech CS 3rd Year', 20, 'Female', '+91 9876543360', '+91 9876543361', '+91 9876543362', 82.0, 76.0, 80.0, 75.0, 3.8),
        ('STU1017', 'Arjun Saxena', 'B.Tech CS 3rd Year', 21, 'Male', '+91 9876543370', '+91 9876543371', '+91 9876543372', 49.0, 39.0, 41.0, 37.0, 1.0),
        ('STU1018', 'Bhavna Bose', 'B.Tech IT 3rd Year', 20, 'Female', '+91 9876543380', '+91 9876543381', '+91 9876543382', 77.0, 71.0, 73.0, 69.0, 3.2),
        ('STU1019', 'Gaurav Dubey', 'BCA 2nd Year', 20, 'Male', '+91 9876543390', '+91 9876543391', '+91 9876543392', 86.0, 80.0, 84.0, 79.0, 4.4),
        ('STU1020', 'Ishita Sen', 'B.Tech CS 3rd Year', 20, 'Female', '+91 9876543400', '+91 9876543401', '+91 9876543402', 93.0, 89.0, 92.0, 87.0, 5.2)
    ]

    for stu in sample_students:
        s_id, name, course, age, gender, phone, f_phone, m_phone, att, internal, assign, prev, study_hrs = stu
        
        # Calculate heuristic baseline for seed
        est_score = round(0.20 * att + 0.30 * internal + 0.20 * assign + 0.25 * prev + min(study_hrs * 1.5, 5.0), 1)
        est_score = min(max(est_score, 25.0), 99.0)

        if est_score >= 80:
            category = 'Excellent'
            risk = 'Low'
            recs = 'Maintain strong academic habits, explore advanced research projects, and mentor peers.'
            improvements = 'Consistent performance across all modules. Keep challenging yourself.'
        elif est_score >= 65:
            category = 'Good'
            risk = 'Low'
            recs = 'Focus on turning good scores into top tier. Increase dedicated revision by 1 hour daily.'
            improvements = 'Target previous exam weak topics to boost final score.'
        elif est_score >= 50:
            category = 'Average'
            risk = 'Medium'
            recs = 'Increase attendance and form weekly study groups. Submit all practice assignments on time.'
            improvements = 'Internal marks and attendance need consistent focus.'
        else:
            category = 'At-Risk'
            risk = 'High'
            recs = 'URGENT: Schedule 1-on-1 academic counseling. Remedial tutoring required. Contact parents.'
            improvements = 'Attendance is critically low (<60%), internal exam and assignment scores are below threshold.'

        cursor.execute("""
        INSERT INTO students (
            student_id, name, class_course, age, gender, phone, father_phone, mother_phone,
            attendance_pct, internal_marks, assignment_marks, previous_exam_marks, study_hours_per_day,
            predicted_score, predicted_category, risk_level, recommendations, improvement_areas, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s_id, name, course, age, gender, phone, f_phone, m_phone,
            att, internal, assign, prev, study_hrs,
            est_score, category, risk, recs, improvements, 'teacher'
        ))

if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded successfully.")
