import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="PlacementIQ — Industry Placement & Skill Analytics API",
    description="Machine Learning & Deep Learning Placement Prediction System across Engineering, CS, Business & General Higher Education",
    version="3.0.0"
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

MODEL_FILE = "placement_pipeline.joblib"
METADATA_FILE = "model_metadata.json"

pipeline = None
metadata = None

def load_resources():
    global pipeline, metadata
    if os.path.exists(MODEL_FILE):
        pipeline = joblib.load(MODEL_FILE)
        print(f"Loaded ML model pipeline from {MODEL_FILE}")
    else:
        print(f"Warning: {MODEL_FILE} not found.")

    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)
        print(f"Loaded metadata from {METADATA_FILE}")
    else:
        print(f"Warning: {METADATA_FILE} not found.")

@app.on_event("startup")
def startup_event():
    load_resources()

class StudentData(BaseModel):
    full_name: Optional[str] = Field("Alex Smith", description="Student / Candidate Full Name")
    target_role: Optional[str] = Field("Software Engineer", description="Target Industry Role")
    github_url: Optional[str] = Field("", description="GitHub Profile URL")
    linkedin_url: Optional[str] = Field("", description="LinkedIn Profile URL")
    portfolio_url: Optional[str] = Field("", description="Portfolio / Personal Website URL")
    
    ssc_p: float = Field(..., ge=0.0, le=100.0, description="10th Grade Percentage")
    hsc_p: float = Field(..., ge=0.0, le=100.0, description="12th Grade Percentage")
    degree_p: float = Field(..., ge=0.0, le=100.0, description="Degree Percentage")
    etest_p: float = Field(..., ge=0.0, le=100.0, description="Employability Test Percentage")
    
    coding_score: float = Field(70.0, ge=0.0, le=100.0, description="Technical / Coding Score")
    communication_score: float = Field(75.0, ge=0.0, le=100.0, description="Communication / Soft Skills Score")
    projects_count: int = Field(2, ge=0, le=15, description="Number of Completed Projects")
    certifications_count: int = Field(1, ge=0, le=10, description="Number of Industry Certifications")
    
    gender: str = Field("M", description="'M' or 'F'")
    ssc_b: str = Field("Central", description="'Central' or 'Others'")
    hsc_b: str = Field("Central", description="'Central' or 'Others'")
    hsc_s: str = Field("Science", description="'Commerce', 'Science', or 'Arts'")
    degree_t: str = Field("Sci&Tech", description="'Sci&Tech', 'Comm&Mgmt', or 'Others'")
    workex: str = Field("No", description="'Yes' or 'No'")

@app.get("/", response_class=HTMLResponse)
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>PlacementIQ API Backend Running</h2><p>Building interface...</p>")

@app.get("/api/model-info")
def get_model_info():
    if not metadata:
        load_resources()
    if not metadata:
        raise HTTPException(status_code=500, detail="Model metadata not found. Please train model first.")
    return JSONResponse(content=metadata)

@app.post("/api/predict")
def predict_placement(data: StudentData):
    global pipeline
    if pipeline is None:
        load_resources()
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Model pipeline not available.")

    try:
        feature_dict = {
            'ssc_p': float(data.ssc_p),
            'hsc_p': float(data.hsc_p),
            'degree_p': float(data.degree_p),
            'etest_p': float(data.etest_p),
            'coding_score': float(data.coding_score),
            'communication_score': float(data.communication_score),
            'projects_count': int(data.projects_count),
            'certifications_count': int(data.certifications_count),
            'gender_M': 1 if data.gender.upper() == 'M' else 0,
            'ssc_b_Others': 1 if data.ssc_b.capitalize() == 'Others' else 0,
            'hsc_b_Others': 1 if data.hsc_b.capitalize() == 'Others' else 0,
            'hsc_s_Commerce': 1 if data.hsc_s.capitalize() == 'Commerce' else 0,
            'hsc_s_Science': 1 if data.hsc_s.capitalize() == 'Science' else 0,
            'degree_t_Others': 1 if data.degree_t == 'Others' else 0,
            'degree_t_Sci&Tech': 1 if data.degree_t in ['Sci&Tech', 'Sci & Tech'] else 0,
            'workex_Yes': 1 if data.workex.capitalize() in ['Yes', 'Y', '1'] else 0
        }

        df_input = pd.DataFrame([feature_dict])
        
        if metadata and 'feature_cols' in metadata:
            # Re-order columns to match trained pipeline expectation
            df_input = df_input[metadata['feature_cols']]

        prediction = int(pipeline.predict(df_input)[0])
        probabilities = pipeline.predict_proba(df_input)[0]

        prob_placed = float(probabilities[1])
        prob_not_placed = float(probabilities[0])

        verdict = "Placed" if prediction == 1 else "Needs Improvement"
        confidence = float(np.max(probabilities))

        # Personalised recommendations & skill insights
        insights = []
        recommendations = []

        # Technical & Soft Skills Evaluation
        if data.coding_score >= 80:
            insights.append("High technical & coding proficiency — strong competitive edge for technical screening.")
        elif data.coding_score < 60:
            recommendations.append("Enhance core programming & algorithmic problem-solving on platforms like LeetCode / HackerRank.")

        if data.communication_score >= 80:
            insights.append("Exceptional soft skills & verbal communication — excellent fit for leadership & client-facing interview rounds.")
        elif data.communication_score < 60:
            recommendations.append("Participate in mock interviews & public speaking sessions to boost soft skills score.")

        if data.projects_count >= 3:
            insights.append(f"Impressive portfolio featuring {data.projects_count} end-to-end industry & capstone projects.")
        elif data.projects_count < 2:
            recommendations.append("Build at least 2 full-stack / domain capstone projects and showcase them on GitHub.")

        if data.certifications_count >= 2:
            insights.append(f"Validated expertise with {data.certifications_count} professional industry certifications.")

        # Academic Strengths
        if data.degree_p >= 75:
            insights.append("Consistent high academic performance in undergraduate degree.")
        if data.workex.capitalize() == 'Yes':
            insights.append("Prior internship / work experience adds significant practical value to recruiter evaluations.")

        # Calculate Profile Link Completeness
        has_github = bool(data.github_url and len(data.github_url.strip()) > 5)
        has_linkedin = bool(data.linkedin_url and len(data.linkedin_url.strip()) > 5)
        has_portfolio = bool(data.portfolio_url and len(data.portfolio_url.strip()) > 5)

        links_count = sum([has_github, has_linkedin, has_portfolio])
        if links_count == 3:
            insights.append("Comprehensive online professional footprint (GitHub, LinkedIn, Portfolio verified).")
        elif links_count == 0:
            recommendations.append("Add your GitHub, LinkedIn, and Portfolio links to boost recruiter visibility.")

        # Expected CTC Band Calculation
        if prediction == 1:
            base_ctc = 4.0 + (data.coding_score * 0.05) + (data.projects_count * 0.4) + (data.degree_p * 0.03) + (1.5 if data.workex.capitalize() == 'Yes' else 0.0)
            ctc_min = round(base_ctc, 1)
            ctc_max = round(base_ctc * 1.35, 1)
            estimated_ctc = f"{ctc_min} - {ctc_max} LPA"
        else:
            estimated_ctc = "3.5 - 5.0 LPA (Post Skill Upgrade)"

        skills_score = round((data.coding_score * 0.35 + data.communication_score * 0.35 + min(data.projects_count * 5, 20) + min(data.certifications_count * 2.5, 10)), 1)

        return JSONResponse(content={
            "full_name": data.full_name or "Candidate",
            "target_role": data.target_role or "General Industry Role",
            "github_url": data.github_url or "",
            "linkedin_url": data.linkedin_url or "",
            "portfolio_url": data.portfolio_url or "",
            "prediction": prediction,
            "verdict": verdict,
            "probability_placed": round(prob_placed * 100, 2),
            "probability_not_placed": round(prob_not_placed * 100, 2),
            "confidence_score": round(confidence * 100, 2),
            "skills_score": skills_score,
            "estimated_ctc": estimated_ctc,
            "insights": insights if insights else ["Well-rounded academic candidate profile."],
            "recommendations": recommendations if recommendations else ["Focus on mastering technical domain fundamentals."]
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
