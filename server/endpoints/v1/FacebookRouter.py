from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional, Dict
from core.settings import settings

router = APIRouter(tags=["Auth/Facebook"])

FACEBOOK_APP_ID = settings.FACEBOOK_APP_ID
FACEBOOK_APP_SECRET =settings.FACEBOOK_APP_SECRET
FACEBOOK_REDIRECT_URI =settings.FACEBOOK_REDIRECT_URI
FACEBOOK_API_VERSION = "v12.0"

async def get_access_token(code: str) -> Optional[str]:
    access_token_url = (
        f"https://graph.facebook.com/{FACEBOOK_API_VERSION}/oauth/access_token"
        f"?client_id={FACEBOOK_APP_ID}&redirect_uri={FACEBOOK_REDIRECT_URI}"
        f"&client_secret={FACEBOOK_APP_SECRET}&code={code}"
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(access_token_url)
            response.raise_for_status()  # Raise HTTP errors if they occur
            data = response.json()
            return data.get("access_token")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500)

async def get_user_info(access_token: str) -> Optional[Dict]:
    user_info_url = f"https://graph.facebook.com/{FACEBOOK_API_VERSION}/me?fields=id,name,email&access_token={access_token}"
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(user_info_url)
            user_response.raise_for_status()  # Raise HTTP errors if they occur
            return user_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500)

@router.get("/facebook/login")
async def login_with_facebook():
    facebook_auth_url = (
        f"https://www.facebook.com/{FACEBOOK_API_VERSION}/dialog/oauth?"
        f"client_id={FACEBOOK_APP_ID}&redirect_uri={FACEBOOK_REDIRECT_URI}&scope=email"
    )
    return RedirectResponse(url=facebook_auth_url)

@router.get("/auth/facebook/callback")
async def Auth_callback(code: str):
    access_token = await get_access_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_data = await get_user_info(access_token)
    if not user_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    return user_data