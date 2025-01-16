import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from app.route import router
from app.auth.route import router as auth_router
from starlette.middleware.sessions import SessionMiddleware
# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="ChatBot Service", version="1.0.0")

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    session_cookie="chatbot_session",    # Name of the cookie
    max_age=3600,                        # Session expires in 1 hour
    same_site="lax",                     # Cookie security setting
    https_only=False                     # Set to True in production with HTTPS
)

# Configure CORS
origins = ["*"]  # Allow all origins for development
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
    user=request.session.get("user")
    if user:
        return {"message": f"Welcome back, {user['name']}!"}
    else:
        return {"message": "This is a backend service for chatbot, please go to /docs to see the API documentation"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)