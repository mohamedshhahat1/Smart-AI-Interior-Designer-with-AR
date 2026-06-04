from typing import Optional


FURNITURE_BLOCKING_RISK = {
    "sofa": 0.3, "couch": 0.3, "bed": 0.4, "wardrobe": 0.5,
    "bookshelf": 0.4, "desk": 0.3, "dining table": 0.3,
    "tv_stand": 0.2, "cabinet": 0.4, "shelf": 0.3,
}

ROOM_CHI_RULES = {
    "bedroom": {
        "commanding_position": {
            "bed": "Position the bed so you can see the door without being directly in line with it",
        },
        "no_mirror_facing_bed": "Mirrors reflecting the bed disrupt sleep energy",
        "no_electronics": "Minimize electronics near the sleeping area",
        "pairs": "Use paired nightstands and lamps for relationship harmony",
    },
    "living_room": {
        "commanding_position": {
            "sofa": "Place the main sofa facing the entrance with a solid wall behind it",
        },
        "conversation_flow": "Arrange seating to encourage face-to-face conversation",
        "open_center": "Keep the center of the room open for chi circulation",
    },
    "office": {
        "commanding_position": {
            "desk": "Position your desk to face the door with a solid wall behind you",
        },
        "no_back_to_door": "Never sit with your back to the door — it creates vulnerability",
        "clear_desk": "A clear desk surface promotes clear thinking",
    },
    "kitchen": {
        "stove_visibility": "The cook should be able to see the kitchen entrance",
        "fire_water_separation": "Separate stove (fire) from sink (water) — they clash",
        "clean_surfaces": "Clean counters represent abundance and readiness",
    },
}


class ChiFlowAnalyzer:
    def analyze(
        self,
        room_type: str,
        detected_objects: Optional[list[dict]] = None,
        room_dimensions: Optional[dict] = None,
    ) -> dict:
        issues = []
        score = 7.0

        path_issues, path_score = self._analyze_pathways(detected_objects, room_dimensions)
        issues.extend(path_issues)
        score = min(score, path_score)

        cmd_issues, cmd_score = self._analyze_commanding_position(room_type, detected_objects)
        issues.extend(cmd_issues)

        rule_issues, rule_penalty = self._check_room_rules(room_type, detected_objects)
        issues.extend(rule_issues)

        clutter_issues, clutter_score = self._analyze_clutter(detected_objects)
        issues.extend(clutter_issues)

        door_issues = self._analyze_door_alignment(detected_objects)
        issues.extend(door_issues)

        final_chi_score = max(1.0, min(10.0, score - rule_penalty - len(door_issues) * 0.5))

        return {
            "chi_flow_score": round(final_chi_score, 1),
            "commanding_position_score": round(cmd_score, 1),
            "clutter_score": round(clutter_score, 1),
            "issues": issues,
        }

    def _analyze_pathways(
        self, detected_objects: Optional[list[dict]], room_dimensions: Optional[dict]
    ) -> tuple[list[dict], float]:
        issues = []
        score = 8.0

        if not detected_objects:
            return issues, score

        large_items = [
            obj for obj in detected_objects
            if isinstance(obj, dict) and FURNITURE_BLOCKING_RISK.get(obj.get("label", ""), 0) > 0.3
        ]

        if len(large_items) > 5:
            issues.append({
                "issue_type": "blocked_pathway",
                "severity": "high",
                "location": "general",
                "description": "Too many large furniture pieces may block natural chi flow through the room",
                "impact": "Stagnant energy, feeling of heaviness and congestion",
            })
            score -= 2.0

        if room_dimensions:
            area = room_dimensions.get("width", 4) * room_dimensions.get("depth", 4)
            item_density = len(detected_objects) / max(area, 1)
            if item_density > 0.8:
                issues.append({
                    "issue_type": "overcrowded",
                    "severity": "medium",
                    "location": "general",
                    "description": "Room density is high — insufficient space between furniture for chi to circulate",
                    "impact": "Restricted energy flow causing stress and restlessness",
                })
                score -= 1.5

        return issues, score

    def _analyze_commanding_position(
        self, room_type: str, detected_objects: Optional[list[dict]]
    ) -> tuple[list[dict], float]:
        issues = []
        score = 7.0

        rules = ROOM_CHI_RULES.get(room_type, {})
        cmd_rules = rules.get("commanding_position", {})

        if not detected_objects or not cmd_rules:
            return issues, score

        labels = {
            (obj.get("label", "") if isinstance(obj, dict) else str(obj)).lower()
            for obj in detected_objects
        }

        for furniture, advice in cmd_rules.items():
            if furniture in labels:
                score += 1.0
            else:
                issues.append({
                    "issue_type": "commanding_position",
                    "severity": "medium",
                    "location": furniture,
                    "description": f"Key furniture '{furniture}' not detected — verify commanding position: {advice}",
                    "impact": "Reduced sense of security and control in the space",
                })

        has_door = "door" in labels
        if not has_door:
            issues.append({
                "issue_type": "door_visibility",
                "severity": "low",
                "location": "entrance",
                "description": "Door not detected in the room scan — ensure main seating/bed can see the entrance",
                "impact": "Subconscious anxiety from not seeing who enters",
            })
            score -= 0.5

        return issues, min(10.0, max(1.0, score))

    def _check_room_rules(
        self, room_type: str, detected_objects: Optional[list[dict]]
    ) -> tuple[list[dict], float]:
        issues = []
        penalty = 0.0

        rules = ROOM_CHI_RULES.get(room_type, {})
        labels = set()

        if detected_objects:
            labels = {
                (obj.get("label", "") if isinstance(obj, dict) else str(obj)).lower()
                for obj in detected_objects
            }

        if room_type == "bedroom":
            if "mirror" in labels:
                issues.append({
                    "issue_type": "mirror_in_bedroom",
                    "severity": "medium",
                    "location": "bedroom",
                    "description": "Mirror detected in bedroom — if facing the bed, it disrupts sleep by bouncing energy",
                    "impact": "Restless sleep, amplified worries, disrupted intimacy",
                })
                penalty += 1.0

            if "tv" in labels or "laptop" in labels:
                issues.append({
                    "issue_type": "electronics_in_bedroom",
                    "severity": "low",
                    "location": "bedroom",
                    "description": "Electronics near sleeping area create active (yang) energy that conflicts with rest",
                    "impact": "Difficulty falling asleep, electromagnetic disturbance",
                })
                penalty += 0.5

        if room_type == "office" and "desk" in labels:
            pass

        if room_type == "kitchen":
            if "sink" in labels and "oven" in labels:
                issues.append({
                    "issue_type": "fire_water_clash",
                    "severity": "medium",
                    "location": "kitchen",
                    "description": "Stove (fire) and sink (water) are opposing elements — separate them or add wood element between",
                    "impact": "Arguments, financial instability, digestive issues",
                })
                penalty += 1.0

        return issues, penalty

    def _analyze_clutter(
        self, detected_objects: Optional[list[dict]]
    ) -> tuple[list[dict], float]:
        issues = []
        score = 8.0

        if not detected_objects:
            return issues, score

        object_count = len(detected_objects)

        if object_count > 12:
            issues.append({
                "issue_type": "clutter",
                "severity": "high",
                "location": "general",
                "description": f"High object density ({object_count} items) suggests clutter — chi cannot flow freely through cluttered spaces",
                "impact": "Mental fog, stuck energy, inability to move forward in life",
            })
            score = 4.0
        elif object_count > 8:
            issues.append({
                "issue_type": "moderate_clutter",
                "severity": "medium",
                "location": "general",
                "description": "Moderate object density — consider decluttering to improve energy flow",
                "impact": "Mild energy stagnation, reduced clarity",
            })
            score = 6.0

        return issues, score

    def _analyze_door_alignment(
        self, detected_objects: Optional[list[dict]]
    ) -> list[dict]:
        issues = []

        if not detected_objects:
            return issues

        doors = [
            obj for obj in detected_objects
            if isinstance(obj, dict) and obj.get("label", "").lower() == "door"
        ]
        windows = [
            obj for obj in detected_objects
            if isinstance(obj, dict) and obj.get("label", "").lower() == "window"
        ]

        if len(doors) >= 2:
            issues.append({
                "issue_type": "aligned_doors",
                "severity": "medium",
                "location": "doors",
                "description": "Multiple doors detected — if they align directly, chi rushes through without nourishing the room (sha chi)",
                "impact": "Energy drains out too quickly, instability",
            })

        if doors and windows:
            issues.append({
                "issue_type": "door_window_alignment",
                "severity": "low",
                "location": "entrance",
                "description": "Check if door and window are directly opposite — place furniture or a plant between to slow chi flow",
                "impact": "Chi rushes from door to window without circulating",
            })

        return issues


chi_flow_analyzer = ChiFlowAnalyzer()
