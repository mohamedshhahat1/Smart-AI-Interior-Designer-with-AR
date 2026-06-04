# Smart AI Interior Designer with AR

AI-Powered Room Redesign with Augmented Reality Visualization, Furniture Recommendation, and Cost Estimation.

## Problem Statement

Interior design services are expensive, time-consuming, and often require multiple consultations. Most existing AI design tools only generate images and do not help users visualize furniture in their real rooms or estimate implementation costs.

## Solution

A mobile application that:

- **Scans a room** using a smartphone camera
- **Analyzes** the room layout and existing furniture
- **Generates** multiple AI-powered interior design concepts
- **Places virtual furniture** using Augmented Reality (AR)
- **Recommends** real furniture products from catalogs
- **Calculates** estimated renovation costs
- **Allows redesign** through natural language commands
- **Designs entire homes** with unified multi-room themes

## Core Features

| Feature | Description | Technologies |
|---------|------------|--------------|
| Room Scanning | Detect room dimensions, walls, floor, windows, doors | ARCore, ARKit, Depth Estimation |
| Room Understanding | Identify furniture objects (sofa, chair, bed, desk, etc.) | YOLOv11, Segment Anything (SAM) |
| AI Interior Generation | Generate design concepts from text prompts | Stable Diffusion XL, ControlNet, FLUX |
| AR Visualization | Overlay redesigned furniture in real-time camera view | ARCore, ARKit |
| Furniture Recommendation | Match detected needs with real product catalogs | Custom recommendation engine |
| Cost Estimation | Calculate furniture, decoration, and labor costs | Budget optimization engine |
| AI Design Assistant | Natural language commands for room redesign | OpenAI API / Google Gemini |
| **Multi-Room House Design** | **Redesign entire homes with unified themes** | **Theme Unifier, Consistency Engine** |
| **Smart Lighting & Mood** | **AI-powered lighting that adapts to mood and circadian rhythm** | **Mood Analyzer, Scene Generator, Circadian Engine** |
| **Feng Shui Analysis** | **AI-powered room harmony scoring with Five Elements and Bagua** | **Bagua Mapper, Element Analyzer, Chi Flow, Cure Recommender** |
| **Seasonal & Holiday Themes** | **Transform rooms for every season and celebration with decor, DIY, scents** | **Season Detector, Theme Generator, Transition Planner** |
| **Pet-Friendly Design** | **Safety audit, zone planning, and product recommendations for pet owners** | **Safety Analyzer, Zone Planner, Product Recommender** |
| **3D Walkthrough** | **Interactive 3D room exploration with walkthrough navigation** | **Depth Estimator, Mesh Generator, Scene Builder, NeRF/Gaussian Splatting** |

## 3D Walkthrough / 3D Room Generation

Transform room designs from static 2D images into fully interactive 3D environments that users can explore in real time.

### Pipeline

```
Room Image → Depth Estimation (MiDaS) → Point Cloud
           → Room Geometry (walls, floor, ceiling)
           → Furniture Placement (15 item catalog with GLB models)
           → Lighting Setup (ambient + point + directional)
           → Camera Positions (6 preset views)
           → Walkthrough Path (7-point tour / 12-step orbit / furniture focus)
           → GLB/USDZ Export
```

### Reconstruction Methods

| Method | Speed | Quality | Input Required |
|--------|-------|---------|---------------|
| Depth Estimation | Fast | Good | Single image |
| NeRF | Slow | Excellent | Multiple images |
| Gaussian Splatting | Medium | Excellent | Multiple images |
| Multi-View Stereo | Medium | Good | Image pairs |

### Quality Levels

| Level | Polygons | Texture | Shadows | Est. Time |
|-------|----------|---------|---------|-----------|
| Draft | ~5K | 512px | None | ~2s |
| Standard | ~15K | 1024px | Basic | ~8s |
| High | ~25K | 2048px | Soft | ~20s |
| Ultra | ~45K | 4096px | Ray-traced | ~60s |

### Features

- **3D Room Reconstruction** — Walls, floor, ceiling mesh from depth estimation
- **Furniture Placement** — 15-item 3D catalog with automatic smart positioning
- **Dynamic Lighting** — Ambient, ceiling, window, and lamp-based light sources
- **6 Camera Presets** — Overview, entrance, center, left/right corners, low angle
- **3 Walkthrough Modes** — Room tour, orbit, and furniture-focus paths with easing curves
- **Design Comparison** — Side-by-side walkthrough of two design versions
- **Session Tracking** — Record camera paths, screenshots, and annotations
- **GLB + USDZ Export** — Industry-standard 3D formats for web and iOS AR

## AI-Powered Pet-Friendly Room Design

Design rooms that are safe, comfortable, and stylish for both you and your pets. The system analyzes your room for hazards, creates dedicated pet zones, recommends durable materials, and suggests the best pet products.

### Supported Pets

Dog, Cat, Bird, Rabbit (with species-specific safety rules, zones, materials, and products)

### Analysis Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Safety | 35% | Toxic plants, hazardous items, electrical cords, room-specific dangers |
| Comfort | 25% | Pet zones (sleeping, feeding, play), enrichment areas |
| Durability | 20% | Scratch-resistant materials, chew-proof furniture |
| Cleanliness | 20% | Fur management, litter tracking, easy-clean surfaces |

### Features

- **Safety Audit** — Detect 10 toxic plants, 8 hazardous items, and room-specific dangers (PTFE cookware for birds, recliner crush risk for cats)
- **Pet Zone Planner** — Species-specific zones: Dog (4 zones), Cat (6 zones including climbing wall and litter area), Bird (2 zones), Rabbit (2 zones)
- **Material Advisor** — Recommended vs avoid for flooring, upholstery, rugs, curtains per species
- **Plant Safety** — 10 toxic plant database + 8 safe alternatives with benefits
- **Cleaning Tips** — Species-specific maintenance routines (vacuuming, litter, cage cleaning)
- **Product Recommendations** — Curated catalog of 30 pet products across 11 categories, priority-sorted (essential/recommended/optional)
- **Behavioral Adaptation** — Adjusts recommendations based on pet traits (destructive, shedding, climbing, high energy)

### Example

```
Pet: Luna (Cat, Medium, Indoor, Climbs Furniture, Sheds Fur)
Room: Living Room | Safety Score: 7.2/10

Hazards Found:
  [HIGH] Blinds cords — strangulation risk → Switch to cordless blinds ($60)
  [MED]  Essential oil diffuser — toxic to cats → Use pet-safe alternatives
  [MED]  Tall unstable shelves — climbing risk → Secure with anti-tip straps ($25)

Pet Zones:
  1. Luna's Sleeping     — elevated shelf, warm sunny spot      $70
  2. Luna's Climbing     — wall shelves + cat tree              $120
  3. Luna's Scratching   — sisal post near sofa                $35
  4. Luna's Window Perch — suction cup perch at sunniest window $25
  5. Luna's Hiding       — cat cave under side table            $30
  6. Luna's Litter       — enclosed box in bathroom corner      $50

Materials: Use microfiber upholstery (avoid leather), low-pile rugs, short curtains
```

## AI-Powered Seasonal & Holiday Room Themes

Transform your room for every season and celebration with AI-generated decor plans, DIY projects, scent recommendations, and smooth transitions between themes.

### Supported Themes

**Seasons:** Spring (bloom & pastels), Summer (tropical & coastal), Autumn (harvest & warmth), Winter (hygge & wonderland)

**Holidays:** Christmas, Halloween, Eid al-Fitr, Diwali, Valentine's Day, Thanksgiving, Easter, Lunar New Year, Hanukkah, New Year

### Features

- **Auto Season Detection** — Detects current season by hemisphere with upcoming holiday lookahead
- **Complete Theme Packages** — Color palettes, textures, materials, decor items, lighting mood
- **DIY Projects** — Step-by-step instructions with materials lists, difficulty levels, time and cost estimates
- **Scent Recommendations** — Season-appropriate scents with method (candle, diffuser, simmer pot) and placement
- **Budget Tiers** — Budget (0.5x), Medium (1x), Premium (2x) pricing for all recommendations
- **Intensity Control** — From subtle seasonal hints (reusable items only) to full room transformation
- **Reusability Scoring** — Track what percentage of decor can be reused next year
- **Theme Transitions** — Gradual 7-day or immediate transition plans with keep/add/remove item lists
- **Multi-Cultural** — Authentic themes for global celebrations (Eid, Diwali, Lunar New Year, etc.)

### Example

```
Theme: Warm Autumn Harvest | Budget: Medium | Intensity: 70%

Color Palette:
  Primary:  Cornsilk, Antique White, Linen
  Accent:   Chocolate, Peru, Saddle Brown, Firebrick, Goldenrod

Decor Items:
  1. Pumpkin & gourd display      — dining table    $15   (seasonal)
  2. Chunky knit throw blanket    — sofa arm        $55   (reusable)
  3. Dried wheat bundle           — entrance vase   $12   (reusable)
  4. Copper candle holders        — mantel          $30   (reusable)
  5. Fall leaf garland            — doorway         $18   (reusable)

DIY Project: Cinnamon Stick Candle Wrap
  Difficulty: Easy | Time: 20 min | Cost: $6
  Materials: pillar candle, cinnamon sticks, twine, hot glue

Scents: Cinnamon & apple (simmer pot), Pumpkin spice (candle), Cedarwood (diffuser)

Reusability: 83% of items reusable next season
```

## AI-Powered Feng Shui Analysis

Analyze your room's energy flow using traditional Feng Shui principles enhanced with AI object detection and spatial analysis.

### Analysis Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Chi Flow | 25% | Energy circulation paths, pathway blockages |
| Element Balance | 20% | Five Elements (Wood, Fire, Earth, Metal, Water) ratio |
| Yin-Yang | 15% | Balance between active and passive energy |
| Clutter | 20% | Object density and visual chaos |
| Commanding Position | 20% | Key furniture placement relative to doorways |

### Features

- **Bagua Map** — 9-zone room analysis mapping directions to life areas (Career, Wealth, Love, Health, etc.)
- **Five Elements** — Detect current element levels from furniture and compare to room-specific ideal ratios
- **Chi Flow Analysis** — Identify blocked pathways, door-window alignment issues, and sha chi
- **Commanding Position** — Verify bed, desk, and sofa face the entrance for security and authority
- **Cure Recommendations** — Prioritized, actionable fixes with element, placement, and estimated cost
- **Color Guidance** — Room-specific color recommendations (primary, accent, avoid) with Feng Shui reasoning
- **Personal Kua Number** — Birth year calculation for lucky/unlucky directions and compatible elements
- **Furniture Placement** — AI-generated positioning advice with Feng Shui reasoning for each item

### Example Output

```
Room: Living Room | Direction: South | Score: 7.2/10

Element Balance:
  Wood:  ████████░░ 35% (ideal: 20%) — excess
  Fire:  ███░░░░░░░ 15% (ideal: 20%) — deficient
  Earth: █████░░░░░ 25% (ideal: 25%) — balanced
  Metal: ██░░░░░░░░ 10% (ideal: 15%) — deficient
  Water: ███░░░░░░░ 15% (ideal: 20%) — deficient

Cures:
  1. [HIGH] Add candles or warm lighting to strengthen Fire element — south area
  2. [MED]  Place a small tabletop fountain for Water element — north area
  3. [MED]  Include metallic frames or wind chimes — west corner
```

## Smart Lighting Integration with Mood Detection

AI-powered lighting system that detects your mood and generates optimal lighting scenes for any room.

### Features

- **Mood Detection** — Analyze mood from natural language, activity, time of day, and energy level
- **10 Mood Profiles** — Relaxed, Focused, Energetic, Romantic, Cozy, Creative, Social, Sleepy, Refreshed, Melancholic
- **Scene Generation** — Full lighting configuration with color temperature (1800K-6500K), brightness, fixtures, and zones
- **Circadian Rhythm** — 13-phase daily schedule that follows your natural body clock with sunrise/sunset simulation
- **Smart Home Export** — Export to Philips Hue, LIFX, HomeKit, Google Home, and Alexa
- **Room-Aware** — Adjusts lighting based on room type (bedroom dims, kitchen brightens, office shifts cooler)
- **Analytics & Learning** — Track usage patterns, mood distribution, and get personalized recommendations

### Example Flow

```
User Input: "I want to relax after a long day" + evening + low energy
    ↓
Mood Analysis: relaxed (87% confidence), energy: 0.25, warmth: 0.75
    ↓
Lighting Scene:
  Color Temperature: 2700K (warm amber)
  Brightness: 40%
  Fixtures: Floor lamp (35%), Table lamp (30%), LED strip (20%)
  Transition: 2 seconds
  Ambiance: "Soft golden glow with gentle shadows..."
    ↓
Export to Philips Hue / LIFX / HomeKit / Google Home / Alexa
```

## Multi-Room House Design

Instead of redesigning a single room, the system redesigns an entire apartment or house while maintaining a consistent visual identity.

### How It Works

1. **Create a House Project** — name your project, select a design style, and define your rooms (Living Room, Bedroom, Kitchen, Office, etc.)
2. **Configure Shared Theme** — choose a unified color palette, material preferences, and lighting scheme
3. **Generate All Rooms** — AI generates designs for every room using the shared theme DNA
4. **Review & Refine** — adjust individual rooms while maintaining cross-room consistency
5. **View Cost Report** — see per-room costs plus shared elements (flooring transitions, consistent paint, lighting)

### Shared Design Elements

```
Style:           Scandinavian
Primary Colors:  White, Light Blue, Natural Oak
Materials:       Light oak, birch, linen, wool, ceramic
Lighting:        Warm ambient, natural light emphasis
Principles:      Emphasize natural light, functional minimal furniture,
                 layer neutral textures, incorporate natural materials
```

### Consistency Engine

The system validates cross-room visual coherence across three dimensions:
- **Color Consistency (40%)** — palette overlap with house theme
- **Style Consistency (35%)** — furniture style matching
- **Material Consistency (25%)** — material language alignment

### Supported Room Types

Living Room, Bedroom, Kitchen, Bathroom, Dining Room, Office, Hallway, Studio

## System Architecture

```
┌───────────────────┐
│   Flutter App     │
└─────────┬─────────┘
          │
          v
┌───────────────────┐
│   FastAPI Server  │
└─────────┬─────────┘
          │
    ┌─────┼──────────────────┐
    v     v                  v
┌────────┐ ┌──────────┐ ┌──────────┐
│AI Agent│ │ Database │ │AR Engine │
└───┬────┘ └──────────┘ └──────────┘
    │
    v
┌────────────────────────────┐
│ Room Analysis (YOLO + SAM) │
├────────────────────────────┤
│ Design Generation (SDXL)   │
├────────────────────────────┤
│ Recommendation Engine      │
├────────────────────────────┤
│ Cost Estimation Engine     │
└────────────────────────────┘
```

## Technology Stack

### Mobile
- Flutter with Riverpod state management
- AR Flutter Plugins (ARCore / ARKit)

### Backend
- Python 3.11+ with FastAPI
- PostgreSQL database
- MinIO / AWS S3 for object storage
- Redis for caching

### AI Models
- **Detection:** YOLOv11
- **Segmentation:** Segment Anything Model (SAM)
- **Image Generation:** Stable Diffusion XL, FLUX.1, ControlNet
- **LLM:** OpenAI API or Google Gemini API

## Project Structure

```
Smart-AI-Interior-Designer-with-AR/
│
├── mobile_app/          # Flutter mobile application
├── backend/             # FastAPI server
├── ai_services/         # AI models and pipelines
├── infrastructure/      # Database, Docker, storage configs
├── shared/              # Common configurations and utilities
└── docs/                # Documentation and architecture diagrams
```

## AI Pipeline

```
User Image → Room Analysis (YOLO + SAM)
           → Scene Understanding JSON
           → LLM Prompt Generator
           → Stable Diffusion / ControlNet
           → Generated Design Image
           → Furniture Extraction
           → Recommendation Engine
           → Cost Estimation Engine
           → AR Rendering Data
           → Flutter AR View
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/room/upload` | Upload room image |
| GET | `/api/v1/room/{id}` | Get room details |
| POST | `/api/v1/design/generate` | Generate AI design |
| POST | `/api/v1/design/enhance` | Enhance existing design |
| POST | `/api/v1/furniture/recommend` | Get furniture recommendations |
| POST | `/api/v1/cost/calculate` | Calculate renovation cost |
| POST | `/api/v1/ar/generate-scene` | Generate AR scene data |
| POST | `/api/v1/house/project` | Create multi-room house project |
| GET | `/api/v1/house/projects` | List all house projects |
| GET | `/api/v1/house/project/{id}` | Get house project details |
| PATCH | `/api/v1/house/project/{id}` | Update house project |
| POST | `/api/v1/house/project/{id}/generate` | Generate all room designs |
| POST | `/api/v1/house/room/refine` | Refine individual room design |
| GET | `/api/v1/house/project/{id}/cost` | Get house cost report |
| DELETE | `/api/v1/house/project/{id}` | Delete house project |
| POST | `/api/v1/lighting/detect-mood` | Detect mood and recommend lighting |
| POST | `/api/v1/lighting/scenes` | Create lighting scene |
| GET | `/api/v1/lighting/scenes` | List saved scenes |
| GET | `/api/v1/lighting/scenes/{id}` | Get scene details |
| PATCH | `/api/v1/lighting/scenes/{id}` | Update scene |
| DELETE | `/api/v1/lighting/scenes/{id}` | Delete scene |
| POST | `/api/v1/lighting/circadian` | Generate circadian schedule |
| POST | `/api/v1/lighting/profiles` | Create mood profile |
| GET | `/api/v1/lighting/profiles` | List mood profiles |
| POST | `/api/v1/lighting/feedback` | Submit scene rating |
| POST | `/api/v1/lighting/export` | Export to smart home platform |
| GET | `/api/v1/lighting/insights` | Get lighting usage analytics |
| POST | `/api/v1/feng-shui/analyze` | Run Feng Shui analysis |
| GET | `/api/v1/feng-shui/analyses` | List all analyses |
| GET | `/api/v1/feng-shui/analyses/{id}` | Get analysis details |
| POST | `/api/v1/feng-shui/cures/apply` | Mark a cure as applied |
| POST | `/api/v1/feng-shui/compatibility` | Personal Kua number check |
| POST | `/api/v1/seasonal/detect` | Auto-detect current season & holidays |
| POST | `/api/v1/seasonal/generate` | Generate seasonal/holiday theme |
| POST | `/api/v1/seasonal/transition` | Plan theme transition |
| GET | `/api/v1/seasonal/themes` | List saved themes |
| GET | `/api/v1/seasonal/themes/{id}` | Get theme details |
| POST | `/api/v1/seasonal/themes/{id}/favorite` | Toggle favorite |
| DELETE | `/api/v1/seasonal/themes/{id}` | Delete theme |
| POST | `/api/v1/pet-friendly/profiles` | Create pet profile |
| GET | `/api/v1/pet-friendly/profiles` | List pet profiles |
| GET | `/api/v1/pet-friendly/profiles/{id}` | Get pet profile |
| POST | `/api/v1/pet-friendly/analyze` | Run pet-friendly room analysis |
| GET | `/api/v1/pet-friendly/analyses` | List past analyses |
| POST | `/api/v1/3d/generate` | Generate 3D room model |
| GET | `/api/v1/3d/models` | List 3D models |
| GET | `/api/v1/3d/models/{id}` | Get 3D model details |
| DELETE | `/api/v1/3d/models/{id}` | Delete 3D model |
| POST | `/api/v1/3d/walkthrough/start` | Start walkthrough session |
| POST | `/api/v1/3d/walkthrough/end` | End walkthrough session |

## Getting Started

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11+ | https://python.org/downloads |
| Flutter | 3.19+ | https://docs.flutter.dev/get-started/install |
| Docker & Docker Compose | Latest | https://docker.com/products/docker-desktop |
| Git | Latest | https://git-scm.com/downloads |
| CUDA GPU (optional) | For AI models | Required only for AI service inference |

### Quick Start with Docker (All Platforms)

```bash
git clone https://github.com/mohamedshhahat1/Smart-AI-Interior-Designer-with-AR.git
cd Smart-AI-Interior-Designer-with-AR

# Copy environment file
cp .env.example .env

# Start all services (backend, AI, database, Redis, MinIO)
docker compose up -d

# Verify all services are running
docker compose ps
```

Then open:
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin / minioadmin)

### Production Deployment

```bash
# Use the production compose file with your .env.production
docker compose -f docker-compose.prod.yml up -d

# Run database migrations
docker compose exec backend alembic upgrade head
```

---

## Running on Windows

### Option 1: Docker Desktop (Recommended)

```powershell
# Install WSL 2 if prompted
wsl --install

# Clone and start
git clone https://github.com/mohamedshhahat1/Smart-AI-Interior-Designer-with-AR.git
cd Smart-AI-Interior-Designer-with-AR

copy .env.example .env
docker compose up -d
```

### Option 2: Manual Setup on Windows

#### Step 1: Start PostgreSQL & Redis via Docker

```powershell
docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=smart_interior postgres:15-alpine
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

#### Step 2: Backend Setup

```powershell
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set ENVIRONMENT=development
set DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/smart_interior
set REDIS_URL=redis://localhost:6379/0
set SECRET_KEY=dev-only-insecure-key-do-not-use-in-production
set DEBUG=true

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

Backend API docs available at http://localhost:8000/docs

#### Step 3: AI Service (Optional — requires GPU)

```powershell
cd ai_services

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload --port 8001
```

#### Step 4: Flutter Mobile App

```powershell
cd mobile_app

flutter pub get

# Run on connected Android device or emulator
flutter run

# Or run on Chrome (web mode)
flutter run -d chrome
```

> **Note:** Update the API URL in `mobile_app/lib/core/constants/app_constants.dart`:
> ```dart
> static const String baseUrl = 'http://10.0.2.2:8000/api/v1';  // Android emulator
> // or
> static const String baseUrl = 'http://localhost:8000/api/v1';   // Web / iOS simulator
> ```

---

## Running on macOS / Linux

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export ENVIRONMENT=development
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/smart_interior
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=dev-only-insecure-key-do-not-use-in-production
export DEBUG=true

alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Mobile App

```bash
cd mobile_app
flutter pub get
flutter run
```

---

## Running Tests

```bash
cd backend
pip install -r requirements-dev.txt

# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_auth.py -v
```

---

## Quick API Test

```bash
# Health check
curl http://localhost:8000/health

# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `pip install` fails on `asyncpg` (Windows) | Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |
| Docker: "WSL 2 not installed" | Run `wsl --install` in PowerShell as Admin, restart PC |
| Port 5432 already in use | Stop existing PostgreSQL: `net stop postgresql-x64-15` (Windows) or `brew services stop postgresql` (macOS) |
| Flutter: no device found | Run `flutter doctor` and follow instructions |
| CUDA not available | AI service works without GPU using fallback/mock responses |
| `alembic upgrade head` fails | Ensure PostgreSQL is running and DATABASE_URL is correct |
| CORS errors in browser | Check `CORS_ALLOWED_ORIGINS` in your `.env` file includes your frontend URL |
| Redis connection refused | Ensure Redis is running: `docker ps` or `redis-cli ping` |

## License

MIT License

## Authors

- Mohamed Shahat
