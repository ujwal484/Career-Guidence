from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

# Metadata for Swagger UI
app = FastAPI(
    title="SkillPath API",
    description="Chose Your Career Wisely.",
    version="1.0.0",
    contact={
        "name": "SkillPath Team",
        "email": "support@skillpath.com",
    },
)

# --- Enable CORS ---
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",   # Another dev option
    "*"                        # Allow all origins (use carefully in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)

# Request model
class UserInput(BaseModel):
    skills: list[str]
    interests: list[str]

# Response model for root/health
class MessageResponse(BaseModel):
    message: str

@app.get("/", response_model=MessageResponse, tags=["Root"])
def read_root():
    """
    Root endpoint for checking if the API is running.
    """
    return {"message": "SkillPath API is working 🚀"}

@app.get("/health", response_model=MessageResponse, tags=["System"])
def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {"message": "Healthy ✅"}

@app.post("/recommend", tags=["Career Recommendation"])
def recommend(user_input: UserInput):
    """
    Recommend a career path based on skills and interests.
    Matches careers from careers.json using a scoring system.
    """
    with open("careers.json", "r", encoding="utf-8") as f:
        careers = json.load(f)

    best_match = None
    best_score = 0

    for career in careers:
        # Count matching skills
        skill_score = sum(
            skill.lower() in [s.lower() for s in career["skills"]]
            for skill in user_input.skills
        )

        # Count matching interests
        interest_score = sum(
            interest.lower() in [i.lower() for i in career["interests"]]
            for interest in user_input.interests
        )

        total_score = skill_score + interest_score

        if total_score > best_score:
            best_score = total_score
            best_match = career

    if best_match:
        return {
            "career": best_match["career"],
            "description": best_match["description"],
            "roadmap": best_match["roadmap"],
            "resources": best_match["resources"]
        }

    return {"message": "No matching career found. Try different skills or interests."}
