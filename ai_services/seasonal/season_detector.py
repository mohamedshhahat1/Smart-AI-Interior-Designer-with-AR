from datetime import date, timedelta
from typing import Optional


SEASON_DATES_NORTHERN = {
    "spring": (3, 20, 6, 20),
    "summer": (6, 21, 9, 21),
    "autumn": (9, 22, 12, 20),
    "winter": (12, 21, 3, 19),
}

SEASON_DATES_SOUTHERN = {
    "autumn": (3, 20, 6, 20),
    "winter": (6, 21, 9, 21),
    "spring": (9, 22, 12, 20),
    "summer": (12, 21, 3, 19),
}

SEASON_ORDER = ["spring", "summer", "autumn", "winter"]

SEASONAL_MOODS = {
    "spring": "refreshing, renewal, optimistic, light",
    "summer": "vibrant, energetic, bright, joyful",
    "autumn": "cozy, warm, rustic, harvest",
    "winter": "intimate, serene, festive, hygge",
}

HOLIDAYS_CALENDAR = [
    {"name": "new_year", "display": "New Year", "month": 1, "day": 1, "duration": 3, "region": "global"},
    {"name": "lunar_new_year", "display": "Lunar New Year", "month": 1, "day": 29, "duration": 15, "region": "east_asia"},
    {"name": "valentines", "display": "Valentine's Day", "month": 2, "day": 14, "duration": 7, "region": "global"},
    {"name": "ramadan", "display": "Ramadan", "month": 3, "day": 1, "duration": 30, "region": "islamic"},
    {"name": "easter", "display": "Easter", "month": 4, "day": 20, "duration": 7, "region": "western"},
    {"name": "eid", "display": "Eid al-Fitr", "month": 4, "day": 1, "duration": 3, "region": "islamic"},
    {"name": "mothers_day", "display": "Mother's Day", "month": 5, "day": 11, "duration": 3, "region": "western"},
    {"name": "independence_day", "display": "Independence Day", "month": 7, "day": 4, "duration": 3, "region": "us"},
    {"name": "diwali", "display": "Diwali", "month": 10, "day": 20, "duration": 5, "region": "south_asia"},
    {"name": "halloween", "display": "Halloween", "month": 10, "day": 31, "duration": 14, "region": "western"},
    {"name": "thanksgiving", "display": "Thanksgiving", "month": 11, "day": 27, "duration": 5, "region": "us"},
    {"name": "hanukkah", "display": "Hanukkah", "month": 12, "day": 14, "duration": 8, "region": "jewish"},
    {"name": "christmas", "display": "Christmas", "month": 12, "day": 25, "duration": 14, "region": "global"},
]


class SeasonDetector:
    def detect(
        self,
        hemisphere: str = "northern",
        target_date: Optional[date] = None,
        days_ahead: int = 30,
    ) -> dict:
        today = target_date or date.today()
        current_season = self._get_season(today, hemisphere)
        next_season = SEASON_ORDER[(SEASON_ORDER.index(current_season) + 1) % 4]

        days_into = self._days_into_season(today, current_season, hemisphere)
        days_until = self._days_until_next_season(today, current_season, hemisphere)

        upcoming = self._get_upcoming_holidays(today, days_ahead)

        recommended = current_season
        if upcoming and self._days_until_holiday(today, upcoming[0]) <= 14:
            recommended = upcoming[0]["name"]

        return {
            "current_season": current_season,
            "hemisphere": hemisphere,
            "days_into_season": days_into,
            "days_until_next_season": days_until,
            "next_season": next_season,
            "upcoming_holidays": [
                {
                    "name": h["name"],
                    "display_name": h["display"],
                    "days_until": self._days_until_holiday(today, h),
                    "region": h["region"],
                }
                for h in upcoming
            ],
            "recommended_theme": recommended,
            "seasonal_mood": SEASONAL_MOODS.get(current_season, "balanced"),
        }

    def _get_season(self, d: date, hemisphere: str) -> str:
        table = SEASON_DATES_NORTHERN if hemisphere == "northern" else SEASON_DATES_SOUTHERN
        month, day = d.month, d.day

        for season, (sm, sd, em, ed) in table.items():
            if season == "winter" and hemisphere == "northern":
                if (month == 12 and day >= 21) or (month <= 3 and day <= 19):
                    return "winter"
            elif season == "summer" and hemisphere == "southern":
                if (month == 12 and day >= 21) or (month <= 3 and day <= 19):
                    return "summer"
            else:
                start = date(d.year, sm, sd)
                end = date(d.year, em, ed)
                if start <= d <= end:
                    return season

        return "winter" if hemisphere == "northern" else "summer"

    def _days_into_season(self, d: date, season: str, hemisphere: str) -> int:
        table = SEASON_DATES_NORTHERN if hemisphere == "northern" else SEASON_DATES_SOUTHERN
        if season in table:
            sm, sd = table[season][0], table[season][1]
            start = date(d.year, sm, sd)
            if start > d:
                start = date(d.year - 1, sm, sd)
            return (d - start).days
        return 0

    def _days_until_next_season(self, d: date, season: str, hemisphere: str) -> int:
        table = SEASON_DATES_NORTHERN if hemisphere == "northern" else SEASON_DATES_SOUTHERN
        if season in table:
            em, ed = table[season][2], table[season][3]
            end = date(d.year, em, ed)
            if end < d:
                end = date(d.year + 1, em, ed)
            return (end - d).days
        return 0

    def _get_upcoming_holidays(self, d: date, days_ahead: int) -> list[dict]:
        upcoming = []
        cutoff = d + timedelta(days=days_ahead)

        for h in HOLIDAYS_CALENDAR:
            h_date = date(d.year, h["month"], min(h["day"], 28))
            if h_date < d:
                h_date = date(d.year + 1, h["month"], min(h["day"], 28))
            if d <= h_date <= cutoff:
                upcoming.append(h)

        upcoming.sort(key=lambda x: date(d.year, x["month"], min(x["day"], 28)))
        return upcoming

    def _days_until_holiday(self, d: date, h: dict) -> int:
        h_date = date(d.year, h["month"], min(h["day"], 28))
        if h_date < d:
            h_date = date(d.year + 1, h["month"], min(h["day"], 28))
        return (h_date - d).days


season_detector = SeasonDetector()
