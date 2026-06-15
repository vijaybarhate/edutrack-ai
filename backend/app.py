import os
import pickle
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Import local database and training modules
from backend.database import (
    init_db,
    import_csv_to_db,
    get_students_summary,
    get_student_detail,
    get_all_records,
    get_class_averages
)
from notebooks.train_model import train_and_save_model

app = FastAPI(
    title="EduTrack AI Backend",
    description="SDG 4 Quality Education Early Risk Prediction API",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = "D:/lenovo LEAP/Capstone Project"
DB_PATH = os.path.join(BASE_DIR, "data/edutrack.db")
CSV_PATH = os.path.join(BASE_DIR, "data/student_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models/ensemble_model.pkl")

# Pydantic schemas
class PredictRequestItem(BaseModel):
    Subject: str
    Attendance_Rate: float
    Study_Hours: float
    Midterm_Score: float
    Past_Score: float

class PredictRequest(BaseModel):
    records: List[PredictRequestItem]

class PredictResponseItem(BaseModel):
    Subject: str
    Risk_Probability: float
    At_Risk: int

class PredictResponse(BaseModel):
    predictions: List[PredictResponseItem]

# Global model variable
model_pipeline = None

def load_model():
    global model_pipeline
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                model_pipeline = pickle.load(f)
            print("Ensemble model pipeline loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            model_pipeline = None
    else:
        print("Model file not found. Prediction endpoint will be unavailable until trained.")
        model_pipeline = None

@app.on_event("startup")
def startup_event():
    # Initialize DB and import default CSV if available
    init_db(DB_PATH)
    if os.path.exists(CSV_PATH):
        import_csv_to_db(CSV_PATH, DB_PATH)
    
    # Load the trained model
    load_model()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": "EduTrack AI",
        "sdg_alignment": "Goal 4 - Quality Education",
        "model_loaded": model_pipeline is not None
    }

@app.get("/students")
def get_students():
    try:
        df = get_students_summary(DB_PATH)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/students/{student_id}")
def get_student(student_id: int):
    detail = get_student_detail(student_id, DB_PATH)
    if not detail:
        raise HTTPException(status_code=404, detail="Student not found")
    return detail

@app.get("/class-stats")
def get_stats():
    try:
        averages = get_class_averages(DB_PATH)
        return averages.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/records")
def get_records():
    try:
        df = get_all_records(DB_PATH)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/predict", response_model=PredictResponse)
def predict_risk(request: PredictRequest):
    global model_pipeline
    if model_pipeline is None:
        # Try loading again in case it was created recently
        load_model()
        if model_pipeline is None:
            raise HTTPException(
                status_code=503, 
                detail="Model is not trained/loaded. Please train the model first by calling /retrain."
            )
            
    try:
        # Convert request items to DataFrame for pipeline preprocessing
        input_data = []
        for item in request.records:
            input_data.append({
                "Subject": item.Subject,
                "Attendance_Rate": item.Attendance_Rate,
                "Study_Hours": item.Study_Hours,
                "Midterm_Score": item.Midterm_Score,
                "Past_Score": item.Past_Score
            })
        
        df_input = pd.DataFrame(input_data)
        
        # Predict using the loaded pipeline (handles scaling and encoding internally)
        probabilities = model_pipeline.predict_proba(df_input)[:, 1]
        predictions = model_pipeline.predict(df_input)
        
        response_items = []
        for i, item in enumerate(request.records):
            response_items.append(PredictResponseItem(
                Subject=item.Subject,
                Risk_Probability=float(probabilities[i]),
                At_Risk=int(predictions[i])
            ))
            
        return PredictResponse(predictions=response_items)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
    try:
        # Save file to disk
        contents = await file.read()
        with open(CSV_PATH, "wb") as f:
            f.write(contents)
            
        # Import file contents to database
        import_csv_to_db(CSV_PATH, DB_PATH)
        
        # Retrain the model in the background or synchronously
        train_and_save_model(CSV_PATH, os.path.join(BASE_DIR, "models"))
        load_model()
        
        return {
            "message": "Dataset successfully uploaded, imported to database, and model retrained.",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload/Training failed: {str(e)}")

@app.post("/retrain")
def retrain_model():
    try:
        # Fetch data from DB and save temporarily to CSV for standard training pipeline
        df = get_all_records(DB_PATH)
        if df.empty:
            raise HTTPException(status_code=400, detail="No data in database to train on.")
            
        # Format df columns to match expected training columns
        train_df = df.rename(columns={
            'student_id': 'StudentID',
            'name': 'Name',
            'subject': 'Subject',
            'attendance_rate': 'Attendance_Rate',
            'study_hours': 'Study_Hours',
            'midterm_score': 'Midterm_Score',
            'past_score': 'Past_Score',
            'final_score': 'Final_Score',
            'at_risk': 'At_Risk'
        })
        train_df = train_df[['StudentID', 'Name', 'Subject', 'Attendance_Rate', 'Study_Hours', 'Midterm_Score', 'Past_Score', 'Final_Score', 'At_Risk']]
        train_df.to_csv(CSV_PATH, index=False)
        
        # Train model
        train_and_save_model(CSV_PATH, os.path.join(BASE_DIR, "models"))
        load_model()
        
        return {"message": "Model retrained successfully on latest database records."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")
