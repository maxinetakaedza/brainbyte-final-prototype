from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

app = FastAPI(title="BrainByte Mock AI API", description="StudyBuddy + Career Mapping AI (Free vs Premium)")

# CORS — allows frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== MODELS ==================

class SessionData(BaseModel):
    user_id: str
    grade: str  # "Primary" or "Secondary"
    subject: str
    topic: Optional[str] = None
    score: Optional[int] = None  # 0-100
    time_spent_sec: float
    correct_answers: int
    total_questions: int
    difficulty_rating: Optional[int] = None  # 1-5
    is_quiz: bool = False
    engagement_minutes: Optional[float] = None
    weekly_reflection: Optional[Dict[str, str]] = None  # Sat: hardest/easiest/etc.

class StudyBuddyResponse(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    confidence_score: float  # 0–100
    trend: str  # "improving", "declining", "stable"
    pain_points: List[str]
    weekly_mission: Dict[str, Any]
    explanation_depth: str  # "basic" or "deep"

class CareerReportResponse(BaseModel):
    careers: List[str]
    skill_ratings: Dict[str, int]  # 1-5
    explanations: List[str]
    resources: List[str]
    report_type: str  # "free" or "premium"

# ================== IN-MEMORY STORAGE (for demo) ==================
# In real app: use database. Here: just simulate.
SESSIONS_DB = {}  # user_id → list of sessions

def get_mock_study_profile(user_id: str, is_premium: bool = False):
    # Simulate StudyBuddy AI analysis
    strengths = ["Math", "Biology"]
    weaknesses = ["Physics", "Chemical Equations"]
    pain_points = ["Struggles with Newton's Laws", "Confuses mole calculations"]

    if is_premium:
        weekly_mission = {
            "title": "Master Physics Fundamentals",
            "steps": [
                "Watch: 'Forces & Motion' video",
                "Complete 10 practice problems",
                "Take diagnostic quiz",
                "Get AI feedback on errors"
            ],
            "estimated_time_min": 45
        }
        explanation_depth = "deep"
    else:
        weekly_mission = {
            "title": "Practice 5 Physics Problems",
            "steps": ["Go to Study Session → Physics → Forces"],
            "estimated_time_min": 10
        }
        explanation_depth = "basic"

    return StudyBuddyResponse(
        strengths=strengths,
        weaknesses=weaknesses,
        confidence_score=68.5,
        trend="improving",
        pain_points=pain_points,
        weekly_mission=weekly_mission,
        explanation_depth=explanation_depth
    )

def get_mock_career_report(user_id: str, is_premium: bool = False):
    careers = [
        "Biomedical Engineer",
        "Data Analyst",
        "Science Teacher",
        "Software Developer",
        "Environmental Scientist"
    ]
    skill_ratings = {
        "Problem-solving": 4,
        "Creativity": 3,
        "People skills": 2,
        "Tech affinity": 5,
        "Analytical skills": 4
    }
    explanations = [
        "Strong in logic & tech → great for software roles",
        "You enjoy explaining concepts → teaching fits"
    ]
    resources = [
        "https://example.com/biomed-career-zw",
        "https://youtube.com/watch?v=physics_fundamentals"
    ]

    if is_premium:
        explanations = [
            "You scored 4/5 in analytical thinking because you consistently solve multi-step math problems correctly.",
            "Your low 'People skills' (2/5) comes from low engagement in group chats — try Interest Chat Rooms!"
        ]
        resources += [
            "Micro-course: 'Intro to Coding (Premium)'",
            "Skill gap plan: +30% Physics practice → unlock Engineering path"
        ]
        report_type = "premium"
    else:
        report_type = "free"

    return CareerReportResponse(
        careers=careers,
        skill_ratings=skill_ratings,
        explanations=explanations,
        resources=resources[:2] if not is_premium else resources,
        report_type=report_type
    )

# ================== API ENDPOINTS ==================

@app.get("/")
def root():
    return {
        "message": "🧠 BrainByte Mock AI API Online",
        "endpoints": {
            "POST /ai/record-session": "Log study/quiz data",
            "GET /ai/study-profile/{user_id}": "Get StudyBuddy insights",
            "GET /ai/career-report/{user_id}": "Get weekly career report"
        }
    }

@app.post("/ai/record-session")
def record_session( SessionData):
    """StudyBuddy AI: store session data for weekly analysis."""
    uid = data.user_id
    if uid not in SESSIONS_DB:
        SESSIONS_DB[uid] = []
    SESSIONS_DB[uid].append(data.dict())
    return {
        "status": "success",
        "message": f"Session stored for {uid}. StudyBuddy AI will analyze it weekly.",
        "total_sessions": len(SESSIONS_DB[uid])
    }

@app.get("/ai/study-profile/{user_id}")
def get_study_profile(user_id: str, is_premium: bool = False):
    """Free: basic insights. Premium: deep mastery pathway."""
    return get_mock_study_profile(user_id, is_premium)

@app.get("/ai/career-report/{user_id}")
def get_career_report(user_id: str, is_premium: bool = False):
    """Sunday: Career Mapping AI runs. Free = list. Premium = full roadmap."""
    return get_mock_career_report(user_id, is_premium)

# Optional: return stored sessions (for debugging)
@app.get("/debug/sessions/{user_id}")
def debug_sessions(user_id: str):
    return SESSIONS_DB.get(user_id, [])