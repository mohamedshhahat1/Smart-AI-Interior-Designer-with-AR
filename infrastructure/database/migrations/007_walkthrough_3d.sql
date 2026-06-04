-- Smart AI Interior Designer - 3D Walkthrough / Room Generation Schema
-- Migration: 007_walkthrough_3d
-- Date: 2026-06-04

CREATE TABLE IF NOT EXISTS room_3d_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,
    design_id UUID REFERENCES designs(id) ON DELETE SET NULL,

    name VARCHAR(200) NOT NULL,
    room_type VARCHAR(50) NOT NULL,

    -- 3D data
    room_geometry JSONB,
    depth_map_url TEXT,
    mesh_url TEXT,
    texture_urls JSONB,
    glb_model_url TEXT,
    usdz_model_url TEXT,

    -- Scene composition
    furniture_3d_objects JSONB,
    lighting_setup JSONB,
    camera_positions JSONB,
    walkthrough_path JSONB,

    -- Metadata
    dimensions JSONB,
    reconstruction_method VARCHAR(50) DEFAULT 'depth_estimation',
    quality_level VARCHAR(20) DEFAULT 'standard',
    polygon_count INTEGER,
    file_size_mb FLOAT,

    -- Processing
    status VARCHAR(20) DEFAULT 'pending',
    processing_time_seconds FLOAT,
    error_message TEXT,

    -- Social
    is_public BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_room_3d_user_id ON room_3d_models(user_id);
CREATE INDEX idx_room_3d_room_id ON room_3d_models(room_id);
CREATE INDEX idx_room_3d_status ON room_3d_models(status);

CREATE TABLE IF NOT EXISTS walkthrough_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    model_id UUID NOT NULL REFERENCES room_3d_models(id) ON DELETE CASCADE,

    camera_path_taken JSONB,
    duration_seconds FLOAT,
    screenshots_taken INTEGER DEFAULT 0,
    annotations JSONB,
    comparison_model_id UUID,

    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ
);

CREATE INDEX idx_walkthrough_user_id ON walkthrough_sessions(user_id);
CREATE INDEX idx_walkthrough_model_id ON walkthrough_sessions(model_id);
