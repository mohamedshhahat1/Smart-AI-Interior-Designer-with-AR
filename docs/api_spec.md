# Smart AI Interior Designer - API Specification

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints except `/auth/*` require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Auth Endpoints

### POST /auth/register
Create a new user account.

**Request Body:**
```json
{
  "name": "Mohamed Shahat",
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "Mohamed Shahat",
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2026-06-04T10:00:00Z"
  }
}
```

### POST /auth/login
Authenticate and receive access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):** Same as register response.

---

## Room Endpoints

### POST /room/upload
Upload a room image for AI analysis.

**Request:** Multipart form data with `file` field (JPEG, PNG, WebP, max 20MB)

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "image_url": "/storage/rooms/user_id/image.jpg",
  "room_type": "living_room",
  "area": 22.5,
  "detected_objects": [
    {"label": "sofa", "confidence": 0.95, "bounding_box": {"x1": 10, "y1": 20, "x2": 300, "y2": 200}}
  ],
  "created_at": "2026-06-04T10:00:00Z"
}
```

### GET /room/{room_id}
Get room details by ID.

### GET /room/
List all rooms for the authenticated user.

---

## Design Endpoints

### POST /design/generate
Generate an AI interior design for a room.

**Request Body:**
```json
{
  "room_id": "uuid",
  "style": "scandinavian",
  "prompt": "Design this room in Scandinavian style with a budget of $5000",
  "budget": 5000,
  "preserve_layout": true
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "room_id": "uuid",
  "style": "scandinavian",
  "prompt": "...",
  "generated_image_url": "/storage/designs/uuid.jpg",
  "color_palette": {"primary": "#F5F5DC", "secondary": "#8B7355", "accent": "#4A7C59"},
  "furniture_list": [{"name": "Oak Coffee Table", "price": 280}],
  "estimated_cost": 1980.00,
  "cost_breakdown": {"furniture_cost": 1080, "decoration_cost": 400, "labor_cost": 500},
  "created_at": "2026-06-04T10:00:00Z"
}
```

### POST /design/enhance
Refine an existing design with natural language instructions.

**Request Body:**
```json
{
  "design_id": "uuid",
  "instruction": "Make the room look larger and add more natural lighting"
}
```

### GET /design/{design_id}
Get design details by ID.

---

## Furniture Endpoints

### POST /furniture/recommend
Get furniture recommendations based on room analysis.

**Request Body:**
```json
{
  "room_id": "uuid",
  "style": "modern",
  "budget": 3000
}
```

**Response (200):**
```json
{
  "recommendations": [
    {
      "id": "uuid",
      "name": "Modern Blue Sofa",
      "category": "sofa",
      "style": "modern",
      "price": 650,
      "currency": "USD",
      "image_url": "https://...",
      "model_3d_url": "https://...",
      "rating": 4.5
    }
  ],
  "total_cost": 2150.00,
  "currency": "USD"
}
```

---

## Cost Endpoints

### POST /cost/calculate
Calculate detailed renovation cost estimate.

**Request Body:**
```json
{
  "design_id": "uuid",
  "include_labor": true,
  "include_decoration": true,
  "currency": "USD"
}
```

**Response (200):**
```json
{
  "design_id": "uuid",
  "breakdown": {
    "furniture_cost": 1080.00,
    "decoration_cost": 420.00,
    "lighting_cost": 225.00,
    "flooring_cost": 675.00,
    "labor_cost": 500.00,
    "total_cost": 2900.00,
    "currency": "USD"
  },
  "budget_status": "within_budget",
  "savings_suggestions": null
}
```

---

## Multi-Room House Design Endpoints

### POST /house/project
Create a new multi-room house design project.

**Request Body:**
```json
{
  "name": "My Apartment Redesign",
  "description": "Complete apartment makeover in Scandinavian style",
  "style": "scandinavian",
  "rooms": [
    {"room_label": "Living Room", "room_type": "living_room"},
    {"room_label": "Master Bedroom", "room_type": "bedroom"},
    {"room_label": "Kitchen", "room_type": "kitchen"},
    {"room_label": "Home Office", "room_type": "office"}
  ],
  "budget": 15000,
  "color_preferences": ["white", "light blue", "natural oak"],
  "material_preferences": ["oak wood", "linen", "ceramic"],
  "lighting_preference": "warm ambient lighting"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "My Apartment Redesign",
  "style": "scandinavian",
  "shared_theme": {
    "style": "scandinavian",
    "primary_colors": ["white", "light blue", "natural oak"],
    "accent_colors": ["#A8C5DA", "#7BA38E", "#D4A574"],
    "materials": ["oak wood", "linen", "ceramic"],
    "lighting": "warm ambient lighting",
    "design_principles": ["Emphasize natural light...", "..."]
  },
  "room_count": 4,
  "status": "draft",
  "rooms": [
    {"id": "uuid", "room_label": "Living Room", "room_type": "living_room", "order_index": 0, "status": "pending"},
    {"id": "uuid", "room_label": "Master Bedroom", "room_type": "bedroom", "order_index": 1, "status": "pending"}
  ]
}
```

### POST /house/project/{id}/generate
Generate AI designs for all rooms using the shared theme.

**Request Body:**
```json
{
  "project_id": "uuid",
  "preserve_layout": true,
  "regenerate_rooms": null
}
```

**Response (200):** Full project with all rooms updated to `completed` status, including generated images, per-room costs, and design notes.

### GET /house/projects
List all house projects for the authenticated user.

### GET /house/project/{id}
Get full house project details with all room designs.

### PATCH /house/project/{id}
Update project style, budget, or preferences. Rebuilds shared theme on style change.

### POST /house/room/refine
Refine an individual room design while maintaining house-wide theme context.

**Request Body:**
```json
{
  "room_design_id": "uuid",
  "instruction": "Make this bedroom more cozy while keeping the house theme"
}
```

### GET /house/project/{id}/cost
Get multi-room cost report.

**Response (200):**
```json
{
  "project_id": "uuid",
  "project_name": "My Apartment Redesign",
  "style": "scandinavian",
  "total_cost": 12450.00,
  "budget": 15000,
  "budget_status": "within_budget",
  "room_costs": [
    {"room_label": "Living Room", "room_type": "living_room", "estimated_cost": 4200.00},
    {"room_label": "Master Bedroom", "room_type": "bedroom", "estimated_cost": 3100.00},
    {"room_label": "Kitchen", "room_type": "kitchen", "estimated_cost": 3800.00},
    {"room_label": "Home Office", "room_type": "office", "estimated_cost": 1350.00}
  ],
  "shared_elements_cost": {
    "flooring_transitions": 600.00,
    "consistent_paint": 800.00,
    "lighting_fixtures": 480.00,
    "total": 1880.00
  },
  "savings_suggestions": null
}
```

### DELETE /house/project/{id}
Delete a house project and all associated room designs.

---

## Smart Lighting & Mood Detection Endpoints

### POST /lighting/detect-mood
Detect user mood and generate a lighting recommendation.

**Request Body:**
```json
{
  "text_input": "I want to relax after a long day",
  "time_of_day": "evening",
  "activity": "relaxing",
  "energy_level": 0.25,
  "room_type": "living_room"
}
```

**Response (200):**
```json
{
  "mood_analysis": {
    "detected_mood": "relaxed",
    "confidence": 0.87,
    "energy_level": 0.25,
    "warmth_score": 0.75,
    "suggested_moods": ["cozy", "sleepy", "melancholic"],
    "analysis_source": "text+activity+time+energy"
  },
  "lighting_recommendation": {
    "color_temperature": 2700,
    "brightness": 0.40,
    "color_hex": "#FFD699",
    "saturation": 0.15,
    "description": "Warm, dimmed lighting that creates a peaceful sanctuary",
    "mood": "relaxed",
    "time_of_day": "evening",
    "fixtures": [
      {"name": "Floor Lamp", "type": "ambient", "brightness": 0.35, "color_temperature": 2700, "position": "corner"},
      {"name": "Table Lamp", "type": "accent", "brightness": 0.30, "color_temperature": 2700, "position": "side_table"}
    ],
    "zones": [
      {"zone_name": "Primary Seating", "brightness": 0.40, "purpose": "Main relaxation area"},
      {"zone_name": "Perimeter", "brightness": 0.15, "purpose": "Ambient glow around room edges"}
    ],
    "transition_duration": 2.0,
    "ambiance_notes": "Soft golden glow with gentle shadows..."
  },
  "alternative_scenes": [
    {"mood": "cozy", "color_temperature": 2500, "brightness": 0.35, "description": "Warm amber hygge lighting..."}
  ],
  "circadian_note": null
}
```

### POST /lighting/scenes
Save a lighting scene.

### GET /lighting/scenes
List saved scenes (optional `?mood=relaxed` filter).

### PATCH /lighting/scenes/{id}
Update scene parameters (color temp, brightness, favorite status).

### POST /lighting/circadian
Generate a 24-hour circadian rhythm schedule.

**Request Body:**
```json
{
  "wake_time": "07:00",
  "sleep_time": "23:00",
  "work_hours": ["09:00", "17:00"]
}
```

**Response (200):**
```json
{
  "schedule": [
    {"time": "06:30", "phase": "dawn", "color_temp": 2200, "brightness": 0.15, "mood": "sleepy", "label": "Gentle Wake"},
    {"time": "07:00", "phase": "sunrise", "color_temp": 3000, "brightness": 0.45, "mood": "refreshed", "label": "Sunrise Simulation"},
    {"time": "09:00", "phase": "work_start", "color_temp": 5000, "brightness": 0.85, "mood": "focused", "label": "Work Mode"}
  ],
  "wake_time": "07:00",
  "sleep_time": "23:00",
  "total_transitions": 13,
  "energy_savings_estimate": "Moderate savings (~20-30%)"
}
```

### POST /lighting/export
Export scene to smart home platform.

**Request Body:**
```json
{
  "scene_id": "uuid",
  "platform": "philips_hue"
}
```

**Response:** Platform-specific configuration with setup instructions and compatible devices list.

### POST /lighting/feedback
Submit scene feedback (rating 1-5) for ML improvement.

### GET /lighting/insights
Get personalized lighting usage analytics (mood distribution, averages, recommendations).

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

| Status Code | Description |
|------------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Email already registered |
| 413 | Payload Too Large - Image exceeds size limit |
| 500 | Internal Server Error |
