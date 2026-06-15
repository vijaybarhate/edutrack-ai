import os
import sqlite3
import pandas as pd

DEFAULT_DB_PATH = "D:/lenovo LEAP/Capstone Project/data/edutrack.db"

def get_db_connection(db_path=DEFAULT_DB_PATH):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DEFAULT_DB_PATH):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)
    
    # Create academic_records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS academic_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        attendance_rate REAL NOT NULL,
        study_hours REAL NOT NULL,
        midterm_score REAL NOT NULL,
        past_score REAL NOT NULL,
        final_score REAL NOT NULL,
        at_risk INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (student_id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {db_path}")

def import_csv_to_db(csv_path, db_path=DEFAULT_DB_PATH):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")
        
    df = pd.read_csv(csv_path)
    
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    try:
        # Clear existing data to allow clean re-uploads
        cursor.execute("DELETE FROM academic_records")
        cursor.execute("DELETE FROM students")
        
        # Insert students (unique list)
        unique_students = df[['StudentID', 'Name']].drop_duplicates()
        for _, row in unique_students.iterrows():
            cursor.execute(
                "INSERT INTO students (student_id, name) VALUES (?, ?)",
                (int(row['StudentID']), row['Name'])
            )
            
        # Insert academic records
        for _, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO academic_records 
                (student_id, subject, attendance_rate, study_hours, midterm_score, past_score, final_score, at_risk)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    int(row['StudentID']),
                    row['Subject'],
                    float(row['Attendance_Rate']),
                    float(row['Study_Hours']),
                    float(row['Midterm_Score']),
                    float(row['Past_Score']),
                    float(row['Final_Score']),
                    int(row['At_Risk'])
                )
            )
        conn.commit()
        print(f"Successfully imported {len(df)} records into the database.")
    except Exception as e:
        conn.rollback()
        print(f"Error importing CSV to database: {e}")
        raise e
    finally:
        conn.close()

def get_students_summary(db_path=DEFAULT_DB_PATH):
    """
    Get a list of all students with summary statistics:
    - ID, Name, Avg Midterm Score, Avg Attendance Rate, Avg Study Hours, and count of failed subjects.
    """
    conn = get_db_connection(db_path)
    query = """
    SELECT 
        s.student_id,
        s.name,
        ROUND(AVG(r.midterm_score), 1) as avg_midterm,
        ROUND(AVG(r.attendance_rate), 1) as avg_attendance,
        ROUND(AVG(r.study_hours), 1) as avg_study_hours,
        SUM(r.at_risk) as actual_at_risk_subjects
    FROM students s
    LEFT JOIN academic_records r ON s.student_id = r.student_id
    GROUP BY s.student_id, s.name
    ORDER BY s.student_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_student_detail(student_id, db_path=DEFAULT_DB_PATH):
    """
    Get detailed records for a specific student.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # Get student name
    cursor.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return None
        
    student_name = student['name']
    
    # Get detailed records
    query = """
    SELECT subject, attendance_rate, study_hours, midterm_score, past_score, final_score, at_risk
    FROM academic_records
    WHERE student_id = ?
    """
    records_df = pd.read_sql_query(query, conn, params=(student_id,))
    conn.close()
    
    return {
        "student_id": student_id,
        "name": student_name,
        "records": records_df.to_dict(orient="records")
    }

def get_all_records(db_path=DEFAULT_DB_PATH):
    """
    Get all records in the database as a DataFrame (used for training the model).
    """
    conn = get_db_connection(db_path)
    query = """
    SELECT s.name, r.* 
    FROM academic_records r
    JOIN students s ON r.student_id = s.student_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_class_averages(db_path=DEFAULT_DB_PATH):
    """
    Get the class average score and attendance for each subject.
    """
    conn = get_db_connection(db_path)
    query = """
    SELECT 
        subject,
        ROUND(AVG(midterm_score), 1) as avg_midterm,
        ROUND(AVG(attendance_rate), 1) as avg_attendance,
        ROUND(AVG(study_hours), 1) as avg_study_hours
    FROM academic_records
    GROUP BY subject
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
