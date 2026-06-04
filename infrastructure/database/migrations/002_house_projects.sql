-- Smart AI Interior Designer - Multi-Room House Design Schema
-- Migration: 002_house_projects
-- Date: 2026-06-04

-- House Projects table
CREATE TABLE IF NOT EXISTS house_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    style VARCHAR(50) NOT NULL,
    budget FLOAT,
    currency VARCHAR(3) DEFAULT 'USD',

    -- Shared design identity
    shared_theme JSONB,
    color_palette JSONB,
    material_palette JSONB,
    lighting_scheme JSONB,

    -- Aggregated metrics
    total_area FLOAT,
    room_count INTEGER DEFAULT 0,
    total_estimated_cost FLOAT,
    cost_breakdown_by_room JSONB,

    -- Status: draft, generating, completed, failed
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_house_projects_user_id ON house_projects(user_id);
CREATE INDEX idx_house_projects_status ON house_projects(status);

-- House Room Designs table (junction between projects and room designs)
CREATE TABLE IF NOT EXISTS house_room_designs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    house_project_id UUID NOT NULL REFERENCES house_projects(id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    room_label VARCHAR(100) NOT NULL,
    room_type VARCHAR(50) NOT NULL,
    order_index INTEGER DEFAULT 0,

    -- Per-room design output
    generated_image_url TEXT,
    room_color_palette JSONB,
    furniture_list JSONB,
    estimated_cost FLOAT,
    design_notes TEXT,
    ar_scene_data JSONB,

    -- Status: pending, generating, completed, failed
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_house_room_designs_project_id ON house_room_designs(house_project_id);
CREATE INDEX idx_house_room_designs_room_id ON house_room_designs(room_id);

-- Apply updated_at trigger to house_projects
CREATE TRIGGER house_projects_updated_at
    BEFORE UPDATE ON house_projects
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
