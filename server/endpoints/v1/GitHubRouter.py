from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional, Dict
from core.settings import settings

router = APIRouter(tags=["Auth/GitHub"])

GITHUB_APP_ID = settings.GITHUB_APP_ID
GITHUB_APP_SECRET = settings.GITHUB_APP_SECRET
GITHUB_REDIRECT_URI = settings.GITHUB_REDIRECT_URI

async def get_access_token(code: str) -> Optional[str]:
    access_token_url = (
        f"https://github.com/login/oauth/access_token?"
        f"client_id={GITHUB_APP_ID}&client_secret={GITHUB_APP_SECRET}&code={code}&redirect_uri={GITHUB_REDIRECT_URI}"
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(access_token_url,headers={ "Accept":"application/json"})        
            response.raise_for_status() 
            data = response.json()
            
            access_token = data.get('access_token')  
            if access_token:
                return access_token
            else:
                raise HTTPException(status_code=400, detail="Failed to retrieve access token")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch access token: {str(e)}")

async def get_user_info(access_token: str) -> Optional[Dict]:
    user_info_url = f"https://api.github.com/user"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(user_info_url, headers=headers)
            user_response.raise_for_status() 
            return user_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch user info: {str(e)}")

@router.get("/github/login")
async def login_with_github():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={GITHUB_APP_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email"
    )
    return RedirectResponse(url=github_auth_url)

@router.get("/auth/github/callback")
async def auth_callback(code: str):
    
    access_token = await get_access_token(code)
    print(access_token)
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_data = await get_user_info(access_token)
    if not user_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    return user_data
