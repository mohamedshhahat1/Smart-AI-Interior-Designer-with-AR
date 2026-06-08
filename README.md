# Smart AI Interior Designer with AR

AI-powered mobile application that scans rooms, generates interior design concepts, places virtual furniture using Augmented Reality, and estimates renovation costs.

## Features

### Room Analysis & Design Generation
- **Room Scanning** — Capture room photos via smartphone camera
- **AI Object Detection** — Identify furniture, walls, floor, windows, and doors using YOLOv11 + SAM segmentation
- **AI Design Generation** — Generate multiple design concepts from text prompts using Stable Diffusion XL, ControlNet, and FLUX
- **Design Enhancement** — Refine and iterate on generated designs with natural language commands

### AR Visualization
- **Real-time AR** — Place virtual furniture in your room using ARCore (Android) and ARKit (iOS)
- **3D Furniture Models** — CC0-licensed GLB models (chairs, tables, sofas, beds, shelves, lamps, and more)
- **Tap-to-Place** — Tap any detected surface to place, move, or remove 3D furniture
- **Plane Detection** — Automatic horizontal and vertical surface detection

### AI Design Assistant
- **Natural Language Chat** — Describe what you want and get AI-powered design suggestions
- **Context-Aware** — The assistant understands your room layout and current design

### Furniture Recommendations
- **Product Matching** — AI-matched furniture from real product catalogs based on detected room needs
- **Category Filtering** — Browse by category, style, and budget
- **Cost Estimation** — Per-item and total renovation cost calculation with budget optimization

### Multi-Room House Design
- **Whole-Home Projects** — Design entire apartments or houses with a unified visual theme
- **Shared Theme DNA** — Consistent color palette, materials, and lighting across all rooms
- **Room-by-Room Generation** — AI generates designs for each room using the shared theme
- **Consistency Engine** — Validates cross-room coherence across color (40%), style (35%), and material (25%)
- **Cost Report** — Per-room costs plus shared elements (flooring transitions, paint, lighting)
- **Supported Room Types** — Living Room, Bedroom, Kitchen, Bathroom, Dining Room, Office, Hallway, Studio

### Smart Lighting & Mood Detection
- **Mood Detection** — Analyze mood from natural language, activity, time of day, and energy level
- **10 Mood Profiles** — Relaxed, Focused, Energetic, Romantic, Cozy, Creative, Social, Sleepy, Refreshed, Melancholic
- **Scene Generation** — Full lighting configuration with color temperature (1800K-6500K), brightness, and zones
- **Circadian Rhythm** — 13-phase daily schedule following your natural body clock
- **Smart Home Export** — Export to Philips Hue, LIFX, HomeKit, Google Home, and Alexa

### Feng Shui Analysis
- **Bagua Map** — 9-zone room analysis mapping directions to life areas
- **Five Elements** — Detect Wood, Fire, Earth, Metal, Water balance from furniture
- **Chi Flow** — Identify blocked pathways, door-window alignment issues, and sha chi
- **Commanding Position** — Verify bed, desk, and sofa face the entrance
- **Cure Recommendations** — Prioritized fixes with element, placement, and estimated cost
- **Personal Kua Number** — Birth year calculation for lucky directions and compatible elements

### Seasonal & Holiday Themes
- **Auto Season Detection** — Detects current season by hemisphere with holiday lookahead
- **10 Holiday Themes** — Christmas, Halloween, Eid al-Fitr, Diwali, Valentine's Day, Thanksgiving, Easter, Lunar New Year, Hanukkah, New Year
- **Complete Theme Packages** — Color palettes, textures, decor items, lighting mood
- **DIY Projects** — Step-by-step instructions with materials, difficulty, time, and cost
- **Budget Tiers** — Budget (0.5x), Medium (1x), Premium (2x) pricing
- **Theme Transitions** — Gradual 7-day or immediate transition plans

### Pet-Friendly Design
- **Safety Audit** — Detect toxic plants, hazardous items, and room-specific dangers
- **Pet Zone Planner** — Species-specific zones for dogs (4), cats (6), birds (2), rabbits (2)
- **Material Advisor** — Recommended vs. avoid materials per species for flooring, upholstery, rugs
- **Product Recommendations** — 30 curated products across 11 categories, priority-sorted

### 3D Walkthrough
- **3D Room Reconstruction** — Walls, floor, ceiling mesh from depth estimation (MiDaS)
- **Furniture Placement** — 15-item 3D catalog with automatic smart positioning
- **6 Camera Presets** — Overview, entrance, center, left/right corners, low angle
- **3 Walkthrough Modes** — Room tour, orbit, and furniture-focus paths with easing curves
- **GLB + USDZ Export** — Industry-standard 3D formats for web and iOS AR

### User Management
- **Registration & Login** — JWT-based authentication with secure token storage
- **Edit Profile** — Update name and email with validation
- **Change Password** — Current password verification with bcrypt hashing
- **Design History** — Track all generated designs

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Mobile** | Flutter 3.19+, Riverpod, go_router, Dio |
| **AR** | ar_flutter_plugin_2 (ARCore / ARKit), Sceneview Android 2.2.1 |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy async |
| **Database** | PostgreSQL 15 |
| **Cache** | Redis 7 |
| **Object Storage** | MinIO (S3-compatible) |
| **AI Detection** | YOLOv11, Segment Anything Model (SAM) |
| **AI Generation** | Stable Diffusion XL, FLUX.1, ControlNet |
| **LLM** | OpenAI API / Google Gemini API |
| **3D** | MiDaS depth estimation, GLB/USDZ export |
| **Deployment** | Docker Compose, Nginx |

## Project Structure

```
Smart-AI-Interior-Designer-with-AR/
├── mobile_app/              # Flutter mobile application
│   ├── lib/
│   │   ├── core/            # Constants, theme, utilities
│   │   ├── data/            # API services, models, repositories
│   │   └── presentation/    # Screens, widgets, providers
│   ├── android/             # Android config (minSdk 28)
│   └── ios/                 # iOS config (platform 14.0)
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── api/routes/      # Route handlers (14 modules)
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── services/        # Business logic
│   │   └── core/            # Config, security, dependencies
│   ├── alembic/             # Database migrations
│   └── requirements.txt
├── ai_services/             # AI model inference service
│   └── requirements.txt
├── infrastructure/          # Database seeds, Docker, Nginx configs
├── shared/                  # Shared configurations
├── docker-compose.yml       # Development environment
├── docker-compose.prod.yml  # Production environment (with Nginx)
└── docs/                    # Architecture documentation
```

## Architecture

```
┌────────────────────────┐
│   Flutter Mobile App   │
│  (Riverpod + go_router)│
└──────────┬─────────────┘
           │ HTTP / JWT
           v
┌────────────────────────┐       ┌──────────────────┐
│     FastAPI Backend    │──────>│    AI Service    │
│ (Pydantic v2, SQLAlchemy)     │ (YOLOv11, SDXL)  │
└──────┬───────┬─────────┘       └──────────────────┘
       │       │
  ┌────┘       └──────┐
  v                   v
┌──────────┐   ┌─────────────┐
│PostgreSQL│   │ MinIO (S3)  │
│  + Redis │   │ Image Store │
└──────────┘   └─────────────┘
```

### AI Pipeline

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

## Getting Started

### Prerequisites

| Tool | Version | Required For |
|------|---------|-------------|
| [Docker & Docker Compose](https://docker.com/products/docker-desktop) | Latest | All services |
| [Flutter](https://docs.flutter.dev/get-started/install) | 3.19+ | Mobile app |
| [Python](https://python.org/downloads) | 3.11+ | Manual backend setup (without Docker) |
| [Git](https://git-scm.com/downloads) | Latest | Cloning the repo |
| NVIDIA GPU + CUDA | Optional | AI model inference (faster generation) |

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/mohamedshhahat1/Smart-AI-Interior-Designer-with-AR.git
cd Smart-AI-Interior-Designer-with-AR

# Copy and configure environment variables
cp .env.example .env
# Edit .env to set OPENAI_API_KEY and/or GOOGLE_API_KEY

# Start all services (backend, AI service, PostgreSQL, Redis, MinIO)
docker compose up -d

# Run database migrations
docker compose exec backend alembic upgrade head

# Verify services are running
docker compose ps
```

Services will be available at:
- **Backend API Docs** — http://localhost:8000/docs
- **AI Service** — http://localhost:8001
- **MinIO Console** — http://localhost:9001 (minioadmin / minioadmin)

### Flutter Mobile App

```bash
cd mobile_app

# Install dependencies
flutter pub get

# Run on connected device or emulator
flutter run
```

> **API URL Configuration** — Update `mobile_app/lib/core/constants/app_constants.dart`:
> ```dart
> static const String baseUrl = 'http://10.0.2.2:8000/api/v1';  // Android emulator
> // or
> static const String baseUrl = 'http://localhost:8000/api/v1';   // iOS simulator / Web
> ```

### Platform Requirements

**Android:**
- minSdk 28 (Android 9.0+)
- ARCore-supported device for AR features

**iOS:**
- iOS 14.0+
- ARKit-capable device (iPhone 6s or later) for AR features
- Camera, Photo Library, and Location permissions configured in Info.plist

## Manual Setup (Without Docker)

### 1. Start PostgreSQL & Redis

```bash
# Using Docker for just the databases
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=smart_interior \
  postgres:15-alpine

docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=development
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/smart_interior
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=dev-only-insecure-key-do-not-use-in-production
export DEBUG=true

# Run migrations and start server
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 3. AI Service (Optional)

```bash
cd ai_services
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload --port 8001
```

### 4. MinIO (Optional — for image storage)

```bash
docker run -d --name minio -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"
```

## Production Deployment

```bash
# Configure production environment
cp .env.example .env.production
# Edit .env.production with secure values for:
#   POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
#   REDIS_PASSWORD
#   SECRET_KEY (generate a strong random key)
#   MINIO_ROOT_USER, MINIO_ROOT_PASSWORD
#   OPENAI_API_KEY and/or GOOGLE_API_KEY
#   CORS_ALLOWED_ORIGINS

# Deploy with Nginx reverse proxy
docker compose -f docker-compose.prod.yml --env-file .env.production up -d

# Run migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

The production setup includes:
- **Nginx** reverse proxy on ports 80/443
- **Redis** with password authentication
- **No exposed database ports** — PostgreSQL and Redis are internal only

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login and receive JWT token |
| GET | `/api/v1/auth/me` | Get current user profile |
| PATCH | `/api/v1/auth/me` | Update profile (name, email) |
| POST | `/api/v1/auth/change-password` | Change password |

### Room & Design
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/room/upload` | Upload room image |
| GET | `/api/v1/room/{id}` | Get room details |
| POST | `/api/v1/design/generate` | Generate AI design |
| POST | `/api/v1/design/enhance` | Enhance existing design |

### Furniture & Cost
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/furniture/recommend` | Get furniture recommendations |
| POST | `/api/v1/cost/calculate` | Calculate renovation cost |

### AR
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ar/generate-scene` | Generate AR scene data |

### Multi-Room House
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/house/project` | Create house project |
| GET | `/api/v1/house/projects` | List all house projects |
| GET | `/api/v1/house/project/{id}` | Get project details |
| PATCH | `/api/v1/house/project/{id}` | Update project |
| POST | `/api/v1/house/project/{id}/generate` | Generate all room designs |
| POST | `/api/v1/house/room/refine` | Refine individual room |
| GET | `/api/v1/house/project/{id}/cost` | Get cost report |
| DELETE | `/api/v1/house/project/{id}` | Delete project |

### Smart Lighting
| Method | Endpoint | Description |
|--------|----------|-------------|
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
| GET | `/api/v1/lighting/insights` | Get lighting analytics |

### Feng Shui
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/feng-shui/analyze` | Run Feng Shui analysis |
| GET | `/api/v1/feng-shui/analyses` | List all analyses |
| GET | `/api/v1/feng-shui/analyses/{id}` | Get analysis details |
| POST | `/api/v1/feng-shui/cures/apply` | Mark a cure as applied |
| POST | `/api/v1/feng-shui/compatibility` | Personal Kua number check |

### Seasonal Themes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/seasonal/detect` | Auto-detect season & holidays |
| POST | `/api/v1/seasonal/generate` | Generate theme |
| POST | `/api/v1/seasonal/transition` | Plan theme transition |
| GET | `/api/v1/seasonal/themes` | List saved themes |
| GET | `/api/v1/seasonal/themes/{id}` | Get theme details |
| POST | `/api/v1/seasonal/themes/{id}/favorite` | Toggle favorite |
| DELETE | `/api/v1/seasonal/themes/{id}` | Delete theme |

### Pet-Friendly Design
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/pet-friendly/profiles` | Create pet profile |
| GET | `/api/v1/pet-friendly/profiles` | List pet profiles |
| GET | `/api/v1/pet-friendly/profiles/{id}` | Get pet profile |
| POST | `/api/v1/pet-friendly/analyze` | Run pet-friendly analysis |
| GET | `/api/v1/pet-friendly/analyses` | List past analyses |

### 3D Walkthrough
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/3d/generate` | Generate 3D room model |
| GET | `/api/v1/3d/models` | List 3D models |
| GET | `/api/v1/3d/models/{id}` | Get model details |
| DELETE | `/api/v1/3d/models/{id}` | Delete model |
| POST | `/api/v1/3d/walkthrough/start` | Start walkthrough session |
| POST | `/api/v1/3d/walkthrough/end` | End walkthrough session |

### AI Assistant
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/assistant/chat` | Send message to AI assistant |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/smart_interior` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT signing key | (required in production) |
| `OPENAI_API_KEY` | OpenAI API key for LLM features | (optional) |
| `GOOGLE_API_KEY` | Google Gemini API key | (optional) |
| `MINIO_ENDPOINT` | MinIO server address | `localhost:9000` |
| `MINIO_ACCESS_KEY` | MinIO access key | `minioadmin` |
| `MINIO_SECRET_KEY` | MinIO secret key | `minioadmin` |
| `AI_SERVICE_URL` | AI inference service URL | `http://localhost:8001` |
| `ENVIRONMENT` | `development` or `production` | `development` |
| `DEBUG` | Enable debug mode | `true` |

## Running Tests

```bash
cd backend
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific module
pytest tests/test_auth.py -v
```

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

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `pip install` fails on `asyncpg` (Windows) | Install [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |
| Docker: "WSL 2 not installed" | Run `wsl --install` in PowerShell as Admin, restart |
| Port 5432 already in use | Stop existing PostgreSQL service |
| Flutter: no device found | Run `flutter doctor` and follow instructions |
| AR not working on device | Ensure device supports ARCore/ARKit and minSdk is 28+ |
| CUDA not available | AI service falls back to CPU (slower but functional) |
| `alembic upgrade head` fails | Verify PostgreSQL is running and DATABASE_URL is correct |
| CORS errors in browser | Set `CORS_ALLOWED_ORIGINS` in `.env` |
| Redis connection refused | Verify Redis is running: `redis-cli ping` |

## License

MIT License

## Author

Mohamed Shahat
