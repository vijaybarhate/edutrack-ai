# Capstone Project Submission Report: EduTrack AI

## 1. Selected SDG and Reason for Selection
* **Selected SDG**: Goal 4 – Quality Education
* **Focus of the SDG**: SDG 4 focuses on ensuring inclusive and equitable quality education and promoting lifelong learning opportunities for all.
* **Importance of the Issue**: Educational systems frequently fail to address performance gaps early enough. Student performance declines and attendance gaps go completely unnoticed until it is too late (e.g., after final exams), leading to preventable academic failures and course repetitions. Proactive tracking is critical to maintaining high educational quality and equity.

---

## 2. Problem Statement
* **What is the problem?**: Teachers, students, and school administrators lack an automated early warning system for academic risk, preventing timely educational intervention.
* **Where does this problem exist?**: This issue commonly exists in schools with manual progress-tracking systems and low student-to-teacher ratios, where teachers cannot individually monitor daily performance trends across multiple subjects.
* **Who is affected?**: The problem directly affects students who are at risk of failing their subjects and dropping out, as well as teachers who lack the tools to perform early interventions.
* **Why is it serious?**: Without early prediction, performance deficiencies compound. If not solved, this leads to increased course failure rates, higher student dropout percentages, and long-term socio-economic challenges for the affected youth.

---

## 3. Proposed Solution
* **What the project is**: **EduTrack AI** is an intelligent educational assistant that uses machine learning to identify students at risk of academic failure.
* **How the system works**: The application collects early-term academic data (attendance rate, midterm marks, study hours, past history) and inputs them into a machine learning ensemble (Random Forest + Logistic Regression) that calculates the exact failure risk per subject.
* **How it helps solve the problem**: It flags students as High, Medium, or Low risk long before final exams, automatically triggering a personalized study plan recommendation to adjust weekly study hours for their weakest subject.
* **Who will use the application**: School administrators, teachers, and guidance counselors will use the dashboard for class-wide monitoring, while students and parents will receive the individual PDF performance reports.

---

## 4. Project Features
* **Overview Dashboard**: A high-level visual analytics panel displaying KPI cards for class pass rates and average attendance, paired with Plotly charts tracking risk distribution and subject-wise averages to help teachers monitor whole-class performance.
* **Risk Prediction Engine**: A machine learning-powered sandbox allowing users to input hypothetical attendance and score parameters to instantly calculate failure risk using a Random Forest and Logistic Regression soft-voting ensemble.
* **Personalized Recommendations**: A rule-based intervention logic that automatically identifies a student's weakest subject relative to the class average and calculates the precise addition to weekly study hours needed to mitigate risk (e.g., +5 hours/week if failing).
* **Exportable Reports**: A reporting tool that allows teachers to instantly generate and download formatted PDF progress reports and CSV raw data containing student grades, risk ratings, and custom action plans.

---

## 5. Technologies Used (Tech Stack)
* **Programming Language**: Python (Core application logic and ML modeling)
* **Machine Learning**: Scikit-Learn (Random Forest Classifier + Logistic Regression voting ensemble, preprocessing pipelines)
* **Backend Framework**: FastAPI (RESTful API serving prediction, data storage, and model retraining)
* **Frontend Interface**: Streamlit (Responsive web dashboard and interactive user interface)
* **Database**: SQLite (Local database for storing student records and tracking academic history)
* **Data Manipulation**: Pandas and Numpy (Data engineering and processing)
* **Visualization**: Plotly (Interactive dashboard charts)
* **PDF Generation**: FPDF2 (Dynamic report layout and export)

---

## 7. Open Source Repository
* **GitHub Link**: [https://github.com/vijaybarhate/edutrack-ai](https://github.com/vijaybarhate/edutrack-ai)
* **Live Application**: [https://edutrack-ai-01.streamlit.app](https://edutrack-ai-01.streamlit.app)
* **Backend API**: [https://edutrack-backend-dsss.onrender.com](https://edutrack-backend-dsss.onrender.com)

---

## 8. Future Scope
* **Chatbot Tutor**: Integrate a generative AI chatbot tutor using Google Gemini API to provide students with immediate, subject-specific tutoring assistance on their weakest topics.
* **Mobile Application**: Build a cross-platform mobile companion app for students and parents to view weekly progress reports and study plans on the go.
* **LMS Integration**: Create integration plugins for standard Learning Management Systems (LMS) like Moodle, Canvas, or Google Classroom to automatically sync attendance and grades.

---

## 7. Conclusion & Summary
EduTrack AI demonstrates the power of integrating machine learning and data analytics to serve SDG 4 (Quality Education). By converting static student data into actionable early warning indicators, teachers can intervene before performance gaps widen. The capstone showcases a complete full-stack machine learning pipeline from synthetic dataset generation to API-first serving and interactive visualization, offering an scalable, automated approach to supporting student success.
