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


# --- Smart Lighting & Mood Detection ---

class MoodDetectRequest(BaseModel):
    text_input: Optional[str] = Field(
        None, max_length=500,
        examples=["I want to relax after a long day", "Hosting a dinner party tonight"],
    )
    time_of_day: Optional[str] = Field(None, examples=["morning", "afternoon", "evening", "night"])
    activity: Optional[str] = Field(
        None, examples=["relaxing", "working", "entertaining", "sleeping", "cooking", "reading"],
    )
    energy_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    room_type: Optional[str] = None
    room_id: Optional[str] = None
    design_id: Optional[str] = None


class LightingSceneCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    mood: str = Field(..., min_length=2, max_length=50)
    room_id: Optional[str] = None
    design_id: Optional[str] = None
    time_of_day: Optional[str] = None
    activity: Optional[str] = None
    color_temperature: int = Field(..., ge=1800, le=6500)
    brightness: float = Field(..., ge=0.0, le=1.0)
    color_hex: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    saturation: float = Field(default=0.0, ge=0.0, le=1.0)
    fixtures: Optional[list[dict]] = None
    zones: Optional[list[dict]] = None
    transition_duration: float = Field(default=2.0, ge=0.0, le=30.0)


class LightingSceneUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color_temperature: Optional[int] = Field(None, ge=1800, le=6500)
    brightness: Optional[float] = Field(None, ge=0.0, le=1.0)
    color_hex: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    saturation: Optional[float] = Field(None, ge=0.0, le=1.0)
    transition_duration: Optional[float] = Field(None, ge=0.0, le=30.0)
    is_favorite: Optional[bool] = None


class CircadianScheduleRequest(BaseModel):
    room_id: Optional[str] = None
    wake_time: str = Field(default="07:00", pattern=r"^\d{2}:\d{2}$")
    sleep_time: str = Field(default="23:00", pattern=r"^\d{2}:\d{2}$")
    work_hours: Optional[list[str]] = Field(None, examples=[["09:00", "17:00"]])
    preferences: Optional[dict] = None


class MoodProfileCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    mood_type: str = Field(..., examples=["relaxed", "focused", "energetic", "romantic", "cozy"])
    energy_level: float = Field(default=0.5, ge=0.0, le=1.0)
    warmth_preference: float = Field(default=0.5, ge=0.0, le=1.0)
    brightness_preference: float = Field(default=0.5, ge=0.0, le=1.0)
    preferred_colors: Optional[list[str]] = None
    preferred_activities: Optional[list[str]] = None


class LightingFeedbackRequest(BaseModel):
    scene_id: str
    mood: str
    rating: int = Field(..., ge=1, le=5)
    duration_minutes: Optional[float] = Field(None, ge=0)


class SmartHomeExportRequest(BaseModel):
    scene_id: str
    platform: str = Field(..., examples=["philips_hue", "lifx", "homekit", "google_home", "alexa"])


# --- Feng Shui Analysis ---

class FengShuiAnalyzeRequest(BaseModel):
    room_id: Optional[str] = None
    design_id: Optional[str] = None
    room_type: str = Field(..., examples=["living_room", "bedroom", "office", "kitchen"])
    compass_direction: Optional[str] = Field(
        None, examples=["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
    )
    detected_objects: Optional[list[dict]] = None
    room_dimensions: Optional[dict] = None
    birth_year: Optional[int] = Field(None, ge=1920, le=2026)
    include_bagua: bool = Field(default=True)
    include_element_analysis: bool = Field(default=True)


class FengShuiApplyCureRequest(BaseModel):
    analysis_id: str
    cure_id: str


class FengShuiRedesignRequest(BaseModel):
    analysis_id: str
    room_id: Optional[str] = None
    design_id: Optional[str] = None
    apply_cures: list[str] = Field(
        default_factory=list, description="Cure IDs to apply in the redesign"
    )
    budget: Optional[float] = Field(None, ge=0)
    preserve_existing: bool = Field(default=True)


class FengShuiCompatibilityRequest(BaseModel):
    birth_year: int = Field(..., ge=1920, le=2026)
    room_type: str
    compass_direction: Optional[str] = None


# --- Seasonal & Holiday Themes ---

class SeasonalThemeGenerateRequest(BaseModel):
    theme_type: str = Field(..., examples=["season", "holiday"])
    season: Optional[str] = Field(None, examples=["spring", "summer", "autumn", "winter"])
    holiday: Optional[str] = Field(
        None, examples=[
            "christmas", "halloween", "easter", "valentines", "thanksgiving",
            "eid", "diwali", "lunar_new_year", "hanukkah", "ramadan",
            "new_year", "independence_day", "mothers_day",
        ],
    )
    room_type: str = Field(default="living_room")
    room_id: Optional[str] = None
    design_id: Optional[str] = None
    budget_tier: str = Field(default="medium", examples=["budget", "medium", "premium"])
    base_style: Optional[str] = Field(None, examples=["scandinavian", "modern", "traditional"])
    intensity: float = Field(default=0.7, ge=0.0, le=1.0, description="0=subtle hints, 1=full transformation")
    include_diy: bool = Field(default=True)
    include_scents: bool = Field(default=True)


class SeasonalTransitionRequest(BaseModel):
    from_theme_id: Optional[str] = None
    to_season: Optional[str] = None
    to_holiday: Optional[str] = None
    room_type: str = Field(default="living_room")
    gradual: bool = Field(default=True, description="Gradual transition vs complete swap")


class AutoSeasonDetectRequest(BaseModel):
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    hemisphere: str = Field(default="northern", examples=["northern", "southern"])
    include_upcoming_holidays: bool = Field(default=True)
    days_ahead: int = Field(default=30, ge=0, le=90)
