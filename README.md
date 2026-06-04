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

## Getting Started

### Prerequisites

- Python 3.11+
- Flutter 3.x
- PostgreSQL 15+
- Docker & Docker Compose
- CUDA-compatible GPU (for AI models)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Mobile App Setup

```bash
cd mobile_app
flutter pub get
flutter run
```

### Docker Setup

```bash
docker-compose up -d
```

## License

MIT License

## Authors

- Mohamed Shahat
