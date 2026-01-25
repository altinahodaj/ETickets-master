from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    username: str | None = Field(default=None, min_length=3, max_length=50)


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str | None
    is_admin: bool = Field(False, alias="isAdmin")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "Bearer"
