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
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
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


# --- Smart Lighting & Mood Detection ---

class LightingFixture(BaseModel):
    name: str
    type: str
    brightness: float
    color_temperature: int
    color_hex: Optional[str] = None
    position: Optional[str] = None


class LightingZone(BaseModel):
    zone_name: str
    fixtures: list[LightingFixture]
    brightness: float
    purpose: str


class MoodAnalysis(BaseModel):
    detected_mood: str
    confidence: float
    energy_level: float
    warmth_score: float
    suggested_moods: list[str]
    analysis_source: str


class LightingRecommendation(BaseModel):
    color_temperature: int
    brightness: float
    color_hex: Optional[str] = None
    saturation: float
    description: str
    mood: str
    time_of_day: str
    fixtures: list[LightingFixture]
    zones: list[LightingZone]
    transition_duration: float
    ambiance_notes: str


class MoodDetectResponse(BaseModel):
    mood_analysis: MoodAnalysis
    lighting_recommendation: LightingRecommendation
    alternative_scenes: list[dict]
    circadian_note: Optional[str] = None


class LightingSceneResponse(BaseModel):
    id: str
    name: str
    mood: str
    time_of_day: Optional[str] = None
    activity: Optional[str] = None
    color_temperature: int
    brightness: float
    color_hex: Optional[str] = None
    saturation: float
    fixtures: Optional[list[dict]] = None
    zones: Optional[list[dict]] = None
    transition_duration: float
    is_circadian: bool
    is_favorite: bool
    usage_count: int
    room_id: Optional[str] = None
    design_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CircadianScheduleResponse(BaseModel):
    schedule: list[dict]
    wake_time: str
    sleep_time: str
    total_transitions: int
    energy_savings_estimate: Optional[str] = None


class MoodProfileResponse(BaseModel):
    id: str
    name: str
    mood_type: str
    energy_level: float
    warmth_preference: float
    brightness_preference: float
    preferred_colors: Optional[list[str]] = None
    preferred_activities: Optional[list[str]] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SmartHomeExportResponse(BaseModel):
    platform: str
    config: dict
    instructions: list[str]
    compatible_devices: list[str]


class LightingInsightsResponse(BaseModel):
    total_scenes: int
    most_used_mood: Optional[str] = None
    average_brightness: Optional[float] = None
    average_color_temperature: Optional[int] = None
    peak_usage_time: Optional[str] = None
    mood_distribution: dict
    recommendations: list[str]


# --- Feng Shui Analysis ---

class BaguaZone(BaseModel):
    zone: str
    direction: str
    element: str
    life_area: str
    colors: list[str]
    status: str
    score: float
    enhancement: Optional[str] = None


class ElementBalance(BaseModel):
    element: str
    current_level: float
    ideal_level: float
    status: str
    associated_colors: list[str]
    associated_shapes: list[str]
    enhancement_items: list[str]


class ChiFlowIssue(BaseModel):
    issue_type: str
    severity: str
    location: str
    description: str
    impact: str


class FengShuiCureResponse(BaseModel):
    id: str
    category: str
    severity: str
    issue_description: str
    cure_description: str
    element: Optional[str] = None
    placement: Optional[str] = None
    estimated_cost: Optional[float] = None
    priority: int
    is_applied: bool

    class Config:
        from_attributes = True


class FurniturePlacementAdvice(BaseModel):
    item: str
    current_position: Optional[str] = None
    recommended_position: str
    reason: str
    commanding_position: bool


class FengShuiAnalysisResponse(BaseModel):
    id: str
    room_type: str
    compass_direction: Optional[str] = None
    overall_score: float
    chi_flow_score: float
    element_balance_score: float
    yin_yang_score: float
    clutter_score: float
    commanding_position_score: float
    score_interpretation: str
    bagua_map: Optional[list[BaguaZone]] = None
    element_analysis: Optional[list[ElementBalance]] = None
    chi_flow_issues: Optional[list[ChiFlowIssue]] = None
    cures: list[FengShuiCureResponse]
    furniture_placement: Optional[list[FurniturePlacementAdvice]] = None
    color_recommendations: Optional[dict] = None
    lucky_directions: Optional[dict] = None
    birth_element: Optional[str] = None
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True


class FengShuiCompatibilityResponse(BaseModel):
    birth_year: int
    kua_number: int
    birth_element: str
    lucky_directions: list[str]
    unlucky_directions: list[str]
    compatible_colors: list[str]
    compatible_elements: list[str]
    room_recommendations: dict


# --- Seasonal & Holiday Themes ---

class DecorItem(BaseModel):
    name: str
    category: str
    placement: str
    estimated_cost: Optional[float] = None
    reusable: bool = True
    diy_possible: bool = False


class DIYProject(BaseModel):
    name: str
    difficulty: str
    time_minutes: int
    materials: list[str]
    instructions: str
    estimated_cost: float


class ScentRecommendation(BaseModel):
    scent: str
    method: str
    placement: str
    intensity: str


class SeasonalThemeResponse(BaseModel):
    id: str
    theme_type: str
    season: Optional[str] = None
    holiday: Optional[str] = None
    name: str
    description: Optional[str] = None
    color_palette: Optional[dict] = None
    textures: Optional[list[str]] = None
    materials: Optional[list[str]] = None
    lighting_mood: Optional[str] = None
    decor_items: Optional[list[DecorItem]] = None
    diy_projects: Optional[list[DIYProject]] = None
    scent_recommendations: Optional[list[ScentRecommendation]] = None
    music_playlist_mood: Optional[str] = None
    generated_image_url: Optional[str] = None
    budget_tier: str
    estimated_cost: Optional[float] = None
    reusability_score: Optional[float] = None
    transition_from: Optional[str] = None
    transition_tips: Optional[list[str]] = None
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SeasonDetectResponse(BaseModel):
    current_season: str
    hemisphere: str
    days_into_season: int
    days_until_next_season: int
    next_season: str
    upcoming_holidays: list[dict]
    recommended_theme: str
    seasonal_mood: str


class SeasonalTransitionResponse(BaseModel):
    from_theme: Optional[str] = None
    to_theme: str
    transition_steps: list[dict]
    items_to_keep: list[str]
    items_to_add: list[str]
    items_to_remove: list[str]
    estimated_effort: str
    estimated_cost: float


# --- Pet-Friendly Design ---

class PetProfileResponse(BaseModel):
    id: str
    name: str
    species: str
    breed: Optional[str] = None
    size: str
    age_years: Optional[float] = None
    weight_kg: Optional[float] = None
    energy_level: str
    is_indoor: bool
    is_destructive: bool
    sheds_fur: bool
    climbs_furniture: bool
    has_allergies: bool
    special_needs: Optional[list[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PetHazard(BaseModel):
    hazard_type: str
    severity: str
    item: str
    description: str
    solution: str
    estimated_cost: Optional[float] = None


class PetZone(BaseModel):
    zone_name: str
    zone_type: str
    location: str
    description: str
    items_needed: list[str]
    estimated_cost: float


class PetMaterialRecommendation(BaseModel):
    category: str
    recommended: str
    avoid: str
    reason: str


class PetProductRecommendation(BaseModel):
    name: str
    category: str
    for_pet_type: str
    description: str
    price_range: str
    priority: str


class PetFriendlyAnalysisResponse(BaseModel):
    id: str
    room_type: str
    overall_score: float
    safety_score: float
    comfort_score: float
    durability_score: float
    cleanliness_score: float
    score_interpretation: str
    hazards: list[PetHazard]
    zone_plan: list[PetZone]
    material_recommendations: list[PetMaterialRecommendation]
    plant_safety: Optional[dict] = None
    cleaning_tips: list[str]
    product_recommendations: Optional[list[PetProductRecommendation]] = None
    estimated_cost: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- 3D Walkthrough / Room Generation ---

class Furniture3DObject(BaseModel):
    object_id: str
    name: str
    category: str
    model_url: Optional[str] = None
    position: dict
    rotation: dict
    scale: dict
    material: Optional[str] = None
    interactable: bool = True


class LightSource3D(BaseModel):
    light_id: str
    light_type: str
    position: dict
    color: str
    intensity: float
    cast_shadows: bool = True


class CameraPosition(BaseModel):
    position_id: str
    label: str
    position: dict
    look_at: dict
    fov: float = 60.0


class WalkthroughPathPoint(BaseModel):
    index: int
    position: dict
    look_at: dict
    duration_seconds: float
    easing: str = "ease_in_out"


class Room3DModelResponse(BaseModel):
    id: str
    name: str
    room_type: str
    status: str
    reconstruction_method: str
    quality_level: str
    dimensions: Optional[dict] = None
    room_geometry: Optional[dict] = None
    depth_map_url: Optional[str] = None
    mesh_url: Optional[str] = None
    glb_model_url: Optional[str] = None
    usdz_model_url: Optional[str] = None
    furniture_objects: Optional[list[Furniture3DObject]] = None
    lighting_setup: Optional[list[LightSource3D]] = None
    camera_positions: Optional[list[CameraPosition]] = None
    walkthrough_path: Optional[list[WalkthroughPathPoint]] = None
    polygon_count: Optional[int] = None
    file_size_mb: Optional[float] = None
    processing_time_seconds: Optional[float] = None
    view_count: int = 0
    room_id: Optional[str] = None
    design_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WalkthroughSessionResponse(BaseModel):
    id: str
    model_id: str
    comparison_model_id: Optional[str] = None
    duration_seconds: Optional[float] = None
    screenshots_taken: int = 0
    started_at: datetime
    ended_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Room3DSummary(BaseModel):
    id: str
    name: str
    room_type: str
    status: str
    quality_level: str
    glb_model_url: Optional[str] = None
    polygon_count: Optional[int] = None
    view_count: int = 0
    created_at: datetime


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
