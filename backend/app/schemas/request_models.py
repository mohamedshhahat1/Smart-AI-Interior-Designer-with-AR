from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RoomUploadRequest(BaseModel):
    room_type: Optional[str] = None


class DesignGenerateRequest(BaseModel):
    room_id: str
    style: str = Field(..., min_length=2, max_length=50)
    prompt: Optional[str] = Field(
        None,
        max_length=1000,
        examples=["Design this room in Scandinavian style with a budget of $5000"],
    )
    budget: Optional[float] = Field(None, ge=0)
    preserve_layout: bool = Field(default=True)


class DesignEnhanceRequest(BaseModel):
    design_id: str
    instruction: str = Field(
        ...,
        max_length=500,
        examples=["Make the room look larger", "Add more natural lighting"],
    )


class FurnitureRecommendRequest(BaseModel):
    room_id: str
    design_id: Optional[str] = None
    categories: Optional[list[str]] = None
    budget: Optional[float] = Field(None, ge=0)
    style: Optional[str] = None


class CostCalculateRequest(BaseModel):
    design_id: str
    include_labor: bool = Field(default=True)
    include_decoration: bool = Field(default=True)
    currency: str = Field(default="USD", max_length=3)


class ARSceneRequest(BaseModel):
    design_id: str
    room_dimensions: Optional[dict] = None


class AIAssistantRequest(BaseModel):
    room_id: str
    message: str = Field(..., max_length=1000)
    conversation_history: Optional[list[dict]] = None


class RoomEntry(BaseModel):
    room_label: str = Field(..., min_length=1, max_length=100, examples=["Master Bedroom"])
    room_type: str = Field(..., min_length=2, max_length=50, examples=["bedroom"])
    room_id: Optional[str] = Field(None, description="Existing room ID if already scanned")


class HouseProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=200, examples=["My Apartment Redesign"])
    description: Optional[str] = Field(None, max_length=1000)
    style: str = Field(..., min_length=2, max_length=50, examples=["scandinavian"])
    rooms: list[RoomEntry] = Field(..., min_length=1, max_length=20)
    budget: Optional[float] = Field(None, ge=0)
    currency: str = Field(default="USD", max_length=3)
    color_preferences: Optional[list[str]] = Field(
        None, examples=[["white", "light blue", "natural oak"]]
    )
    material_preferences: Optional[list[str]] = Field(
        None, examples=[["oak wood", "linen", "ceramic"]]
    )
    lighting_preference: Optional[str] = Field(
        None, max_length=100, examples=["warm ambient lighting"]
    )


class HouseProjectGenerateRequest(BaseModel):
    project_id: str
    regenerate_rooms: Optional[list[str]] = Field(
        None, description="Room IDs to regenerate; omit to generate all pending"
    )
    preserve_layout: bool = Field(default=True)


class HouseProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    style: Optional[str] = Field(None, min_length=2, max_length=50)
    budget: Optional[float] = Field(None, ge=0)
    color_preferences: Optional[list[str]] = None
    lighting_preference: Optional[str] = None


class HouseRoomUpdateRequest(BaseModel):
    room_design_id: str
    instruction: str = Field(
        ..., max_length=500,
        examples=["Make this bedroom more cozy while keeping the house theme"]
    )
