"""
Machine Learning and AI Prediction Module for Student Performance Prediction.
Uses Scikit-Learn RandomForestRegressor & GradientBoosting to predict final scores,
risk classifications, and generates Explainable AI diagnostics and action plans.
"""

import os
import joblib
import numpy as np

MODEL_FILE = os.path.join(os.path.dirname(__file__), "trained_model.joblib")

def generate_synthetic_training_data(n_samples=500, random_seed=42):
    """
    Generates realistic academic dataset:
    Features:
    0: attendance_pct (30 - 100)
    1: internal_marks (20 - 100)
    2: assignment_marks (20 - 100)
    3: previous_exam_marks (20 - 100)
    4: study_hours_per_day (0.5 - 8.0)
    """
    rng = np.random.RandomState(random_seed)
    
    attendance = rng.uniform(40, 98, n_samples)
    internal = rng.uniform(30, 98, n_samples)
    assignment = rng.uniform(35, 100, n_samples)
    previous_exam = rng.uniform(30, 98, n_samples)
    study_hours = rng.uniform(0.5, 7.5, n_samples)
    
    # Realistic correlated ground truth formula with non-linear interaction and gaussian noise
    # Attendance heavily affects assimilation; study hours amplify internal & previous marks
    base_score = (
        0.22 * attendance +
        0.28 * internal +
        0.18 * assignment +
        0.24 * previous_exam +
        1.6 * np.minimum(study_hours, 6.0)
    )
    
    # Penalty for critically low attendance (< 65%)
    attendance_penalty = np.where(attendance < 65, (65 - attendance) * 0.4, 0)
    
    # Slight random noise simulating exam-day factors
    noise = rng.normal(0, 2.5, n_samples)
    
    final_scores = base_score - attendance_penalty + noise
    final_scores = np.clip(final_scores, 20.0, 99.5)
    
    X = np.column_stack([attendance, internal, assignment, previous_exam, study_hours])
    y = final_scores
    return X, y

def train_model():
    """Trains a Random Forest Regressor and persists it."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score

    X, y = generate_synthetic_training_data(n_samples=600)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=120, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = float(r2_score(y_test, y_pred))
    mae = float(mean_absolute_error(y_test, y_pred))

    model_payload = {
        "model": model,
        "feature_names": ["Attendance", "Internal Marks", "Assignment Marks", "Previous Exam", "Study Hours"],
        "feature_importances": model.feature_importances_.tolist(),
        "r2_score": round(r2, 4),
        "mae_score": round(mae, 2),
        "samples_count": len(X)
    }

    joblib.dump(model_payload, MODEL_FILE)
    return model_payload

def get_or_load_model():
    if not os.path.exists(MODEL_FILE):
        return train_model()
    try:
        return joblib.load(MODEL_FILE)
    except Exception:
        return train_model()

def analyze_weaknesses_and_recommendations(attendance, internal, assignment, prev_exam, study_hours, predicted_score):
    """
    Explainable AI engine: analyzes inputs to give concrete, prioritized guidance.
    """
    weak_areas = []
    actions = []

    # 1. Attendance Analysis
    if attendance < 60.0:
        weak_areas.append("Critically Low Attendance (<60%): High danger of exam debarment.")
        actions.append("Must meet Course Coordinator immediately and attend every upcoming lecture without fail.")
    elif attendance < 75.0:
        weak_areas.append("Attendance Below Mandatory 75% Threshold.")
        actions.append("Prioritize attending next 15 lectures consecutively to regain clearance.")

    # 2. Study Habits Analysis
    if study_hours < 2.0:
        weak_areas.append(f"Insufficient Daily Study ({study_hours} hrs/day).")
        actions.append("Implement the Pomodoro Technique: dedicate at least 2.5 to 3.5 focused hours every evening.")
    elif study_hours > 5.0 and predicted_score < 70.0:
        weak_areas.append("High study duration but suboptimal retention.")
        actions.append("Shift from passive reading to active recall, practice tests, and flashcards.")

    # 3. Assessment & Internal Marks Analysis
    if internal < 50.0:
        weak_areas.append(f"Low Internal Test Score ({internal}%): Demonstrates conceptual difficulties in core syllabus.")
        actions.append("Enroll in remedial tutorial sessions and review teacher's lecture notes for previous quizzes.")

    if assignment < 60.0:
        weak_areas.append(f"Assignment Deficit ({assignment}%): Unsubmitted or incomplete homework.")
        actions.append("Complete pending coursework promptly; consult teaching assistants for problem-solving support.")

    if prev_exam < 50.0:
        weak_areas.append(f"Previous Term Exam Marks ({prev_exam}%) require immediate remediation.")
        actions.append("Solve 5 years of past university question papers under timed exam conditions.")

    # Synthesize overall categories
    if predicted_score >= 85.0:
        category = "Excellent"
        risk_level = "Low"
        grade_letter = "A+"
        if not actions:
            actions.append("Maintain consistent revision schedule. Participate in research competitions or peer tutoring.")
        if not weak_areas:
            weak_areas.append("No critical weaknesses detected. Student demonstrates mastery across criteria.")
    elif predicted_score >= 70.0:
        category = "Good"
        risk_level = "Low"
        grade_letter = "A"
        if not actions:
            actions.append("Refine exam presentation skills and target top percentile with extra practice.")
        if not weak_areas:
            weak_areas.append("Good consistency, with minor potential for score optimization.")
    elif predicted_score >= 50.0:
        category = "Average"
        risk_level = "Medium"
        grade_letter = "B"
        actions.append("Schedule bi-weekly progress review with faculty advisor.")
    else:
        category = "At-Risk"
        risk_level = "High"
        grade_letter = "C / Fail"
        actions.insert(0, "URGENT: Alert academic counselor and issue advisory notice to parents/guardians.")

    return {
        "predicted_score": round(float(predicted_score), 1),
        "predicted_category": category,
        "grade_letter": grade_letter,
        "risk_level": risk_level,
        "weak_areas": weak_areas,
        "actions": actions,
        "recommendation_summary": " ".join(actions[:2])
    }

def predict_student_performance(attendance, internal, assignment, prev_exam, study_hours):
    """
    Main prediction entry point.
    """
    # Safe bounds
    att = float(np.clip(attendance, 0.0, 100.0))
    intl = float(np.clip(internal, 0.0, 100.0))
    asgn = float(np.clip(assignment, 0.0, 100.0))
    prev = float(np.clip(prev_exam, 0.0, 100.0))
    sh = float(np.clip(study_hours, 0.0, 24.0))

    try:
        model_payload = get_or_load_model()
        model = model_payload["model"]
        input_features = np.array([[att, intl, asgn, prev, sh]])
        pred_raw = model.predict(input_features)[0]
    except Exception:
        # Robust heuristic fallback
        pred_raw = (0.22 * att + 0.28 * intl + 0.18 * asgn + 0.24 * prev + min(sh * 1.5, 6.0))
        if att < 65:
            pred_raw -= (65 - att) * 0.4

    predicted_score = float(np.clip(pred_raw, 15.0, 99.0))
    analysis = analyze_weaknesses_and_recommendations(att, intl, asgn, prev, sh, predicted_score)
    return analysis

if __name__ == "__main__":
    print("Testing ML model...")
    res = train_model()
    print(f"Model trained! R2: {res['r2_score']}, MAE: {res['mae_score']}")
    test_pred = predict_student_performance(85, 80, 90, 75, 4.0)
    print("Sample prediction:", test_pred)
