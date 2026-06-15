# EduTrack AI - QA Progress

## Map of Interaction Surfaces
- [ ] **Overview Dashboard**
  - KPI Cards (Total Students, Avg Attendance, etc.)
  - Charts (Subject Midterm, Risk Distribution)
  - At-Risk Student Table
- [ ] **Individual Lookup**
  - Student Selectbox
  - Performance Table (Subject, Midterm, Attendance, etc.)
  - Intervention Plan (Weakest Subject, Study Hours)
  - PDF/CSV Download Buttons
- [ ] **Risk Sandbox**
  - Inputs: Subject, Attendance %, Study Hours, Midterm %, Past Score %
  - Predict Button
  - Gauge Chart + Prediction Result
  - Intervention Scenario Planner
- [ ] **Dataset Manager**
  - CSV Uploader
  - Upload & Retrain Button
  - Force Retrain Button
- [ ] **Backend API**
  - `/` (Health check)
  - `/students` (List)
  - `/students/{id}` (Detail)
  - `/class-stats` (Averages)
  - `/records` (All)
  - `/predict` (ML Prediction)
  - `/upload` (CSV Import)
  - `/retrain` (Model Training)

## Stress Tests & Findings
- [ ] Empty student list handling
- [ ] Invalid CSV upload handling
- [ ] Sandbox boundary values (0%, 100%, negative study hours)
- [ ] Backend disconnect handling in Frontend
- [ ] UI Responsiveness at 768px (Mobile)

## Issues Log
- [ ] [SEVERITY] <description> — <file/page/endpoint>
