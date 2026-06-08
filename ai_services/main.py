import os
import tempfile
import uuid

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional

from ai_services.vision.room_analysis import room_analyzer
from ai_services.generation.prompt_builder import prompt_builder
from ai_services.generation.stable_diffusion import sdxl_generator
from ai_services.generation.controlnet_pipeline import controlnet_pipeline
from ai_services.recommendation.furniture_matcher import furniture_matcher
from ai_services.recommendation.catalog_search import catalog_search
from ai_services.cost.cost_calculator import cost_calculator
from ai_services.cost.budget_optimizer import budget_optimizer
from ai_services.agents.interior_ai_agent import interior_agent
from ai_services.utils.image_processing import load_image, image_to_bytes

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

    generated_image_url = None
    try:
        image_url = request.room_analysis.get("image_url")
        if request.preserve_layout and image_url and os.path.exists(image_url):
            original = load_image(image_url)
            generated_image = controlnet_pipeline.redesign_room(
                original_image=original,
                prompt_data=prompt_data,
            )
        else:
            generated_image = sdxl_generator.generate(
                positive_prompt=prompt_data["positive"],
                negative_prompt=prompt_data["negative"],
            )

        output_filename = f"/tmp/designs/{uuid.uuid4()}.jpg"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        generated_image.save(output_filename, quality=95)
        generated_image_url = output_filename
    except Exception:
        pass

    design_brief = await interior_agent.generate_design_brief(
        room_data=request.room_analysis,
        style=request.style,
        budget=request.budget,
    )

    return {
        "image_url": generated_image_url,
        "color_palette": prompt_data.get("style"),
        "furniture_list": [],
        "ar_scene_data": {},
        "design_brief": design_brief.get("brief", ""),
    }


@app.post("/generation/enhance")
async def enhance_design(request: EnhanceRequest):
    current_style = request.design_data.get("style", "modern")
    prompt_data = prompt_builder.build_enhancement_prompt(
        current_style=current_style,
        instruction=request.instruction,
    )

    enhanced_image_url = request.design_data.get("image_url")
    try:
        image_url = request.design_data.get("image_url")
        if image_url and os.path.exists(image_url):
            original = load_image(image_url)
            generated_image = controlnet_pipeline.redesign_room(
                original_image=original,
                prompt_data=prompt_data,
            )
        else:
            generated_image = sdxl_generator.generate(
                positive_prompt=prompt_data["positive"],
                negative_prompt=prompt_data["negative"],
            )

        output_filename = f"/tmp/designs/{uuid.uuid4()}.jpg"
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        generated_image.save(output_filename, quality=95)
        enhanced_image_url = output_filename
    except Exception:
        pass

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
