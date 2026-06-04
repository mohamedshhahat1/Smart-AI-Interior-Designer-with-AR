from typing import Optional


MOOD_LIGHTING_PROFILES = {
    "relaxed": {
        "color_temperature": 2700,
        "brightness": 0.40,
        "color_hex": "#FFD699",
        "saturation": 0.15,
        "description": "Warm, dimmed lighting that creates a peaceful sanctuary",
        "ambiance": "Soft golden glow with gentle shadows. Use table lamps and indirect lighting to avoid harsh overhead light. Layer with candle-style fixtures for depth.",
        "fixtures": [
            {"name": "Floor Lamp", "type": "ambient", "brightness": 0.35, "position": "corner"},
            {"name": "Table Lamp", "type": "accent", "brightness": 0.30, "position": "side_table"},
            {"name": "LED Strip", "type": "indirect", "brightness": 0.20, "position": "behind_furniture"},
        ],
        "zones": [
            {"zone_name": "Primary Seating", "brightness": 0.40, "purpose": "Main relaxation area"},
            {"zone_name": "Perimeter", "brightness": 0.15, "purpose": "Ambient glow around room edges"},
        ],
    },
    "focused": {
        "color_temperature": 4500,
        "brightness": 0.80,
        "color_hex": "#FFF5E6",
        "saturation": 0.05,
        "description": "Bright, neutral-white task lighting for maximum concentration",
        "ambiance": "Clean, shadow-free illumination centered on the work area. Cool-neutral tone reduces eye strain during extended work sessions. Minimize ambient distractions.",
        "fixtures": [
            {"name": "Desk Lamp", "type": "task", "brightness": 0.90, "position": "desk"},
            {"name": "Overhead Panel", "type": "general", "brightness": 0.75, "position": "ceiling"},
            {"name": "Monitor Backlight", "type": "bias", "brightness": 0.30, "position": "behind_monitor"},
        ],
        "zones": [
            {"zone_name": "Work Surface", "brightness": 0.90, "purpose": "Direct task illumination"},
            {"zone_name": "Background", "brightness": 0.40, "purpose": "Reduce contrast fatigue"},
        ],
    },
    "energetic": {
        "color_temperature": 5500,
        "brightness": 0.95,
        "color_hex": "#F0F8FF",
        "saturation": 0.10,
        "description": "Bright, cool-daylight lighting to boost energy and alertness",
        "ambiance": "Full-spectrum daylight simulation that activates the body's wake response. Every corner illuminated evenly. Perfect for morning routines or workout spaces.",
        "fixtures": [
            {"name": "Ceiling Array", "type": "general", "brightness": 0.95, "position": "ceiling"},
            {"name": "Wall Sconce", "type": "fill", "brightness": 0.80, "position": "walls"},
            {"name": "Accent Spots", "type": "accent", "brightness": 0.70, "position": "corners"},
        ],
        "zones": [
            {"zone_name": "Full Room", "brightness": 0.95, "purpose": "Even, energizing coverage"},
        ],
    },
    "romantic": {
        "color_temperature": 2200,
        "brightness": 0.20,
        "color_hex": "#FF8C69",
        "saturation": 0.35,
        "description": "Ultra-warm, intimate candlelight-style glow",
        "ambiance": "Deep amber and rose tones create an intimate envelope of warmth. Flickering candle effects on smart bulbs add organic movement. Shadows are part of the design.",
        "fixtures": [
            {"name": "Candle Lights", "type": "ambient", "brightness": 0.15, "position": "table"},
            {"name": "Accent Uplighter", "type": "accent", "brightness": 0.20, "position": "floor"},
            {"name": "String Lights", "type": "decorative", "brightness": 0.10, "position": "perimeter"},
        ],
        "zones": [
            {"zone_name": "Dining/Intimate Area", "brightness": 0.25, "purpose": "Focal warmth"},
            {"zone_name": "Surroundings", "brightness": 0.08, "purpose": "Deep ambient shadow"},
        ],
    },
    "cozy": {
        "color_temperature": 2500,
        "brightness": 0.35,
        "color_hex": "#FFE4B5",
        "saturation": 0.20,
        "description": "Warm amber hygge lighting that wraps the room in comfort",
        "ambiance": "Multiple low-level warm sources mimic firelight. Heavy use of table and floor lamps. No overhead lighting — everything at or below eye level for maximum coziness.",
        "fixtures": [
            {"name": "Table Lamp", "type": "ambient", "brightness": 0.35, "position": "side_table"},
            {"name": "Floor Lamp", "type": "ambient", "brightness": 0.30, "position": "reading_nook"},
            {"name": "Fairy Lights", "type": "decorative", "brightness": 0.15, "position": "shelf"},
            {"name": "Salt Lamp", "type": "accent", "brightness": 0.10, "position": "corner"},
        ],
        "zones": [
            {"zone_name": "Reading Nook", "brightness": 0.40, "purpose": "Focused cozy light"},
            {"zone_name": "General", "brightness": 0.20, "purpose": "Warm ambient fill"},
        ],
    },
    "creative": {
        "color_temperature": 3500,
        "brightness": 0.65,
        "color_hex": "#E6D5FF",
        "saturation": 0.25,
        "description": "Balanced, slightly warm lighting with creative color accents",
        "ambiance": "Neutral base with pops of color from accent lights. Not too bright, not too dim — the sweet spot for creative flow. Adjustable zones let you shift focus.",
        "fixtures": [
            {"name": "Track Light", "type": "directional", "brightness": 0.70, "position": "ceiling"},
            {"name": "Color LED Strip", "type": "accent", "brightness": 0.50, "position": "behind_desk"},
            {"name": "Spot Light", "type": "task", "brightness": 0.75, "position": "easel"},
        ],
        "zones": [
            {"zone_name": "Creative Space", "brightness": 0.70, "purpose": "Work surface illumination"},
            {"zone_name": "Inspiration Wall", "brightness": 0.45, "purpose": "Color accent display"},
        ],
    },
    "social": {
        "color_temperature": 3000,
        "brightness": 0.60,
        "color_hex": "#FFECD2",
        "saturation": 0.15,
        "description": "Warm, inviting group-friendly lighting at conversational levels",
        "ambiance": "Even, flattering warmth that makes everyone look their best. Bright enough for games and conversation, warm enough for relaxed socializing. No dark corners.",
        "fixtures": [
            {"name": "Pendant Light", "type": "general", "brightness": 0.55, "position": "ceiling_center"},
            {"name": "Wall Sconce", "type": "fill", "brightness": 0.50, "position": "walls"},
            {"name": "Accent Lamp", "type": "decorative", "brightness": 0.40, "position": "shelves"},
        ],
        "zones": [
            {"zone_name": "Gathering Area", "brightness": 0.65, "purpose": "Primary social space"},
            {"zone_name": "Bar/Snack Area", "brightness": 0.55, "purpose": "Functional accent"},
        ],
    },
    "sleepy": {
        "color_temperature": 1800,
        "brightness": 0.08,
        "color_hex": "#FF6347",
        "saturation": 0.40,
        "description": "Ultra-dim, deep-red sunset lighting for melatonin production",
        "ambiance": "Near-darkness with just enough deep red/amber to navigate safely. Zero blue light to preserve melatonin. Automated fade-to-black over 30 minutes.",
        "fixtures": [
            {"name": "Night Light", "type": "ambient", "brightness": 0.05, "position": "baseboard"},
            {"name": "Bedside Glow", "type": "task", "brightness": 0.10, "position": "nightstand"},
        ],
        "zones": [
            {"zone_name": "Bedside", "brightness": 0.10, "purpose": "Minimal navigation light"},
            {"zone_name": "Pathway", "brightness": 0.03, "purpose": "Safe movement in darkness"},
        ],
    },
    "refreshed": {
        "color_temperature": 5000,
        "brightness": 0.85,
        "color_hex": "#F0FFFF",
        "saturation": 0.05,
        "description": "Crisp, cool-white morning light that simulates sunrise",
        "ambiance": "Gradual brightening from warm amber to full daylight over 20 minutes. Activates the circadian wake response naturally. Full room coverage.",
        "fixtures": [
            {"name": "Ceiling Light", "type": "general", "brightness": 0.85, "position": "ceiling"},
            {"name": "Window Accent", "type": "fill", "brightness": 0.70, "position": "near_window"},
        ],
        "zones": [
            {"zone_name": "Full Room", "brightness": 0.85, "purpose": "Sunrise simulation"},
        ],
    },
    "melancholic": {
        "color_temperature": 2800,
        "brightness": 0.25,
        "color_hex": "#B0C4DE",
        "saturation": 0.20,
        "description": "Gentle, warm-blue undertone lighting for quiet reflection",
        "ambiance": "Soft, contemplative light that respects the mood without amplifying it. Warm base with cool-blue accent — like twilight through a window.",
        "fixtures": [
            {"name": "Floor Lamp", "type": "ambient", "brightness": 0.25, "position": "corner"},
            {"name": "Cool Accent", "type": "accent", "brightness": 0.15, "position": "wall"},
        ],
        "zones": [
            {"zone_name": "Personal Space", "brightness": 0.30, "purpose": "Gentle illumination"},
            {"zone_name": "Ambient", "brightness": 0.10, "purpose": "Soft background"},
        ],
    },
}

ROOM_TYPE_ADJUSTMENTS = {
    "bedroom": {"brightness_factor": 0.85, "warmth_offset": -200},
    "living_room": {"brightness_factor": 1.0, "warmth_offset": 0},
    "kitchen": {"brightness_factor": 1.15, "warmth_offset": 300},
    "bathroom": {"brightness_factor": 1.10, "warmth_offset": 200},
    "office": {"brightness_factor": 1.10, "warmth_offset": 500},
    "dining_room": {"brightness_factor": 0.90, "warmth_offset": -300},
}


class SceneGenerator:
    def generate_scene(
        self,
        mood: str,
        time_of_day: Optional[str] = None,
        room_type: Optional[str] = None,
        energy_level: Optional[float] = None,
        warmth_score: Optional[float] = None,
    ) -> dict:
        profile = MOOD_LIGHTING_PROFILES.get(mood, MOOD_LIGHTING_PROFILES["relaxed"])

        color_temp = profile["color_temperature"]
        brightness = profile["brightness"]

        if room_type and room_type in ROOM_TYPE_ADJUSTMENTS:
            adj = ROOM_TYPE_ADJUSTMENTS[room_type]
            brightness = min(1.0, brightness * adj["brightness_factor"])
            color_temp = max(1800, min(6500, color_temp + adj["warmth_offset"]))

        if warmth_score is not None:
            warmth_shift = int((warmth_score - 0.5) * -1000)
            color_temp = max(1800, min(6500, color_temp + warmth_shift))

        if energy_level is not None:
            brightness = min(1.0, brightness * (0.6 + energy_level * 0.5))

        transition = 2.0
        if mood == "sleepy":
            transition = 15.0
        elif mood == "refreshed":
            transition = 10.0
        elif mood in ("energetic", "focused"):
            transition = 1.0

        fixtures = []
        for f in profile.get("fixtures", []):
            fixtures.append({
                "name": f["name"],
                "type": f["type"],
                "brightness": min(1.0, f["brightness"] * (brightness / profile["brightness"]) if profile["brightness"] > 0 else 0),
                "color_temperature": color_temp,
                "color_hex": profile["color_hex"],
                "position": f.get("position", "general"),
            })

        zones = []
        for z in profile.get("zones", []):
            zones.append({
                "zone_name": z["zone_name"],
                "fixtures": [f for f in fixtures if True],
                "brightness": min(1.0, z["brightness"] * (brightness / profile["brightness"]) if profile["brightness"] > 0 else 0),
                "purpose": z["purpose"],
            })

        return {
            "color_temperature": color_temp,
            "brightness": round(brightness, 2),
            "color_hex": profile["color_hex"],
            "saturation": profile["saturation"],
            "description": profile["description"],
            "mood": mood,
            "time_of_day": time_of_day or "any",
            "fixtures": fixtures,
            "zones": zones,
            "transition_duration": transition,
            "ambiance_notes": profile["ambiance"],
        }

    def generate_alternatives(
        self, primary_mood: str, suggested_moods: list[str], **kwargs
    ) -> list[dict]:
        alternatives = []
        for alt_mood in suggested_moods[:3]:
            scene = self.generate_scene(mood=alt_mood, **kwargs)
            alternatives.append({
                "mood": alt_mood,
                "color_temperature": scene["color_temperature"],
                "brightness": scene["brightness"],
                "color_hex": scene["color_hex"],
                "description": scene["description"],
            })
        return alternatives


scene_generator = SceneGenerator()
