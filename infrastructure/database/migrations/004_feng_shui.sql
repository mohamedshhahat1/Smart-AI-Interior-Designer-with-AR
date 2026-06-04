-- Smart AI Interior Designer - Feng Shui Analysis Schema
-- Migration: 004_feng_shui
-- Date: 2026-06-04

-- Feng Shui Analyses table
CREATE TABLE IF NOT EXISTS feng_shui_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    design_id UUID REFERENCES designs(id) ON DELETE SET NULL,

    room_type VARCHAR(50) NOT NULL,
    compass_direction VARCHAR(20),

    -- Scoring (0.0 - 10.0)
    overall_score FLOAT NOT NULL,
    chi_flow_score FLOAT NOT NULL,
    element_balance_score FLOAT NOT NULL,
    yin_yang_score FLOAT NOT NULL,
    clutter_score FLOAT NOT NULL,
    commanding_position_score FLOAT NOT NULL,

    -- Detailed analysis JSON
    bagua_map JSONB,
    element_analysis JSONB,
    chi_flow_analysis JSONB,

    -- Recommendations
    issues JSONB,
    cures JSONB,
    enhancements JSONB,

    -- Furniture and color advice
    furniture_placement JSONB,
    color_recommendations JSONB,

    -- Personal feng shui
    lucky_directions JSONB,
    birth_element VARCHAR(20),

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feng_shui_user_id ON feng_shui_analyses(user_id);
CREATE INDEX idx_feng_shui_room_id ON feng_shui_analyses(room_id);

-- Feng Shui Cures (individual actionable items)
CREATE TABLE IF NOT EXISTS feng_shui_cures (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID NOT NULL REFERENCES feng_shui_analyses(id) ON DELETE CASCADE,

    category VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    issue_description TEXT NOT NULL,
    cure_description TEXT NOT NULL,
    element VARCHAR(20),
    placement VARCHAR(100),
    estimated_cost FLOAT,
    priority INTEGER DEFAULT 3,
    is_applied BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_feng_shui_cures_analysis ON feng_shui_cures(analysis_id);
CREATE INDEX idx_feng_shui_cures_priority ON feng_shui_cures(priority);
