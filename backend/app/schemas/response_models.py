from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class DetectedObject(BaseModel):
    label: str
    confidence: float
    bounding_box: dict


class RoomAnalysis(BaseModel):
    room_type: str
    area: Optional[float] = None
    detected_objects: list[DetectedObject]
    segmentation_data: Optional[dict] = None


class RoomResponse(BaseModel):
    id: str
    user_id: str
    image_url: str
    room_type: Optional[str] = None
    area: Optional[float] = None
    detected_objects: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DesignResponse(BaseModel):
    id: str
    room_id: str
    style: Optional[str] = None
    prompt: Optional[str] = None
    generated_image_url: Optional[str] = None
    color_palette: Optional[dict] = None
    furniture_list: Optional[dict] = None
    estimated_cost: Optional[float] = None
    cost_breakdown: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class FurnitureItem(BaseModel):
    id: str
    name: str
    category: str
    style: Optional[str] = None
    price: float
    currency: str = "USD"
    image_url: Optional[str] = None
    model_3d_url: Optional[str] = None
    rating: Optional[float] = None


class FurnitureRecommendation(BaseModel):
    recommendations: list[FurnitureItem]
    total_cost: float
    currency: str = "USD"


class CostBreakdown(BaseModel):
    furniture_cost: float
    decoration_cost: float
    lighting_cost: float
    flooring_cost: float
    labor_cost: float
    total_cost: float
    currency: str = "USD"


class CostEstimationResponse(BaseModel):
    design_id: str
    breakdown: CostBreakdown
    budget_status: str
    savings_suggestions: Optional[list[str]] = None


class ARSceneResponse(BaseModel):
    design_id: str
    scene_objects: list[dict]
    room_anchor: dict
    lighting_config: dict


class AIAssistantResponse(BaseModel):
    message: str
    suggestions: list[str]
    preview_image_url: Optional[str] = None


class HouseRoomDesignResponse(BaseModel):
    id: str
    room_label: str
    room_type: str
    order_index: int
    room_id: Optional[str] = None
    generated_image_url: Optional[str] = None
    room_color_palette: Optional[dict] = None
    furniture_list: Optional[dict] = None
    estimated_cost: Optional[float] = None
    design_notes: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SharedTheme(BaseModel):
    style: str
    primary_colors: list[str]
    accent_colors: list[str]
    materials: list[str]
    lighting: str
    design_principles: list[str]


class HouseProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    style: str
    budget: Optional[float] = None
    currency: str = "USD"
    shared_theme: Optional[SharedTheme] = None
    color_palette: Optional[dict] = None
    material_palette: Optional[dict] = None
    lighting_scheme: Optional[dict] = None
    total_area: Optional[float] = None
    room_count: int
    total_estimated_cost: Optional[float] = None
    cost_breakdown_by_room: Optional[dict] = None
    status: str
    rooms: list[HouseRoomDesignResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HouseProjectSummary(BaseModel):
    id: str
    name: str
    style: str
    room_count: int
    total_estimated_cost: Optional[float] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class HouseCostReport(BaseModel):
    project_id: str
    project_name: str
    style: str
    total_cost: float
    budget: Optional[float] = None
    budget_status: str
    room_costs: list[dict]
    shared_elements_cost: dict
    savings_suggestions: Optional[list[str]] = None
    currency: str = "USD"


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
