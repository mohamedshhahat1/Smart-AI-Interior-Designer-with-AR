import httpx
from typing import Optional

from backend.app.core.config import get_settings

settings = get_settings()


class AIService:
    def __init__(self):
        self.base_url = settings.ai_service_url
        self.client = httpx.AsyncClient(timeout=1200.0)

    async def analyze_room(self, image_url: str) -> dict:
        response = await self.client.post(
            f"{self.base_url}/vision/analyze",
            json={"image_url": image_url},
        )
        response.raise_for_status()
        return response.json()

    async def generate_design(
        self,
        room_analysis: dict,
        style: str,
        prompt: Optional[str] = None,
        budget: Optional[float] = None,
        preserve_layout: bool = True,
    ) -> dict:
        payload = {
            "room_analysis": room_analysis,
            "style": style,
            "prompt": prompt,
            "budget": budget,
            "preserve_layout": preserve_layout,
        }
        response = await self.client.post(
            f"{self.base_url}/generation/design",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def enhance_design(
        self, design_data: dict, instruction: str
    ) -> dict:
        response = await self.client.post(
            f"{self.base_url}/generation/enhance",
            json={"design_data": design_data, "instruction": instruction},
        )
        response.raise_for_status()
        return response.json()

    async def get_furniture_recommendations(
        self, detected_objects: dict, style: str, budget: Optional[float] = None
    ) -> list[dict]:
        response = await self.client.post(
            f"{self.base_url}/recommendation/furniture",
            json={
                "detected_objects": detected_objects,
                "style": style,
                "budget": budget,
            },
        )
        response.raise_for_status()
        return response.json()

    async def chat_with_assistant(
        self,
        room_data: dict,
        message: str,
        conversation_history: Optional[list[dict]] = None,
    ) -> dict:
        response = await self.client.post(
            f"{self.base_url}/agents/chat",
            json={
                "room_data": room_data,
                "message": message,
                "conversation_history": conversation_history or [],
            },
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()


ai_service = AIService()
