-- Smart AI Interior Designer - Initial Database Schema
-- Migration: 001_initial_schema
-- Date: 2026-06-04

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    room_type VARCHAR(50),
    area FLOAT,
    dimensions JSONB,
    detected_objects JSONB,
    segmentation_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rooms_user_id ON rooms(user_id);

-- Designs table
CREATE TABLE IF NOT EXISTS designs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    room_id UUID NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    style VARCHAR(50),
    prompt TEXT,
    generated_image_url TEXT,
    color_palette JSONB,
    furniture_list JSONB,
    estimated_cost FLOAT,
    cost_breakdown JSONB,
    ar_scene_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_designs_room_id ON designs(room_id);

-- Furniture catalog table
CREATE TABLE IF NOT EXISTS furniture_catalog (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    style VARCHAR(50),
    description TEXT,
    price FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    dimensions JSONB,
    color VARCHAR(50),
    material VARCHAR(100),
    image_url TEXT,
    model_3d_url TEXT,
    stock_quantity INTEGER DEFAULT 0,
    rating FLOAT,
    tags JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_furniture_category ON furniture_catalog(category);
CREATE INDEX idx_furniture_name ON furniture_catalog(name);
CREATE INDEX idx_furniture_style ON furniture_catalog(style);

-- Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    design_id UUID NOT NULL REFERENCES designs(id) ON DELETE CASCADE,
    furniture_id UUID NOT NULL REFERENCES furniture_catalog(id),
    relevance_score FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cost reports table
CREATE TABLE IF NOT EXISTS cost_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    design_id UUID NOT NULL REFERENCES designs(id) ON DELETE CASCADE,
    furniture_cost FLOAT DEFAULT 0,
    decoration_cost FLOAT DEFAULT 0,
    lighting_cost FLOAT DEFAULT 0,
    flooring_cost FLOAT DEFAULT 0,
    labor_cost FLOAT DEFAULT 0,
    total_cost FLOAT DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    budget_status VARCHAR(50),
    savings_suggestions JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cost_reports_design_id ON cost_reports(design_id);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
