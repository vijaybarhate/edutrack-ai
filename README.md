# EduTrack AI 🎓

EduTrack AI is a machine learning-powered student performance tracking system and early warning classifier aligned with **UN Sustainable Development Goal 4 (Quality Education)**. It predicts student pass/fail risk per subject based on midterm scores, attendance, study hours, and historical scores, and generates personalized academic intervention plans.

---

## 🚀 Key Features

1. **Academic Risk Classifier**: Soft-voting ensemble combining **Random Forest** and **Logistic Regression** to output the probability of a student being "At Risk" (failing) in any subject.
2. **Interactive Streamlit Dashboard**:
   - **Overview Analytics**: Class-wide average metrics, risk distributions, and correlation scatter plots.
   - **Student Lookup**: Search profiles, view subject performance breakdowns, and analyze risk trends.
   - **Risk Prediction Sandbox**: Real-time "what-if" scenario simulator for testing interventions.
   - **Dataset Upload**: Interface to upload CSV datasets, automatically update SQLite, and trigger model retraining.
3. **Personalized Recommendations**: Identifies a student's weakest subject relative to class averages and recommends specific increases in weekly study hours.
4. **Report Export**: Exports structured student report cards as formatted **PDFs** or raw **CSVs**.
5. **REST API**: Built with **FastAPI** to serve student records and run ML predictions.
6. **SQLite Database**: Standardized relational schema to persist student demographics and academic records.

---

## 📁 Project Structure

```text
EduTrack AI/
├── backend/
│   ├── app.py                # FastAPI server (endpoints, Pydantic schemas, routing)
│   └── database.py           # SQLite database utility (tables, insertions, queries)
├── data/
│   ├── generate_data.py      # Synthetic data generator script
│   └── student_data.csv      # Generated student dataset (50 students, 5 subjects)
├── frontend/
│   └── app.py                # Streamlit dashboard app (UI, Plotly charts, PDF export)
├── models/
│   └── ensemble_model.pkl    # Trained Scikit-Learn pipeline
├── notebooks/
│   ├── model_training.ipynb  # Jupyter Notebook for EDA & model training
│   └── train_model.py        # Standalone Python script for training the model
├── Capstone_Project_Submission.md # Capstone submission document mapping SDG criteria
├── requirements.txt          # Python dependencies
└── README.md                 # Running instructions (this file)
```

---

## 🛠️ Setup Instructions

### 1. Prerequisite Installation
Ensure Python (version 3.8 to 3.12 recommended) is installed on your system.

### 2. Install Dependencies
Open a terminal inside the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Generate the Sample Dataset
Generate a synthetic dataset of 50 students across 5 subjects (Math, Science, English, History, Computer Science) with realistic distributions:
```bash
python data/generate_data.py
```
This generates `data/student_data.csv`.

### 4. Train the ML Ensemble Model
Train the Random Forest + Logistic Regression pipeline and save it as `models/ensemble_model.pkl`:
```bash
python notebooks/train_model.py
```

### 5. Run the FastAPI Backend
Start the backend server on `http://127.0.0.1:8000`:
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```
*(You can access the interactive API docs at `http://127.0.0.1:8000/docs`)*

### 6. Run the Streamlit Dashboard
In a **new terminal window**, start the Streamlit frontend:
```bash
streamlit run frontend/app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 📊 ML Ensemble Details
The model is structured as a Scikit-Learn `Pipeline` containing:
* **Preprocessing**: `ColumnTransformer` applying `StandardScaler` to numerical inputs (Attendance, Study Hours, Midterm, Past Score) and `OneHotEncoder` to categorical inputs (Subject).
* **Classifier**: `VotingClassifier` performing soft-voting (averaging probabilities) of:
  * **Random Forest Classifier**: For identifying complex non-linear combinations of scores and attendance.
  * **Logistic Regression**: For robust linear baseline classification.

---

## 👥 Authors & License
Developed as an AI Capstone Project for SDG 4 (Quality Education). Licensed under the MIT License.
