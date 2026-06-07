import os
import json
from typing import Optional

import openai
import google.generativeai as genai


SYSTEM_PROMPT = """You are an expert interior designer AI assistant. You help users redesign their rooms
by providing professional advice on:
- Color schemes and palettes
- Furniture selection and arrangement
- Lighting design
- Space optimization
- Style consistency
- Budget-friendly alternatives

When analyzing a room, consider:
1. The existing room layout and dimensions
2. Current furniture and objects detected
3. The user's preferred style and budget
4. Practical functionality of the space
5. Natural lighting and room orientation

Always provide specific, actionable recommendations. When suggesting changes, explain WHY
each change would improve the room. Include estimated costs when relevant.

Respond in a structured format with clear sections for different aspects of the design."""


class InteriorAIAgent:
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None

    def _init_openai(self):
        if self.openai_client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = openai.AsyncOpenAI(api_key=api_key)

    def _init_gemini(self):
        if self.gemini_model is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel("gemini-1.5-pro")

    async def chat(
        self,
        message: str,
        room_data: Optional[dict] = None,
        conversation_history: Optional[list[dict]] = None,
    ) -> dict:
        context = self._build_context(room_data)
        messages = self._build_messages(message, context, conversation_history)

        response_text = await self._get_llm_response(messages)

        suggestions = self._extract_suggestions(response_text)

        return {
            "message": response_text,
            "suggestions": suggestions,
        }

    async def generate_design_brief(
        self,
        room_data: dict,
        style: str,
        budget: Optional[float] = None,
    ) -> dict:
        prompt = self._build_design_brief_prompt(room_data, style, budget)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        response = await self._get_llm_response(messages)

        return {
            "brief": response,
            "style": style,
            "budget": budget,
        }

    def _build_context(self, room_data: Optional[dict]) -> str:
        if not room_data:
            return ""

        parts = ["Current Room Information:"]
        if room_data.get("room_type"):
            parts.append(f"- Room Type: {room_data['room_type']}")
        if room_data.get("area"):
            parts.append(f"- Area: {room_data['area']} sq meters")
        if room_data.get("detected_objects"):
            objects = room_data["detected_objects"]
            if isinstance(objects, list):
                labels = [
                    obj.get("label", str(obj)) if isinstance(obj, dict) else str(obj)
                    for obj in objects
                ]
                parts.append(f"- Detected Objects: {', '.join(labels)}")
            elif isinstance(objects, dict):
                parts.append(f"- Detected Objects: {json.dumps(objects)}")

        return "\n".join(parts)

    def _build_messages(
        self,
        message: str,
        context: str,
        conversation_history: Optional[list[dict]],
    ) -> list[dict]:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if context:
            messages.append({"role": "system", "content": context})

        if conversation_history:
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

        messages.append({"role": "user", "content": message})
        return messages

    def _build_design_brief_prompt(
        self, room_data: dict, style: str, budget: Optional[float]
    ) -> str:
        prompt = f"""Create a detailed interior design brief for this room:

Room Type: {room_data.get('room_type', 'Unknown')}
Area: {room_data.get('area', 'Unknown')} sq meters
Desired Style: {style}
"""
        if budget:
            prompt += f"Budget: ${budget}\n"

        detected = room_data.get("detected_objects", [])
        if detected:
            prompt += f"Current Objects: {json.dumps(detected)}\n"

        prompt += """
Please provide:
1. Color palette recommendations (primary, secondary, accent colors)
2. Furniture selection and placement
3. Lighting plan
4. Decoration and accessories
5. Estimated cost breakdown
6. Priority order for implementation
"""
        return prompt

    async def _get_llm_response(self, messages: list[dict]) -> str:
        self._init_openai()
        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
            )
            return response.choices[0].message.content

        self._init_gemini()
        if self.gemini_model:
            combined = "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            response = self.gemini_model.generate_content(combined)
            return response.text

        raise RuntimeError(
            "No LLM provider configured. Set OPENAI_API_KEY or GOOGLE_API_KEY "
            "environment variable to enable the AI assistant."
        )

    def _extract_suggestions(self, response_text: str) -> list[str]:
        suggestions = []
        lines = response_text.split("\n")
        for line in lines:
            line = line.strip()
            if line and (
                line[0].isdigit()
                or line.startswith("-")
                or line.startswith("*")
            ):
                clean = line.lstrip("0123456789.-*) ").strip()
                if len(clean) > 10 and len(clean) < 200:
                    suggestions.append(clean)

        return suggestions[:8]


interior_agent = InteriorAIAgent()
