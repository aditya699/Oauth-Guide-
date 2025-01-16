'''
Author: Aditya Bhatt 
Date: 15-01-2025 11:00 AM

NOTE:
1.Basic or bare minimum config for Microsoft OAuth

'''
from dotenv import load_dotenv
import os
load_dotenv()

MICROSOFT_CONFIG = {
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET'),
    'tenant_id': os.getenv('TENANT_ID'),
    'redirect_uri': os.getenv('REDIRECT_URI'),

    #OAuth Endpoints
    'authorize_endpoint':f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/authorize",
     "token_url": f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token",
    
    # Basic scopes we need
    "scopes": ["openid", "profile", "email"]

    #Openid is like userid
    #Profile is like user name
    #Email is like user email

}

