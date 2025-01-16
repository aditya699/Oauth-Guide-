'''
Author: Aditya Bhatt 
Date: 15-01-2025 11:00 AM

NOTE:

'''
from fastapi import APIRouter,Request
from fastapi.responses import RedirectResponse
from .config import MICROSOFT_CONFIG
from urllib.parse import urlencode
import requests
from fastapi import HTTPException

router = APIRouter()

@router.get("/login")
async def login(request: Request):
      # Check if user is already logged in
    if request.session.get('user'):
        return RedirectResponse(url="/")  # Redirect to home if already logged in
    query_params = {
        "client_id": MICROSOFT_CONFIG["client_id"],
        "response_type": "code",
        "redirect_uri": MICROSOFT_CONFIG["redirect_uri"],
        "scope": " ".join(MICROSOFT_CONFIG["scopes"]),
    }
    auth_url = f"{MICROSOFT_CONFIG['authorize_endpoint']}?{urlencode(query_params)}"
    return RedirectResponse(url=auth_url)

@router.get("/callback")
async def auth_callback(request: Request, code: str):
    """
    Handle the OAuth callback from Microsoft
    """
    try:
        # 1. Exchange code for access token
        token_response = requests.post(
            MICROSOFT_CONFIG['token_url'],
            data={
                'client_id': MICROSOFT_CONFIG['client_id'],
                'client_secret': MICROSOFT_CONFIG['client_secret'],
                'code': code,
                'redirect_uri': MICROSOFT_CONFIG['redirect_uri'],
                'grant_type': 'authorization_code'
            }
        )
        token_response.raise_for_status()
        token_info = token_response.json()

        # 2. Get user information using the access token
        user_response = requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers={'Authorization': f'Bearer {token_info["access_token"]}'}
        )
        user_response.raise_for_status()
        user_info = user_response.json()

        # 3. Store user info in session
        request.session['user'] = {
            "email": user_info.get("mail") or user_info.get("userPrincipalName"),
            "name": user_info.get("displayName")
        }
        
        # 4. Redirect to main chat page
        return RedirectResponse(url="/")

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))