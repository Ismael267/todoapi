from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional, Dict
from core.settings import settings
from db.database import get_db
from sqlalchemy.orm import Session
from models.User import User
from core.security import create_access_token,generate_password


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
            response = await client.post(access_token_url, headers={"Accept": "application/json"})        
            response.raise_for_status() 
            data = response.json()
            
            access_token = data.get('access_token')  
            if access_token:
                return access_token
            else:
                raise HTTPException(status_code=400, detail="Failed to retrieve access token")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch access token: {str(e)}")

from typing import Optional, Dict
import httpx
from fastapi import HTTPException

async def get_user_info(access_token: str) -> Optional[Dict]:
    user_info_url = "https://api.github.com/user"
    user_email_url = "https://api.github.com/user/emails"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(user_info_url, headers=headers)
            user_response.raise_for_status() 
            user_info = user_response.json()

            
            email_response = await client.get(user_email_url, headers=headers)
            email_response.raise_for_status()
            user_email_info = email_response.json()
            
           
            user_info['email'] = user_email_info[0].get("email") if user_email_info else None
            
            return user_info
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch user info: {str(e)}")


@router.get("/github/login")
async def login_with_github():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={GITHUB_APP_ID}&redirect_uri={GITHUB_REDIRECT_URI}"
    )
    return RedirectResponse(url=github_auth_url)

@router.get("/auth/github/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):

    access_token = await get_access_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_data = await get_user_info(access_token)
    
    if not user_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")
    # return user_data
    gh_user = db.query(User).filter(User.email == user_data["email"]).first()

    if gh_user:
        token = create_access_token(user_data["login"])
    else:
        new_user = User(
            username=user_data["login"],
            email=user_data["email"],
            hashed_password=generate_password()
        )
        db.add(new_user)
        db.commit()
        token = create_access_token(user_data["login"])

    return {"token": token, "token_type": "bearer"}
