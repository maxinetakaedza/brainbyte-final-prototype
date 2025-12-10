# 🧠 BrainByte — AI-Powered Gamified Learning Platform


> **"Study. Earn. Grow."** — A playful, AI-driven platform that turns learning into a personalized journey with real career insights — built for Zimbabwean students.

---

## 🌟 Features

- **📚 StudyBuddy AI**: Tracks your progress over time, finds your strengths & weaknesses
- **🎯 Career Mapping AI**: Weekly reports with skill ratings + local career paths
- **🎮 Gamified Learning**: Quizzes, F1 racing game, BrainBits rewards
- **🛒 Student Marketplace**: Buy/sell notes, tutoring, revision packs
- **💰 Dual Economy**: BrainBits (in-app) + EcoCash Simulation (parent sponsorship)
- **🏫 Teacher Dashboard**: Monitor class analytics, issue vouchers, assign quizzes
- **📊 Weekly Cycle**: Reflect on Saturday → Get AI insights on Sunday

### Free vs Premium
| Free | Premium |
|------|---------|
| Basic weekly AI report | Deep mastery pathways |
| Simple explanations | Multi-step AI reasoning |
| 5 career matches | Full skill gap analysis |
| Limited quizzes | Unlimited + tournament access |

---

## 🚀 How to Run

### Backend (Mock AI API)
```bash
cd backend
pip install fastapi uvicorn[standard]
uvicorn app.main:app --reload --port 8000