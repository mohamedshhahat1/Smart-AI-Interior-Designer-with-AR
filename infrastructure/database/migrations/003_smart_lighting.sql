-- Smart AI Interior Designer - Smart Lighting & Mood Detection Schema
-- Migration: 003_smart_lighting
-- Date: 2026-06-04

-- Lighting Scenes table
CREATE TABLE IF NOT EXISTS lighting_scenes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    design_id UUID REFERENCES designs(id) ON DELETE SET NULL,

    name VARCHAR(100) NOT NULL,
    mood VARCHAR(50) NOT NULL,
    time_of_day VARCHAR(20),
    activity VARCHAR(50),

    -- Lighting parameters
    color_temperature INTEGER NOT NULL CHECK (color_temperature BETWEEN 1800 AND 6500),
    brightness FLOAT NOT NULL CHECK (brightness BETWEEN 0.0 AND 1.0),
    color_hex VARCHAR(7),
    saturation FLOAT DEFAULT 0.0 CHECK (saturation BETWEEN 0.0 AND 1.0),

    -- Fixture and zone configuration
    fixtures JSONB,
    zones JSONB,
    transition_duration FLOAT DEFAULT 2.0,

    -- Circadian rhythm support
    is_circadian BOOLEAN DEFAULT FALSE,
    circadian_schedule JSONB,

    -- Smart home integration
    smart_home_config JSONB,

    -- Usage tracking
    is_favorite BOOLEAN DEFAULT FALSE,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_lighting_scenes_user_id ON lighting_scenes(user_id);
CREATE INDEX idx_lighting_scenes_mood ON lighting_scenes(mood);
CREATE INDEX idx_lighting_scenes_room_id ON lighting_scenes(room_id);

-- Mood Profiles table
CREATE TABLE IF NOT EXISTS mood_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    name VARCHAR(100) NOT NULL,
    mood_type VARCHAR(50) NOT NULL,
    energy_level FLOAT DEFAULT 0.5 CHECK (energy_level BETWEEN 0.0 AND 1.0),
    warmth_preference FLOAT DEFAULT 0.5 CHECK (warmth_preference BETWEEN 0.0 AND 1.0),
    brightness_preference FLOAT DEFAULT 0.5 CHECK (brightness_preference BETWEEN 0.0 AND 1.0),

    preferred_colors JSONB,
    preferred_activities JSONB,
    time_associations JSONB,
    room_overrides JSONB,

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_mood_profiles_user_id ON mood_profiles(user_id);
CREATE INDEX idx_mood_profiles_mood_type ON mood_profiles(mood_type);

-- Lighting Analytics table
CREATE TABLE IF NOT EXISTS lighting_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scene_id UUID REFERENCES lighting_scenes(id) ON DELETE SET NULL,

    mood VARCHAR(50) NOT NULL,
    time_of_day VARCHAR(20) NOT NULL,
    duration_minutes FLOAT,
    feedback_rating INTEGER CHECK (feedback_rating BETWEEN 1 AND 5),
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_lighting_analytics_user_id ON lighting_analytics(user_id);
CREATE INDEX idx_lighting_analytics_mood ON lighting_analytics(mood);
CREATE INDEX idx_lighting_analytics_recorded ON lighting_analytics(recorded_at);
