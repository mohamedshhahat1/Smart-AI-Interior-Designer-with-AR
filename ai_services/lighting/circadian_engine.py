from typing import Optional


class CircadianEngine:
    """Generates 24-hour lighting schedules aligned with human circadian rhythm."""

    DEFAULT_SCHEDULE_TEMPLATE = [
        {"time": "06:00", "phase": "pre_dawn",    "color_temp": 1800, "brightness": 0.02, "mood": "sleepy",    "label": "Night Mode"},
        {"time": "06:30", "phase": "dawn",         "color_temp": 2200, "brightness": 0.15, "mood": "sleepy",    "label": "Gentle Wake"},
        {"time": "07:00", "phase": "sunrise",      "color_temp": 3000, "brightness": 0.45, "mood": "refreshed", "label": "Sunrise Simulation"},
        {"time": "07:30", "phase": "early_morning", "color_temp": 4000, "brightness": 0.70, "mood": "refreshed", "label": "Morning Energize"},
        {"time": "09:00", "phase": "morning",      "color_temp": 5000, "brightness": 0.85, "mood": "focused",   "label": "Morning Focus"},
        {"time": "12:00", "phase": "midday",       "color_temp": 5500, "brightness": 0.95, "mood": "energetic", "label": "Peak Daylight"},
        {"time": "14:00", "phase": "afternoon",    "color_temp": 5000, "brightness": 0.85, "mood": "focused",   "label": "Afternoon Focus"},
        {"time": "16:00", "phase": "late_afternoon", "color_temp": 4500, "brightness": 0.75, "mood": "creative", "label": "Creative Hour"},
        {"time": "18:00", "phase": "golden_hour",  "color_temp": 3500, "brightness": 0.60, "mood": "social",    "label": "Golden Hour"},
        {"time": "19:30", "phase": "evening",      "color_temp": 3000, "brightness": 0.45, "mood": "relaxed",   "label": "Evening Wind-Down"},
        {"time": "21:00", "phase": "late_evening",  "color_temp": 2500, "brightness": 0.30, "mood": "cozy",      "label": "Cozy Evening"},
        {"time": "22:00", "phase": "pre_sleep",    "color_temp": 2000, "brightness": 0.15, "mood": "sleepy",    "label": "Sleep Preparation"},
        {"time": "23:00", "phase": "sleep",        "color_temp": 1800, "brightness": 0.03, "mood": "sleepy",    "label": "Sleep Mode"},
    ]

    def generate_schedule(
        self,
        wake_time: str = "07:00",
        sleep_time: str = "23:00",
        work_hours: Optional[list[str]] = None,
        preferences: Optional[dict] = None,
    ) -> dict:
        wake_minutes = self._time_to_minutes(wake_time)
        sleep_minutes = self._time_to_minutes(sleep_time)
        default_wake = self._time_to_minutes("07:00")
        offset = wake_minutes - default_wake

        schedule = []
        for entry in self.DEFAULT_SCHEDULE_TEMPLATE:
            entry_minutes = self._time_to_minutes(entry["time"])
            adjusted_minutes = entry_minutes + offset

            if adjusted_minutes < 0:
                adjusted_minutes += 1440
            elif adjusted_minutes >= 1440:
                adjusted_minutes -= 1440

            adjusted_time = self._minutes_to_time(adjusted_minutes)

            new_entry = entry.copy()
            new_entry["time"] = adjusted_time

            schedule.append(new_entry)

        if work_hours and len(work_hours) == 2:
            work_start = work_hours[0]
            work_end = work_hours[1]
            schedule = self._inject_work_period(schedule, work_start, work_end)

        if preferences:
            schedule = self._apply_preferences(schedule, preferences)

        schedule.sort(key=lambda x: self._time_to_minutes(x["time"]))

        energy_note = self._calculate_energy_savings(schedule)

        return {
            "schedule": schedule,
            "wake_time": wake_time,
            "sleep_time": sleep_time,
            "total_transitions": len(schedule),
            "energy_savings_estimate": energy_note,
        }

    def _inject_work_period(
        self, schedule: list[dict], work_start: str, work_end: str
    ) -> list[dict]:
        work_entries = [
            {
                "time": work_start,
                "phase": "work_start",
                "color_temp": 5000,
                "brightness": 0.85,
                "mood": "focused",
                "label": "Work Mode",
            },
            {
                "time": self._add_minutes(work_start, 120),
                "phase": "work_break",
                "color_temp": 4000,
                "brightness": 0.70,
                "mood": "refreshed",
                "label": "Break Refresh",
            },
            {
                "time": work_end,
                "phase": "work_end",
                "color_temp": 3500,
                "brightness": 0.60,
                "mood": "relaxed",
                "label": "Post-Work Transition",
            },
        ]

        work_start_min = self._time_to_minutes(work_start)
        work_end_min = self._time_to_minutes(work_end)

        filtered = [
            e for e in schedule
            if not (work_start_min <= self._time_to_minutes(e["time"]) <= work_end_min
                    and e["phase"] in ("morning", "midday", "afternoon", "late_afternoon"))
        ]

        return filtered + work_entries

    def _apply_preferences(self, schedule: list[dict], preferences: dict) -> list[dict]:
        brightness_factor = preferences.get("brightness_factor", 1.0)
        warmth_offset = preferences.get("warmth_offset", 0)

        adjusted = []
        for entry in schedule:
            new_entry = entry.copy()
            new_entry["brightness"] = min(1.0, max(0.01, entry["brightness"] * brightness_factor))
            new_entry["color_temp"] = max(1800, min(6500, entry["color_temp"] + warmth_offset))
            adjusted.append(new_entry)

        return adjusted

    def _calculate_energy_savings(self, schedule: list[dict]) -> str:
        avg_brightness = sum(e["brightness"] for e in schedule) / len(schedule)

        if avg_brightness < 0.4:
            return "High savings (~40-50%) — predominantly low-light schedule"
        elif avg_brightness < 0.6:
            return "Moderate savings (~20-30%) — balanced dim and bright periods"
        else:
            return "Standard consumption — schedule favors bright lighting"

    def _time_to_minutes(self, time_str: str) -> int:
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])

    def _minutes_to_time(self, minutes: int) -> str:
        hours = (minutes // 60) % 24
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def _add_minutes(self, time_str: str, add_min: int) -> str:
        total = self._time_to_minutes(time_str) + add_min
        return self._minutes_to_time(total)


circadian_engine = CircadianEngine()
