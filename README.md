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
