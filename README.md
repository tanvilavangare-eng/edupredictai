# 🎓 AI-Based Student Performance Prediction System

An end-to-end intelligent web application designed for academic institutions, faculty members, and student advisors. Powered by a trained **Scikit-Learn Random Forest Regressor** and **Explainable AI Diagnostics**, this system enables proactive early detection of at-risk students, predicts final examination performance, and delivers personalized academic intervention plans.

---

## 🌟 Key Features & 6 Core Pages

### 1. 🏠 Home Page (`/`)
- Academic brand logo & title: **AI-Based Student Performance Prediction System**
- Responsive navigation bar with dark-blue aesthetic and role status
- High-level project summary and value proposition
- 6 key system capability cards
- Direct CTA buttons: **Get Started** & **Login / Register**
- "About the Project" architectural explanation

### 2. 🔐 Login & Registration Page (`/login`)
- **Sign In Tab:**
  - Username / Email and Password fields
  - "Forgot Password" support modal
  - **1-Click Demo Login Buttons** for instant evaluation
- **New Registration Tab:**
  - Full Name & Role selection (Teacher / Admin / Student)
  - Username & Email
  - Student / Teacher Personal Mobile Number
  - **Father's Mobile Number** & **Mother's Mobile Number**
  - Department / Class / Program
  - Encrypted password storage (SHA-256)

### 3. 📊 Dashboard Page (`/dashboard`)
- **Key Performance Indicators (KPI Cards):**
  - **Total Students** (Cohort count)
  - **Average Marks** (%)
  - **Average Attendance** (%)
  - **Students at Risk** (Urgent highlight)
  - **Top Performing Students** (Dean's list)
- **Interactive Chart.js Visualizations:**
  - Performance Tier Breakdown (Doughnut Chart: Excellent, Good, Average, At-Risk)
  - Attendance % vs. Predicted Exam Marks (Comparative Bar Chart)
- **At-Risk Alert Table:** Immediate list of flagged students with direct parental phone contact triggers.

### 4. 👩‍🎓 Add / Edit Student Details Page (`/add-student`)
- Student ID / Roll No, Full Name, Class / Course, Age, Gender
- Personal Mobile, Father's Mobile, Mother's Mobile numbers
- 5 core academic input indicators:
  1. Attendance Percentage (%)
  2. Internal Assessment Marks (%)
  3. Assignment Marks (%)
  4. Previous Exam Marks (%)
  5. Daily Study Hours (hrs/day)
- Action Buttons:
  - **Save Student** (Automatically triggers ML model and saves record)
  - **Update Details** (For modifying existing student profiles)
  - **Reset Form**

### 5. 🤖 Performance Prediction Page (`/prediction`)
- Direct AI inference interface
- Choose from existing registered students dropdown (auto-fills all 5 inputs) OR enter custom values
- **Quick Preset Scenarios:**
  - *High Performer* (94% Attendance, 5.5 hrs study)
  - *Average* (76% Attendance, 3.0 hrs study)
  - *At-Risk Alert* (48% Attendance, 1.0 hr study)
- **Explainable AI Output Dossier:**
  - Predicted Score (%) and Letter Grade
  - Risk Level Badge: **Low (Green)**, **Medium (Amber)**, **High (Red)**
  - Diagnostic breakdown: Specific areas where the student needs improvement
  - Actionable, personalized intervention roadmap
  - Printable report view and 1-click save to student profile

### 6. 📑 Student Reports Page (`/reports`)
- Comprehensive cohort data table displaying ID, Name, Attendance, Internal, Assignment, Previous Exam, AI Predicted Score, and Risk Level
- **Real-Time Search Bar** (filters by ID, Name, or Course)
- **Risk Level Filter** (High, Medium, Low, All)
- **View Report Modal**: Inspect full student dossier, parent emergency numbers, and AI recommendations
- **Download CSV Report**: 1-click export of the entire cohort table
- **Print Dossier**: Formatted for browser print / PDF export

### 7. 🛠️ Teacher Backend & Model Operations (`/teacher-backend`)
- Real-time Machine Learning Telemetry:
  - Algorithm: **Random Forest Regressor (120 Estimators)**
  - Model Fit: **R² Score = 0.887**
  - Mean Absolute Error: **±2.73%**
  - Number of Training Samples: 600+
- **Feature Importance Weights** (Internal marks 28.4%, Previous exams 24.2%, Attendance 22.1%, Assignments 17.8%, Study hours 7.5%)
- **Retrain AI Model Button**: On-demand retraining on new student cohorts
- Registered Users & Parental Contact Directory table

---

## 🚀 How to Run the Project

### 1. Set Active Workspace
In the Antigravity IDE, open folder:
`C:\Users\Admin\.gemini\antigravity\scratch\student-performance-prediction`

### 2. Install Dependencies (Already Installed)
```powershell
pip install -r requirements.txt
```

### 3. Start the Flask Application
```powershell
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Default Login Credentials

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Teacher / Faculty** | `teacher` | `teacher123` | Full student management, prediction, reports, backend |
| **Administrator** | `admin` | `admin123` | Full access, retraining ML model, user auditing |
| **New Users** | *Self-Register* | *Chosen at registration* | Supports student/faculty registration with mother's & father's numbers |

---

## 📁 File Structure

```
student-performance-prediction/
│
├── app.py                      # Main Flask application with 12 routes & session auth
├── model.py                    # Scikit-learn Random Forest model training & inference
├── database.py                 # SQLite database setup, migrations & sample data seed
├── test_routes.py              # Automated 9-point integration test suite
├── requirements.txt            # Python package requirements
├── trained_model.joblib        # Persisted Random Forest model with metadata
├── student_prediction.db       # SQLite database with users and students
│
├── templates/                  # Jinja2 HTML5 Templates
│   ├── base.html               # Master layout with dark-blue navbar & academic theme
│   ├── index.html              # 1. 🏠 Home Page
│   ├── login.html              # 2. 🔐 Login & Registration Page
│   ├── dashboard.html          # 3. 📊 Dashboard with KPI cards & Chart.js
│   ├── add_student.html        # 4. 👩‍🎓 Add / Edit Student Details Page
│   ├── prediction.html         # 5. 🤖 AI Prediction Page with Explainable AI
│   ├── reports.html            # 6. 📑 Student Reports, Filters & CSV Export
│   └── teacher_backend.html    # 7. 🛠️ Teacher Backend & Model Operations
│
└── static/
    ├── css/
    │   └── style.css           # Academic CSS theme (light-blue/white bg, dark-blue navbar)
    └── js/
        └── main.js             # Client utilities (CSV export, live search, sample fillers)
```
