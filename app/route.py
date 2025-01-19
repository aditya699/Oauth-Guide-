'''
Author: Aditya Bhatt 
Date: 13-01-2025
'''
from fastapi import FastAPI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi import APIRouter

from fastapi import Depends, HTTPException
from fastapi import Request

class ChatResponse(BaseModel):
    message: str

load_dotenv()

os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")


router = APIRouter()


async def verify_session(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.post("/get_chat_response")
async def get_chat_response(
    message: ChatResponse, 
    user: dict = Depends(verify_session)  # Add this dependency
):
    try:
        user_message = message.message
        chat = ChatAnthropic(model="claude-3-haiku-20240307")
        response = chat.invoke(user_message)
        return {"response": response.content}
    except Exception as e:
        return {"error": str(e)}



