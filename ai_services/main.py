import logging
import os
import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from ai_services.vision.room_analysis import room_analyzer
from ai_services.generation.prompt_builder import prompt_builder
from ai_services.generation.stable_diffusion import sdxl_generator
from ai_services.generation.controlnet_pipeline import controlnet_pipeline
from ai_services.recommendation.catalog_search import catalog_search
from ai_services.agents.interior_ai_agent import interior_agent
from ai_services.utils.image_processing import load_image

logger = logging.getLogger(__name__)

DESIGN_OUTPUT_DIR = os.getenv("DESIGN_OUTPUT_DIR", "/tmp/designs")

app = FastAPI(
    title="Smart Interior AI - AI Services",
    version="1.0.0",
    description="Computer Vision, Design Generation, and AI Agent APIs",
)


class AnalyzeRequest(BaseModel):
    image_url: str


class DesignRequest(BaseModel):
    room_analysis: dict
    style: str
    prompt: Optional[str] = None
    budget: Optional[float] = None
    preserve_layout: bool = True


class EnhanceRequest(BaseModel):
    design_data: dict
    instruction: str


class RecommendRequest(BaseModel):
    detected_objects: dict
    style: str
    budget: Optional[float] = None


class ChatRequest(BaseModel):
    room_data: Optional[dict] = None
    message: str
    conversation_history: list[dict] = []


def _render_design(prompt_data: dict, image_url: Optional[str], preserve_layout: bool) -> Optional[str]:
    """Render a design image and return its saved path, or None on failure."""
    try:
        original = None
        if preserve_layout and image_url:
            try:
                # load_image transparently handles both local paths and http(s) URLs.
                original = load_image(image_url)
            except Exception as exc:
                logger.warning("Could not load source image for layout preservation: %s", exc)
                original = None

        if original is not None:
            generated_image = controlnet_pipeline.redesign_room(
                original_image=original,
                prompt_data=prompt_data,
            )
        else:
            generated_image = sdxl_generator.generate(
                positive_prompt=prompt_data["positive"],
                negative_prompt=prompt_data["negative"],
            )

        os.makedirs(DESIGN_OUTPUT_DIR, exist_ok=True)
        output_filename = os.path.join(DESIGN_OUTPUT_DIR, f"{uuid.uuid4()}.jpg")
        generated_image.save(output_filename, quality=95)
        return output_filename
    except Exception:
        logger.exception("Image generation failed")
        return None


@app.post("/vision/analyze")
async def analyze_room(request: AnalyzeRequest):
    result = room_analyzer.analyze(request.image_url)
    return result


@app.post("/generation/design")
async def generate_design(request: DesignRequest):
    room_type = request.room_analysis.get("room_type", "living_room")
    detected = request.room_analysis.get("detected_objects", [])
    object_labels = []
    if isinstance(detected, list):
        object_labels = [
            obj.get("label", str(obj)) if isinstance(obj, dict) else str(obj)
            for obj in detected
        ]

    prompt_data = prompt_builder.build_design_prompt(
        style=request.style,
        room_type=room_type,
        user_prompt=request.prompt,
        detected_objects=object_labels,
        budget=request.budget,
    )

    generated_image_url = _render_design(
        prompt_data=prompt_data,
        image_url=request.room_analysis.get("image_url"),
        preserve_layout=request.preserve_layout,
    )

    try:
        furniture_list = catalog_search.search(style=request.style, max_price=request.budget)
    except Exception:
        logger.exception("Furniture catalog lookup failed")
        furniture_list = []

    try:
        design_brief = await interior_agent.generate_design_brief(
            room_data=request.room_analysis,
            style=request.style,
            budget=request.budget,
        )
        brief_text = design_brief.get("brief", "")
    except Exception:
        logger.exception("Design brief generation failed")
        brief_text = ""

    return {
        "image_url": generated_image_url,
        "color_palette": prompt_data.get("style"),
        "furniture_list": furniture_list,
        "ar_scene_data": {},
        "design_brief": brief_text,
    }


@app.post("/generation/enhance")
async def enhance_design(request: EnhanceRequest):
    current_style = request.design_data.get("style", "modern")
    prompt_data = prompt_builder.build_enhancement_prompt(
        current_style=current_style,
        instruction=request.instruction,
    )

    rendered = _render_design(
        prompt_data=prompt_data,
        image_url=request.design_data.get("image_url"),
        preserve_layout=True,
    )
    enhanced_image_url = rendered or request.design_data.get("image_url")

    return {
        "image_url": enhanced_image_url,
        "furniture_list": request.design_data.get("furniture_list", []),
        "color_palette": request.design_data.get("color_palette"),
        "enhanced": True,
    }


@app.post("/recommendation/furniture")
async def recommend_furniture(request: RecommendRequest):
    catalog_results = catalog_search.search(
        style=request.style,
        max_price=request.budget,
    )
    return catalog_results


@app.post("/agents/chat")
async def chat_with_agent(request: ChatRequest):
    result = await interior_agent.chat(
        message=request.message,
        room_data=request.room_data,
        conversation_history=request.conversation_history,
    )
    return result


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-services"}
