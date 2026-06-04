from typing import Optional


class SmartHomeExporter:
    """Exports lighting scenes to smart home platform configurations."""

    def export(self, scene: dict, platform: str) -> dict:
        exporters = {
            "philips_hue": self._export_philips_hue,
            "lifx": self._export_lifx,
            "homekit": self._export_homekit,
            "google_home": self._export_google_home,
            "alexa": self._export_alexa,
        }

        exporter = exporters.get(platform)
        if not exporter:
            return {
                "platform": platform,
                "config": {},
                "instructions": [f"Platform '{platform}' is not yet supported"],
                "compatible_devices": [],
            }

        return exporter(scene)

    def _export_philips_hue(self, scene: dict) -> dict:
        hue_value, sat_value = self._kelvin_to_hue_ct(scene.get("color_temperature", 3000))
        bri = int(scene.get("brightness", 0.5) * 254)

        lights = []
        for i, fixture in enumerate(scene.get("fixtures", []), 1):
            lights.append({
                "light_id": i,
                "name": fixture.get("name", f"Light {i}"),
                "state": {
                    "on": True,
                    "bri": int(fixture.get("brightness", 0.5) * 254),
                    "ct": hue_value,
                    "transitiontime": int(scene.get("transition_duration", 2) * 10),
                },
            })

        return {
            "platform": "philips_hue",
            "config": {
                "name": scene.get("mood", "Custom Scene"),
                "type": "LightScene",
                "group": "0",
                "lights": lights,
                "recycle": False,
            },
            "instructions": [
                "1. Open the Philips Hue app → Scenes → Create Scene",
                "2. Select the room/zone for this scene",
                "3. Set each light to the values shown above",
                f"4. Set transition time to {scene.get('transition_duration', 2):.0f} seconds",
                "5. Save the scene with the mood name",
            ],
            "compatible_devices": [
                "Philips Hue White Ambiance",
                "Philips Hue White and Color",
                "Philips Hue Go",
                "Philips Hue Lightstrip Plus",
                "Philips Hue Bloom",
            ],
        }

    def _export_lifx(self, scene: dict) -> dict:
        brightness = scene.get("brightness", 0.5)
        kelvin = scene.get("color_temperature", 3000)
        color_hex = scene.get("color_hex", "#FFFFFF")

        effects = []
        for fixture in scene.get("fixtures", []):
            effects.append({
                "selector": f"label:{fixture.get('name', 'Light')}",
                "power": "on",
                "brightness": fixture.get("brightness", brightness),
                "color": f"kelvin:{kelvin}",
                "duration": scene.get("transition_duration", 2),
            })

        return {
            "platform": "lifx",
            "config": {
                "scene_name": scene.get("mood", "Custom"),
                "effects": effects,
                "duration": scene.get("transition_duration", 2),
            },
            "instructions": [
                "1. Open LIFX app → Scenes → Create New",
                "2. Add all lights in the room",
                f"3. Set color temperature to {kelvin}K",
                f"4. Set brightness to {int(brightness * 100)}%",
                f"5. Set transition to {scene.get('transition_duration', 2):.0f}s",
            ],
            "compatible_devices": [
                "LIFX A19",
                "LIFX Mini",
                "LIFX Z Strip",
                "LIFX Beam",
                "LIFX Tile",
            ],
        }

    def _export_homekit(self, scene: dict) -> dict:
        accessories = []
        for fixture in scene.get("fixtures", []):
            accessories.append({
                "name": fixture.get("name", "Light"),
                "characteristics": {
                    "On": True,
                    "Brightness": int(fixture.get("brightness", 0.5) * 100),
                    "ColorTemperature": self._kelvin_to_mired(scene.get("color_temperature", 3000)),
                },
            })

        return {
            "platform": "homekit",
            "config": {
                "scene_name": scene.get("mood", "Custom"),
                "accessories": accessories,
            },
            "instructions": [
                "1. Open Home app → + → Add Scene",
                f"2. Name: '{scene.get('mood', 'Custom')} Lighting'",
                "3. Select room and add light accessories",
                "4. Configure each light per the settings above",
                "5. Optionally add to a Siri shortcut for voice control",
            ],
            "compatible_devices": [
                "Any HomeKit-compatible smart bulb",
                "Eve Light Strip",
                "Nanoleaf Essentials",
                "IKEA TRADFRI",
            ],
        }

    def _export_google_home(self, scene: dict) -> dict:
        return {
            "platform": "google_home",
            "config": {
                "routine_name": f"{scene.get('mood', 'Custom')} Lighting",
                "actions": [
                    {
                        "type": "device.command",
                        "command": "action.devices.commands.ColorAbsoluteTemperature",
                        "params": {"color": {"temperatureK": scene.get("color_temperature", 3000)}},
                    },
                    {
                        "type": "device.command",
                        "command": "action.devices.commands.BrightnessAbsolute",
                        "params": {"brightness": int(scene.get("brightness", 0.5) * 100)},
                    },
                ],
            },
            "instructions": [
                "1. Open Google Home → Routines → + New",
                f"2. Add starter: voice command '{scene.get('mood', 'custom')} mode'",
                f"3. Add action: Set lights to {scene.get('color_temperature', 3000)}K",
                f"4. Add action: Set brightness to {int(scene.get('brightness', 0.5) * 100)}%",
                "5. Save and test with 'Hey Google, activate routine'",
            ],
            "compatible_devices": [
                "Google Nest smart bulbs",
                "Any Works with Google lights",
                "TP-Link Kasa",
                "Wyze Bulb",
            ],
        }

    def _export_alexa(self, scene: dict) -> dict:
        return {
            "platform": "alexa",
            "config": {
                "routine_name": f"{scene.get('mood', 'Custom')} Lighting",
                "trigger": {"type": "voice", "phrase": f"set {scene.get('mood', 'custom')} lighting"},
                "actions": [
                    {"type": "smart_home", "device_type": "light", "action": "turnOn"},
                    {"type": "smart_home", "device_type": "light", "action": "setBrightness",
                     "value": int(scene.get("brightness", 0.5) * 100)},
                    {"type": "smart_home", "device_type": "light", "action": "setColorTemperature",
                     "value": scene.get("color_temperature", 3000)},
                ],
            },
            "instructions": [
                "1. Open Alexa app → More → Routines → +",
                f"2. When: Voice — 'Alexa, {scene.get('mood', 'custom')} lighting'",
                "3. Add action: Smart Home → All Lights → Power On",
                f"4. Add action: Set brightness to {int(scene.get('brightness', 0.5) * 100)}%",
                f"5. Add action: Set color temperature to {scene.get('color_temperature', 3000)}K",
            ],
            "compatible_devices": [
                "Amazon Echo Glow",
                "Ring A19 Smart Bulb",
                "Sengled Smart Bulbs",
                "Any Alexa-compatible lights",
            ],
        }

    def _kelvin_to_hue_ct(self, kelvin: int) -> tuple[int, int]:
        mired = max(153, min(500, int(1_000_000 / max(kelvin, 1))))
        return mired, 0

    def _kelvin_to_mired(self, kelvin: int) -> int:
        return max(50, min(400, int(1_000_000 / max(kelvin, 1))))


smart_home_exporter = SmartHomeExporter()
