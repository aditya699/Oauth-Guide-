import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from dotenv import load_dotenv
from app.route import router
from app.auth.route import router as auth_router
from starlette.middleware.sessions import SessionMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="ChatBot Service", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    session_cookie="chatbot_session",
    max_age=3600,
    same_site="lax",
    https_only=False
)

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/chat", tags=["chat"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Root endpoint
@app.get("/")
async def root(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(
            "chat.html", 
            {"request": request, "user": user}
        )
    return templates.TemplateResponse(
        "login.html", 
        {"request": request}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)