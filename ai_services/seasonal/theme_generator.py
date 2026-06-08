from typing import Optional

from ai_services.utils.llm_client import get_llm_response_sync, parse_llm_json, is_available


SEASONAL_THEMES = {
    "spring": {
        "name": "Fresh Spring Bloom",
        "description": "Light, airy design celebrating renewal with pastels, florals, and natural textures",
        "color_palette": {
            "primary": ["#F0FFF0", "#E8F5E9", "#FFF8E1"],
            "accent": ["#FF69B4", "#87CEEB", "#98FB98", "#DDA0DD"],
            "neutrals": ["#FFFFFF", "#FAF0E6", "#F5F5DC"],
        },
        "textures": ["light linen", "cotton", "sheer fabrics", "woven rattan", "fresh greenery"],
        "materials": ["light wood", "ceramic", "glass vases", "wicker baskets", "cotton throws"],
        "lighting_mood": "bright_natural",
        "music_mood": "uplifting acoustic",
        "scents": [
            {"scent": "Fresh cut flowers", "method": "bouquet", "placement": "dining table", "intensity": "medium"},
            {"scent": "Lavender", "method": "diffuser", "placement": "bedroom", "intensity": "light"},
            {"scent": "Lemon verbena", "method": "candle", "placement": "kitchen", "intensity": "medium"},
        ],
        "decor": [
            {"name": "Fresh flower arrangement", "category": "centerpiece", "placement": "dining table", "cost": 25, "reusable": False, "diy": True},
            {"name": "Pastel throw pillows", "category": "textiles", "placement": "sofa", "cost": 40, "reusable": True, "diy": False},
            {"name": "Bird motif wall art", "category": "wall_decor", "placement": "accent wall", "cost": 30, "reusable": True, "diy": True},
            {"name": "Potted herb garden", "category": "plants", "placement": "windowsill", "cost": 20, "reusable": True, "diy": True},
            {"name": "Sheer curtains", "category": "window", "placement": "windows", "cost": 35, "reusable": True, "diy": False},
            {"name": "Woven basket set", "category": "storage", "placement": "corners", "cost": 28, "reusable": True, "diy": False},
        ],
        "diy_projects": [
            {"name": "Pressed flower frame", "difficulty": "easy", "time": 45, "materials": ["picture frame", "pressed flowers", "contact paper"], "instructions": "Press flowers for 2 weeks, arrange on cardstock, seal with contact paper, frame", "cost": 12},
            {"name": "Macrame plant hanger", "difficulty": "medium", "time": 90, "materials": ["cotton rope", "wooden ring", "scissors"], "instructions": "Cut 8 cords of equal length, attach to ring, create spiral knots and gathering knots, add pot", "cost": 8},
        ],
    },
    "summer": {
        "name": "Vibrant Summer Paradise",
        "description": "Bold, bright design with tropical accents, cool textures, and breezy coastal vibes",
        "color_palette": {
            "primary": ["#FFFFFF", "#F0F8FF", "#FFFFF0"],
            "accent": ["#FF6347", "#00CED1", "#FFD700", "#FF7F50"],
            "neutrals": ["#FAF0E6", "#F5DEB3", "#FAEBD7"],
        },
        "textures": ["linen", "jute", "bamboo", "sisal", "light cotton"],
        "materials": ["rattan", "bamboo", "seagrass", "driftwood", "terracotta"],
        "lighting_mood": "bright_warm",
        "music_mood": "tropical chill",
        "scents": [
            {"scent": "Coconut & lime", "method": "candle", "placement": "living room", "intensity": "medium"},
            {"scent": "Ocean breeze", "method": "diffuser", "placement": "bedroom", "intensity": "light"},
            {"scent": "Fresh citrus", "method": "bowl of fruit", "placement": "kitchen counter", "intensity": "natural"},
        ],
        "decor": [
            {"name": "Tropical leaf prints", "category": "wall_decor", "placement": "accent wall", "cost": 35, "reusable": True, "diy": True},
            {"name": "Rattan floor mirror", "category": "mirror", "placement": "corner", "cost": 65, "reusable": True, "diy": False},
            {"name": "Coral & shell display", "category": "tabletop", "placement": "coffee table", "cost": 20, "reusable": True, "diy": True},
            {"name": "Striped outdoor cushions", "category": "textiles", "placement": "sofa/chairs", "cost": 45, "reusable": True, "diy": False},
            {"name": "Succulent arrangement", "category": "plants", "placement": "shelf", "cost": 22, "reusable": True, "diy": True},
        ],
        "diy_projects": [
            {"name": "Seashell wind chime", "difficulty": "easy", "time": 40, "materials": ["driftwood", "seashells", "fishing line", "drill"], "instructions": "Drill small holes in shells, tie to fishing line at varying lengths, attach lines to driftwood, hang", "cost": 10},
        ],
    },
    "autumn": {
        "name": "Warm Autumn Harvest",
        "description": "Rich, warm design with earthy tones, layered textures, and harvest-inspired accents",
        "color_palette": {
            "primary": ["#FFF8DC", "#FAEBD7", "#FAF0E6"],
            "accent": ["#D2691E", "#CD853F", "#8B4513", "#B22222", "#DAA520"],
            "neutrals": ["#F5DEB3", "#D2B48C", "#BC8F8F"],
        },
        "textures": ["chunky knit", "velvet", "leather", "burlap", "faux fur"],
        "materials": ["dark wood", "copper", "stone", "dried botanicals", "wool"],
        "lighting_mood": "warm_amber",
        "music_mood": "acoustic folk",
        "scents": [
            {"scent": "Cinnamon & apple", "method": "simmer pot", "placement": "kitchen", "intensity": "strong"},
            {"scent": "Pumpkin spice", "method": "candle", "placement": "living room", "intensity": "medium"},
            {"scent": "Cedarwood", "method": "diffuser", "placement": "bedroom", "intensity": "light"},
        ],
        "decor": [
            {"name": "Pumpkin & gourd display", "category": "centerpiece", "placement": "dining table", "cost": 15, "reusable": False, "diy": True},
            {"name": "Chunky knit throw blanket", "category": "textiles", "placement": "sofa arm", "cost": 55, "reusable": True, "diy": False},
            {"name": "Dried wheat bundle", "category": "accent", "placement": "vase by entrance", "cost": 12, "reusable": True, "diy": True},
            {"name": "Copper candle holders", "category": "lighting", "placement": "mantel/shelf", "cost": 30, "reusable": True, "diy": False},
            {"name": "Fall leaf garland", "category": "garland", "placement": "mantel/doorway", "cost": 18, "reusable": True, "diy": True},
            {"name": "Plaid accent pillows", "category": "textiles", "placement": "sofa", "cost": 35, "reusable": True, "diy": False},
        ],
        "diy_projects": [
            {"name": "Cinnamon stick candle wrap", "difficulty": "easy", "time": 20, "materials": ["pillar candle", "cinnamon sticks", "twine", "hot glue"], "instructions": "Apply hot glue to cinnamon sticks, press around candle, wrap twine twice and tie bow", "cost": 6},
            {"name": "Painted pumpkin centerpiece", "difficulty": "easy", "time": 30, "materials": ["mini pumpkins", "acrylic paint", "paintbrush", "sealant"], "instructions": "Clean pumpkins, apply base coat, add patterns (dots, stripes, metallics), seal", "cost": 10},
        ],
    },
    "winter": {
        "name": "Cozy Winter Wonderland",
        "description": "Intimate, hygge-inspired design with rich textures, warm lighting, and serene winter elegance",
        "color_palette": {
            "primary": ["#FFFAFA", "#F0F8FF", "#F5F5F5"],
            "accent": ["#1C3D5A", "#C0C0C0", "#B8860B", "#8B0000"],
            "neutrals": ["#D3D3D3", "#A9A9A9", "#696969"],
        },
        "textures": ["faux fur", "cashmere", "velvet", "heavy knit", "sheepskin"],
        "materials": ["dark wood", "marble", "brass", "crystal", "wool"],
        "lighting_mood": "warm_candlelight",
        "music_mood": "soft jazz & classical",
        "scents": [
            {"scent": "Pine & fir", "method": "wreath/branches", "placement": "entrance", "intensity": "natural"},
            {"scent": "Vanilla & amber", "method": "candle", "placement": "living room", "intensity": "medium"},
            {"scent": "Hot cocoa", "method": "simmer pot", "placement": "kitchen", "intensity": "strong"},
        ],
        "decor": [
            {"name": "Faux fur throw", "category": "textiles", "placement": "armchair", "cost": 60, "reusable": True, "diy": False},
            {"name": "Mercury glass candle holders", "category": "lighting", "placement": "mantel", "cost": 35, "reusable": True, "diy": False},
            {"name": "Pinecone & berry arrangement", "category": "centerpiece", "placement": "dining table", "cost": 18, "reusable": True, "diy": True},
            {"name": "Velvet accent pillows", "category": "textiles", "placement": "sofa", "cost": 42, "reusable": True, "diy": False},
            {"name": "White birch branch bundle", "category": "accent", "placement": "corner vase", "cost": 15, "reusable": True, "diy": True},
            {"name": "Knit candle wraps", "category": "lighting", "placement": "shelf/table", "cost": 12, "reusable": True, "diy": True},
        ],
        "diy_projects": [
            {"name": "Winter terrarium", "difficulty": "medium", "time": 60, "materials": ["glass jar", "mini evergreen clippings", "fake snow", "small figurines", "twine"], "instructions": "Layer fake snow in jar, arrange clippings and figurines, close and decorate lid with twine", "cost": 15},
        ],
    },
}

HOLIDAY_THEMES = {
    "christmas": {
        "name": "Classic Christmas Celebration",
        "description": "Festive red & green with twinkling lights, evergreen accents, and holiday warmth",
        "color_palette": {"primary": ["#FFFAFA", "#F5F5DC"], "accent": ["#C41E3A", "#228B22", "#FFD700", "#B22222"], "neutrals": ["#F5F5F5", "#D4AF37"]},
        "textures": ["velvet", "plaid", "knit", "faux fur", "satin ribbon"],
        "materials": ["evergreen branches", "pinecones", "cinnamon sticks", "glass ornaments", "candles"],
        "lighting_mood": "twinkling_warm",
        "music_mood": "christmas classics",
        "scents": [
            {"scent": "Fresh pine", "method": "real tree/wreath", "placement": "living room", "intensity": "strong"},
            {"scent": "Gingerbread", "method": "baking/candle", "placement": "kitchen", "intensity": "medium"},
        ],
        "decor": [
            {"name": "Christmas tree", "category": "focal_point", "placement": "corner by window", "cost": 80, "reusable": True, "diy": False},
            {"name": "Evergreen wreath", "category": "door_decor", "placement": "front door", "cost": 35, "reusable": True, "diy": True},
            {"name": "String lights", "category": "lighting", "placement": "mantel/windows", "cost": 20, "reusable": True, "diy": False},
            {"name": "Stocking display", "category": "traditional", "placement": "mantel", "cost": 30, "reusable": True, "diy": True},
            {"name": "Advent candle set", "category": "lighting", "placement": "dining table", "cost": 25, "reusable": True, "diy": False},
        ],
        "diy_projects": [
            {"name": "DIY advent calendar", "difficulty": "medium", "time": 120, "materials": ["small bags/boxes", "twine", "number stickers", "branch", "mini treats"], "instructions": "Number 24 bags, fill with treats, hang on branch display with twine", "cost": 20},
        ],
    },
    "halloween": {
        "name": "Enchanted Halloween",
        "description": "Spooky-elegant design with moody purples, flickering candles, and gothic charm",
        "color_palette": {"primary": ["#1A1A2E", "#16213E"], "accent": ["#FF6600", "#800080", "#006400", "#FF0000"], "neutrals": ["#2C2C2C", "#696969"]},
        "textures": ["black lace", "velvet", "cobweb fabric", "burlap"],
        "materials": ["black candles", "vintage frames", "dried branches", "mercury glass"],
        "lighting_mood": "dramatic_dim",
        "music_mood": "eerie ambient",
        "scents": [{"scent": "Smoked pumpkin", "method": "candle", "placement": "entry", "intensity": "medium"}],
        "decor": [
            {"name": "Carved pumpkins", "category": "focal_point", "placement": "porch/entrance", "cost": 15, "reusable": False, "diy": True},
            {"name": "Vintage apothecary jars", "category": "tabletop", "placement": "shelf/mantel", "cost": 25, "reusable": True, "diy": True},
            {"name": "Black pillar candle cluster", "category": "lighting", "placement": "dining table", "cost": 20, "reusable": True, "diy": False},
            {"name": "Bat wall decals", "category": "wall_decor", "placement": "stairway/entry wall", "cost": 8, "reusable": True, "diy": True},
        ],
        "diy_projects": [
            {"name": "Floating candle display", "difficulty": "easy", "time": 30, "materials": ["paper towel tubes", "hot glue", "LED tea lights", "white paint"], "instructions": "Cut tubes to varying heights, drip hot glue around top edges, paint white, insert LED candles, hang from ceiling with fishing line", "cost": 8},
        ],
    },
    "eid": {
        "name": "Elegant Eid Celebration",
        "description": "Luxurious design with gold, jewel tones, intricate patterns, and warm hospitality",
        "color_palette": {"primary": ["#FFFFF0", "#FFF8DC"], "accent": ["#DAA520", "#006400", "#4169E1", "#800080"], "neutrals": ["#F5F5DC", "#D2B48C"]},
        "textures": ["silk", "brocade", "embroidered fabric", "brass inlay"],
        "materials": ["brass lanterns", "rose petals", "date bowls", "prayer beads", "calligraphy art"],
        "lighting_mood": "golden_warm",
        "music_mood": "traditional nasheeds",
        "scents": [
            {"scent": "Oud & rose", "method": "bukhoor/incense", "placement": "living room", "intensity": "medium"},
            {"scent": "Jasmine", "method": "fresh flowers", "placement": "dining table", "intensity": "natural"},
        ],
        "decor": [
            {"name": "Brass lanterns with candles", "category": "lighting", "placement": "entrance & table", "cost": 40, "reusable": True, "diy": False},
            {"name": "Calligraphy wall art", "category": "wall_decor", "placement": "accent wall", "cost": 35, "reusable": True, "diy": False},
            {"name": "Date & sweet display", "category": "hospitality", "placement": "coffee table", "cost": 20, "reusable": False, "diy": True},
            {"name": "Jewel-tone cushion covers", "category": "textiles", "placement": "floor/sofa", "cost": 45, "reusable": True, "diy": False},
            {"name": "Crescent moon garland", "category": "garland", "placement": "wall/doorway", "cost": 15, "reusable": True, "diy": True},
        ],
        "diy_projects": [
            {"name": "Henna-pattern painted tray", "difficulty": "medium", "time": 60, "materials": ["wooden tray", "gold paint pen", "sealant"], "instructions": "Sketch henna-inspired patterns on tray, trace with gold paint pen, let dry 24h, apply sealant", "cost": 12},
        ],
    },
    "diwali": {
        "name": "Radiant Diwali Festival of Lights",
        "description": "Vibrant design celebrating light over darkness with diyas, rangoli patterns, and marigolds",
        "color_palette": {"primary": ["#FFF8DC", "#FFFFF0"], "accent": ["#FF6600", "#FF1493", "#FFD700", "#8B0000"], "neutrals": ["#F5DEB3", "#DAA520"]},
        "textures": ["silk", "brocade", "metallic thread", "mirror work"],
        "materials": ["clay diyas", "marigold garlands", "rangoli powder", "brass items", "silk fabrics"],
        "lighting_mood": "golden_festive",
        "music_mood": "bollywood festive",
        "scents": [{"scent": "Sandalwood & jasmine", "method": "incense & flowers", "placement": "throughout", "intensity": "strong"}],
        "decor": [
            {"name": "Diya arrangement", "category": "lighting", "placement": "entrance & windowsills", "cost": 15, "reusable": True, "diy": True},
            {"name": "Marigold garland", "category": "garland", "placement": "doorways", "cost": 10, "reusable": False, "diy": True},
            {"name": "Rangoli stencil design", "category": "floor_art", "placement": "entrance floor", "cost": 8, "reusable": True, "diy": True},
            {"name": "Brass Ganesh statue", "category": "spiritual", "placement": "altar/shelf", "cost": 30, "reusable": True, "diy": False},
        ],
        "diy_projects": [
            {"name": "Painted clay diyas", "difficulty": "easy", "time": 45, "materials": ["plain clay diyas", "acrylic paint", "glitter", "wicks", "oil"], "instructions": "Paint diyas with bright colors, add dots and patterns, apply glitter accents, let dry, add wick and oil", "cost": 8},
        ],
    },
    "valentines": {
        "name": "Romantic Valentine's Retreat",
        "description": "Intimate, romantic ambiance with roses, soft pinks, candlelight, and luxurious textures",
        "color_palette": {"primary": ["#FFF0F5", "#FFFFF0"], "accent": ["#FF69B4", "#DC143C", "#FFB6C1", "#DAA520"], "neutrals": ["#FAF0E6", "#F5F5DC"]},
        "textures": ["velvet", "silk", "satin", "faux fur"],
        "materials": ["roses", "candles", "glass", "gold accents"],
        "lighting_mood": "intimate_candlelight",
        "music_mood": "romantic jazz",
        "scents": [{"scent": "Rose & vanilla", "method": "candle", "placement": "bedroom/dining", "intensity": "medium"}],
        "decor": [
            {"name": "Rose petal scatter", "category": "ambiance", "placement": "table/pathway", "cost": 12, "reusable": False, "diy": True},
            {"name": "Pillar candle cluster", "category": "lighting", "placement": "dining table", "cost": 25, "reusable": True, "diy": False},
            {"name": "Heart garland", "category": "garland", "placement": "mantel/doorway", "cost": 10, "reusable": True, "diy": True},
        ],
        "diy_projects": [
            {"name": "Paper heart garland", "difficulty": "easy", "time": 30, "materials": ["cardstock", "twine", "hole punch", "scissors"], "instructions": "Cut hearts from cardstock in varying sizes, punch holes, thread onto twine, hang", "cost": 5},
        ],
    },
    "thanksgiving": {
        "name": "Grateful Harvest Gathering",
        "description": "Warm, abundant design celebrating gratitude with harvest elements and earth tones",
        "color_palette": {"primary": ["#FFF8DC", "#FAEBD7"], "accent": ["#D2691E", "#DAA520", "#8B4513", "#B22222"], "neutrals": ["#F5DEB3", "#D2B48C"]},
        "textures": ["burlap", "linen", "plaid flannel", "raw cotton"],
        "materials": ["gourds", "dried corn", "wheat stalks", "wooden platters", "copper"],
        "lighting_mood": "warm_ambient",
        "music_mood": "folk & americana",
        "scents": [{"scent": "Apple cider & cinnamon", "method": "simmer pot", "placement": "kitchen", "intensity": "strong"}],
        "decor": [
            {"name": "Cornucopia centerpiece", "category": "centerpiece", "placement": "dining table", "cost": 25, "reusable": True, "diy": True},
            {"name": "Gratitude chalkboard sign", "category": "wall_decor", "placement": "dining room wall", "cost": 15, "reusable": True, "diy": True},
            {"name": "Harvest table runner", "category": "textiles", "placement": "dining table", "cost": 22, "reusable": True, "diy": False},
        ],
        "diy_projects": [
            {"name": "Thankful leaf tree", "difficulty": "easy", "time": 40, "materials": ["branches", "vase", "paper leaves", "pens", "twine"], "instructions": "Arrange branches in vase, cut leaf shapes, write gratitude notes on each, tie to branches", "cost": 7},
        ],
    },
}

BUDGET_MULTIPLIERS = {"budget": 0.5, "medium": 1.0, "premium": 2.0}


class ThemeGenerator:
    def generate(
        self,
        theme_type: str,
        season: Optional[str] = None,
        holiday: Optional[str] = None,
        room_type: str = "living_room",
        budget_tier: str = "medium",
        intensity: float = 0.7,
        base_style: Optional[str] = None,
        include_diy: bool = True,
        include_scents: bool = True,
    ) -> dict:
        if theme_type == "holiday" and holiday:
            source = HOLIDAY_THEMES.get(holiday, HOLIDAY_THEMES.get("christmas"))
        elif theme_type == "season" and season:
            source = SEASONAL_THEMES.get(season, SEASONAL_THEMES.get("spring"))
        else:
            source = SEASONAL_THEMES.get("spring")

        budget_mult = BUDGET_MULTIPLIERS.get(budget_tier, 1.0)

        style_filter = self._get_style_categories(base_style) if base_style else None

        decor_items = []
        for d in source.get("decor", []):
            if style_filter and d["category"] not in style_filter:
                continue
            item = {
                "name": d["name"],
                "category": d["category"],
                "placement": d["placement"],
                "estimated_cost": round(d.get("cost", 0) * budget_mult, 2),
                "reusable": d.get("reusable", True),
                "diy_possible": d.get("diy", False),
            }
            decor_items.append(item)

        if not decor_items:
            for d in source.get("decor", []):
                decor_items.append({
                    "name": d["name"],
                    "category": d["category"],
                    "placement": d["placement"],
                    "estimated_cost": round(d.get("cost", 0) * budget_mult, 2),
                    "reusable": d.get("reusable", True),
                    "diy_possible": d.get("diy", False),
                })

        if intensity < 0.5:
            decor_items = [d for d in decor_items if d["reusable"]][:3]

        diy_projects = []
        if include_diy:
            for p in source.get("diy_projects", []):
                diy_projects.append({
                    "name": p["name"],
                    "difficulty": p["difficulty"],
                    "time_minutes": p["time"],
                    "materials": p["materials"],
                    "instructions": p["instructions"],
                    "estimated_cost": round(p["cost"] * budget_mult, 2),
                })

        scent_recs = []
        if include_scents:
            scent_recs = source.get("scents", [])

        total_cost = sum(d["estimated_cost"] for d in decor_items)
        total_cost += sum(p["estimated_cost"] for p in diy_projects)

        reusable_count = sum(1 for d in decor_items if d["reusable"])
        reusability = reusable_count / len(decor_items) if decor_items else 0.0

        theme_name = source["name"]
        theme_description = source["description"]

        if is_available():
            context = holiday or season or "seasonal"
            style_note = f" in a {base_style} style" if base_style else ""
            prompt = (
                f"Create a short theme name (3-5 words) and one-sentence description for a "
                f"{context}{style_note} interior design theme for a {room_type}.\n"
                f"Return JSON: {{\"name\": \"...\", \"description\": \"...\"}}"
            )
            raw = get_llm_response_sync([{"role": "user", "content": prompt}], max_tokens=150)
            data = parse_llm_json(raw)
            if data and data.get("name") and data.get("description"):
                theme_name = data["name"]
                theme_description = data["description"]

        return {
            "name": theme_name,
            "description": theme_description,
            "theme_type": theme_type,
            "season": season,
            "holiday": holiday,
            "color_palette": source["color_palette"],
            "textures": source.get("textures", []),
            "materials": source.get("materials", []),
            "lighting_mood": source.get("lighting_mood", "warm_ambient"),
            "decor_items": decor_items,
            "diy_projects": diy_projects,
            "scent_recommendations": scent_recs,
            "music_playlist_mood": source.get("music_mood", "seasonal"),
            "budget_tier": budget_tier,
            "estimated_cost": round(total_cost, 2),
            "reusability_score": round(reusability, 2),
        }

    def _get_style_categories(self, base_style: str) -> set[str]:
        style_map = {
            "minimalist": {"textiles", "lighting", "plants"},
            "modern": {"textiles", "lighting", "wall_decor", "mirror", "plants"},
            "traditional": {"centerpiece", "textiles", "lighting", "garland", "wall_decor"},
            "rustic": {"centerpiece", "textiles", "accent", "garland", "storage"},
            "bohemian": {"textiles", "plants", "wall_decor", "garland", "tabletop"},
            "scandinavian": {"textiles", "lighting", "plants", "storage"},
        }
        cats = style_map.get(base_style.lower())
        if cats:
            return cats
        return {"centerpiece", "textiles", "lighting", "wall_decor", "plants",
                "garland", "accent", "mirror", "tabletop", "storage",
                "focal_point", "door_decor", "traditional", "window",
                "hospitality", "spiritual", "floor_art", "ambiance"}

    def generate_transition(
        self,
        from_theme: Optional[dict],
        to_season: Optional[str] = None,
        to_holiday: Optional[str] = None,
        gradual: bool = True,
    ) -> dict:
        to_type = "holiday" if to_holiday else "season"
        to_data = self.generate(theme_type=to_type, season=to_season, holiday=to_holiday)

        from_items = set()
        if from_theme and from_theme.get("decor_items"):
            from_items = {d["name"] for d in from_theme["decor_items"]}

        to_items = {d["name"] for d in to_data.get("decor_items", [])}

        keep = list(from_items & to_items)
        add = list(to_items - from_items)
        remove = list(from_items - to_items)

        steps = []
        if gradual:
            steps = [
                {"step": 1, "action": "Remove holiday-specific items first", "timing": "Day 1"},
                {"step": 2, "action": "Swap textiles (pillows, throws, curtains)", "timing": "Day 2-3"},
                {"step": 3, "action": "Update color accents and small decor", "timing": "Day 4-5"},
                {"step": 4, "action": "Add new seasonal centerpieces and focal items", "timing": "Day 6-7"},
                {"step": 5, "action": "Adjust lighting mood and scents", "timing": "Day 7"},
            ]
        else:
            steps = [
                {"step": 1, "action": "Remove all previous seasonal decor", "timing": "Day 1"},
                {"step": 2, "action": "Set up new theme completely", "timing": "Day 1"},
            ]

        add_cost = sum(d.get("estimated_cost", 0) for d in to_data.get("decor_items", []) if d["name"] in add)
        effort = "minimal" if len(add) <= 3 else "moderate" if len(add) <= 6 else "significant"

        return {
            "from_theme": from_theme.get("name") if from_theme else None,
            "to_theme": to_data["name"],
            "transition_steps": steps,
            "items_to_keep": keep,
            "items_to_add": add,
            "items_to_remove": remove,
            "estimated_effort": effort,
            "estimated_cost": round(add_cost, 2),
        }


theme_generator = ThemeGenerator()
