from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional, Dict
from core.settings import settings
from db.database import get_db
from sqlalchemy.orm import Session
from models.User import User
from core.security import create_access_token,generate_password

router = APIRouter(tags=["Auth/LinkedIn"])

LINKEDIN_CLIENT_ID = settings.LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET = settings.LINKEDIN_CLIENT_SECRET
LINKEDIN_REDIRECT_URI = settings.LINKEDIN_REDIRECT_URI

async def get_access_token(code: str) -> Optional[str]:
    access_token_url = (
        f"https://www.linkedin.com/oauth/v2/accessToken?"
        f"grant_type=authorization_code&code={code}&client_id={LINKEDIN_CLIENT_ID}"
        f"&client_secret={LINKEDIN_CLIENT_SECRET}&redirect_uri={LINKEDIN_REDIRECT_URI}"
    )
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(access_token_url)
            response.raise_for_status()  # Raise HTTP errors if they occur
            data = response.json()
            # print(data)
            # return {
            #     "access_token": data["access_token"],
            #      "id_token"  : data["id_token"]
            # }
            # print(data)
            return data.get("access_token")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Failed to retrieve access token")

async def get_user_info(access_token: str ) -> Optional[Dict]:
    # mettre userinfo !!!!important
    user_info_url = f"https://api.linkedin.com/v2/userinfo"  
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        try:
            user_response = await client.get(user_info_url, headers=headers,follow_redirects=True)
            user_response.raise_for_status()  
            return user_response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail="Failed to retrieve user info")

@router.get("/linkedin/login")
async def login_with_linkedin():
    linkedin_auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={LINKEDIN_CLIENT_ID}&redirect_uri={LINKEDIN_REDIRECT_URI}"
        f"&scope=profile,email,openid,w_member_social"  
    )
    return RedirectResponse(url=linkedin_auth_url)

@router.get("/auth/linkedin/callback") 
async def auth_callback(code: str,db: Session = Depends(get_db)):
    access_token = await get_access_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_data = await get_user_info(access_token)
    if not user_data:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    # return user_data
    lk_user=db.query(User).filter(User.email==user_data["email"]).first()
    if lk_user:
        token = create_access_token(user_data["name"])
    else:
        new_user = User(
            username=user_data["name"],
            email=user_data["email"],
            hashed_password=generate_password()
        )
        db.add(new_user)
        db.commit()
        token = create_access_token(user_data["email"])

    return {"token": token, "token_type": "bearer"}
