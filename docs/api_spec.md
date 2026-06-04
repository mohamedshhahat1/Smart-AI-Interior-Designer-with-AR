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
