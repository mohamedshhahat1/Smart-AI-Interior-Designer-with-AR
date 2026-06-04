-- Smart AI Interior Designer - Seasonal & Holiday Themes Schema
-- Migration: 005_seasonal_themes
-- Date: 2026-06-04

CREATE TABLE IF NOT EXISTS seasonal_themes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    design_id UUID REFERENCES designs(id) ON DELETE SET NULL,

    -- Theme identity
    theme_type VARCHAR(20) NOT NULL CHECK (theme_type IN ('season', 'holiday')),
    season VARCHAR(20),
    holiday VARCHAR(50),
    name VARCHAR(200) NOT NULL,
    description TEXT,

    -- Visual design
    color_palette JSONB,
    textures JSONB,
    materials JSONB,
    lighting_mood VARCHAR(50),

    -- Decor & experience
    decor_items JSONB,
    diy_projects JSONB,
    scent_recommendations JSONB,
    music_playlist_mood VARCHAR(50),

    -- Generated output
    generated_image_url TEXT,
    ar_overlay_data JSONB,

    -- Budget
    budget_tier VARCHAR(20) DEFAULT 'medium',
    estimated_cost FLOAT,
    reusability_score FLOAT,

    -- Transitions
    transition_from VARCHAR(50),
    transition_tips JSONB,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_seasonal_themes_user_id ON seasonal_themes(user_id);
CREATE INDEX idx_seasonal_themes_type ON seasonal_themes(theme_type);
CREATE INDEX idx_seasonal_themes_season ON seasonal_themes(season);
CREATE INDEX idx_seasonal_themes_holiday ON seasonal_themes(holiday);
