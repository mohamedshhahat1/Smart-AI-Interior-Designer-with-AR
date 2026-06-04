from typing import Optional


MOOD_KEYWORDS = {
    "relaxed": {
        "keywords": ["relax", "calm", "unwind", "peaceful", "zen", "chill", "rest", "serene", "tranquil", "meditat"],
        "energy": 0.25,
        "warmth": 0.75,
    },
    "focused": {
        "keywords": ["focus", "work", "study", "concentrat", "productive", "task", "deadline", "code", "write", "read"],
        "energy": 0.65,
        "warmth": 0.35,
    },
    "energetic": {
        "keywords": ["energy", "excit", "party", "danc", "workout", "exercise", "pump", "morning", "awake", "active"],
        "energy": 0.90,
        "warmth": 0.40,
    },
    "romantic": {
        "keywords": ["romantic", "date", "dinner", "intimate", "candle", "love", "cozy evening", "wine", "together"],
        "energy": 0.20,
        "warmth": 0.85,
    },
    "cozy": {
        "keywords": ["cozy", "warm", "comfort", "hygge", "snuggle", "blanket", "fireplace", "winter", "tea", "book"],
        "energy": 0.20,
        "warmth": 0.90,
    },
    "creative": {
        "keywords": ["creat", "inspir", "art", "paint", "design", "imagin", "brainstorm", "idea", "music", "craft"],
        "energy": 0.55,
        "warmth": 0.50,
    },
    "social": {
        "keywords": ["friend", "gather", "host", "party", "entertain", "game night", "convers", "guest", "celebrat"],
        "energy": 0.70,
        "warmth": 0.60,
    },
    "sleepy": {
        "keywords": ["sleep", "bed", "night", "tired", "drowsy", "wind down", "melatonin", "dream", "rest"],
        "energy": 0.05,
        "warmth": 0.80,
    },
    "refreshed": {
        "keywords": ["refresh", "morning", "sunrise", "wake", "bright", "new day", "start", "clean", "fresh"],
        "energy": 0.75,
        "warmth": 0.30,
    },
    "melancholic": {
        "keywords": ["sad", "melanchol", "quiet", "reflect", "contemplat", "rain", "alone", "think", "nostalg"],
        "energy": 0.15,
        "warmth": 0.65,
    },
}

ACTIVITY_MOOD_MAP = {
    "relaxing": "relaxed",
    "working": "focused",
    "studying": "focused",
    "entertaining": "social",
    "sleeping": "sleepy",
    "cooking": "energetic",
    "reading": "cozy",
    "exercising": "energetic",
    "meditating": "relaxed",
    "dining": "romantic",
    "creating": "creative",
    "gaming": "social",
}

TIME_MOOD_WEIGHTS = {
    "morning": {"refreshed": 0.3, "energetic": 0.2, "focused": 0.2},
    "afternoon": {"focused": 0.3, "creative": 0.2, "energetic": 0.1},
    "evening": {"relaxed": 0.3, "cozy": 0.2, "social": 0.2},
    "night": {"sleepy": 0.3, "relaxed": 0.2, "romantic": 0.15},
}


class MoodAnalyzer:
    def analyze(
        self,
        text_input: Optional[str] = None,
        time_of_day: Optional[str] = None,
        activity: Optional[str] = None,
        energy_level: Optional[float] = None,
    ) -> dict:
        scores = {mood: 0.0 for mood in MOOD_KEYWORDS}

        if text_input:
            text_lower = text_input.lower()
            for mood, config in MOOD_KEYWORDS.items():
                for keyword in config["keywords"]:
                    if keyword in text_lower:
                        scores[mood] += 0.3

        if activity:
            mapped = ACTIVITY_MOOD_MAP.get(activity.lower())
            if mapped and mapped in scores:
                scores[mapped] += 0.35

        if time_of_day and time_of_day in TIME_MOOD_WEIGHTS:
            for mood, weight in TIME_MOOD_WEIGHTS[time_of_day].items():
                scores[mood] += weight

        if energy_level is not None:
            for mood, config in MOOD_KEYWORDS.items():
                mood_energy = config["energy"]
                distance = abs(mood_energy - energy_level)
                scores[mood] += max(0, 0.2 - distance * 0.3)

        if max(scores.values()) == 0:
            if time_of_day in ("evening", "night"):
                scores["relaxed"] = 0.5
            elif time_of_day == "morning":
                scores["refreshed"] = 0.5
            else:
                scores["focused"] = 0.5

        total = sum(scores.values())
        if total > 0:
            scores = {k: v / total for k, v in scores.items()}

        detected_mood = max(scores, key=scores.get)
        confidence = scores[detected_mood]

        mood_config = MOOD_KEYWORDS[detected_mood]

        sorted_moods = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        suggested = [m for m, s in sorted_moods[1:4] if s > 0.05]

        source_parts = []
        if text_input:
            source_parts.append("text")
        if activity:
            source_parts.append("activity")
        if time_of_day:
            source_parts.append("time")
        if energy_level is not None:
            source_parts.append("energy")

        return {
            "detected_mood": detected_mood,
            "confidence": round(min(confidence * 2.5, 0.99), 2),
            "energy_level": energy_level if energy_level is not None else mood_config["energy"],
            "warmth_score": mood_config["warmth"],
            "suggested_moods": suggested,
            "analysis_source": "+".join(source_parts) if source_parts else "default",
            "all_scores": {k: round(v, 3) for k, v in sorted_moods[:5]},
        }


mood_analyzer = MoodAnalyzer()
