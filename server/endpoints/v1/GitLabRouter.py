from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import httpx
from typing import Optional, Dict
from core.settings import settings
from db.database import get_db
from sqlalchemy.orm import Session
from models.User import User
from core.security import create_access_token,generate_password


router = APIRouter(tags=["Auth/GitLab"])

GITLAB_APP_ID = settings.GITLAB_APP_ID
GITLAB_APP_SECRET = settings.GITLAB_APP_SECRET
GITLAB_REDIRECT_URI = settings.GITLAB_REDIRECT_URI

async def get_access_token(code: str) -> Optional[str]:
    access_token_url = (
        f"https://gitlab.com/oauth/token?"
        f"client_id={GITLAB_APP_ID}&redirect_uri={GITLAB_REDIRECT_URI}"
        f"&client_secret={GITLAB_APP_SECRET}&code={code}&grant_type=authorization_code"
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(access_token_url)
            response.raise_for_status()
            data = response.json()
            return data.get("access_token")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Failed to retrieve access token")

async def get_user_info(access_token: str) -> Optional[Dict]:
    user_info_url = "https://gitlab.com/api/v4/user"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(user_info_url, headers=headers)
            user_response.raise_for_status()
            return user_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Failed to retrieve user info")

@router.get("/gitlab/login")
async def login_with_gitlab():
    gitlab_auth_url = (
        f"https://gitlab.com/oauth/authorize?"
        f"client_id={GITLAB_APP_ID}&redirect_uri={GITLAB_REDIRECT_URI}&response_type=code"
        f"&scope=read_user"
    )
    return RedirectResponse(url=gitlab_auth_url)

@router.get("/auth/gitlab/callback")
async def auth_callback(code: str,db: Session = Depends(get_db)):
    access_token = await get_access_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_data = await get_user_info(access_token)
    if not user_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    # return user_data
    lk_user=db.query(User).filter(User.email==user_data["email"]).first()
    
    
    if not lk_user:

        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=generate_password()
        )
        db.add(new_user)
        db.commit()
        token = create_access_token(lk_user.email)

    response_model=JSONResponse(content={
        "token":token,
        "token_type":"Bearer",
        "user":jsonable_encoder(new_user,exclude={
            "hashed_password"
        })
    })
    return response_model
