import os
import random
import pandas as pd
import numpy as np

def generate_student_dataset(output_path, num_students=50):
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", 
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", 
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley", 
        "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle", 
        "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", 
        "Edward", "Deborah"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", 
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", 
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", 
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", 
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", 
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", 
        "Carter", "Roberts"
    ]
    
    subjects = ["Math", "Science", "English", "History", "Computer Science"]
    
    # Generate 50 unique names
    student_names = []
    for i in range(num_students):
        fn = first_names[i % len(first_names)]
        ln = last_names[i % len(last_names)]
        student_names.append(f"{fn} {ln}")
    
    data = []
    student_id_start = 1001
    
    for i, name in enumerate(student_names):
        student_id = student_id_start + i
        
        # Determine student profile (e.g. diligent, average, struggling) to create realistic correlations
        profile_rand = random.random()
        if profile_rand < 0.25:
            # Struggling student profile: low attendance, low study hours, low past scores
            base_attendance = random.randint(45, 70)
            base_study_hours = random.randint(1, 3)
            base_past_score = random.randint(30, 55)
        elif profile_rand < 0.8:
            # Average student profile
            base_attendance = random.randint(70, 90)
            base_study_hours = random.randint(3, 7)
            base_past_score = random.randint(55, 78)
        else:
            # Diligent student profile
            base_attendance = random.randint(90, 100)
            base_study_hours = random.randint(7, 12)
            base_past_score = random.randint(78, 98)
            
        for subject in subjects:
            # Subject specific variations
            sub_diff = random.randint(-12, 8)  # subject difficulty variance
            study_var = max(1, base_study_hours + random.randint(-2, 2))
            attendance_var = max(40, min(100, base_attendance + random.randint(-5, 5)))
            past_score_var = max(25, min(100, base_past_score + sub_diff + random.randint(-5, 5)))
            
            # Midterm score is highly correlated with attendance, study hours and past performance
            midterm_noise = random.randint(-10, 10)
            midterm = 0.35 * past_score_var + 0.3 * attendance_var + 2.0 * study_var + 5 + midterm_noise
            midterm = max(15.0, min(100.0, midterm))
            
            # Final score formula - slightly harder to pass without effort
            final_noise = random.randint(-8, 8)
            final_score = 0.45 * midterm + 0.2 * attendance_var + 1.5 * study_var + 0.15 * past_score_var + final_noise
            final_score = max(15.0, min(100.0, final_score))
            
            # Risk labeling: 1 if Final_Score < 50 (Fail), else 0
            at_risk = 1 if final_score < 50.0 else 0
            
            data.append({
                "StudentID": student_id,
                "Name": name,
                "Subject": subject,
                "Attendance_Rate": round(attendance_var, 1),
                "Study_Hours": round(study_var, 1),
                "Midterm_Score": round(midterm, 1),
                "Past_Score": round(past_score_var, 1),
                "Final_Score": round(final_score, 1),
                "At_Risk": at_risk
            })
            
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully saved to: {output_path}")
    print(f"Total rows: {len(df)}")
    print(f"At-risk instances: {df['At_Risk'].sum()} out of {len(df)} ({round(df['At_Risk'].mean() * 100, 1)}%)")

if __name__ == "__main__":
    generate_student_dataset("D:/lenovo LEAP/Capstone Project/data/student_data.csv")
