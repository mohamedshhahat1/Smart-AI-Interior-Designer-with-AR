-- Smart AI Interior Designer - Pet-Friendly Room Design Schema
-- Migration: 006_pet_friendly
-- Date: 2026-06-04

CREATE TABLE IF NOT EXISTS pet_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    name VARCHAR(100) NOT NULL,
    species VARCHAR(20) NOT NULL,
    breed VARCHAR(100),
    size VARCHAR(20) NOT NULL,
    age_years FLOAT,
    weight_kg FLOAT,

    energy_level VARCHAR(20) DEFAULT 'medium',
    is_indoor BOOLEAN DEFAULT TRUE,
    is_destructive BOOLEAN DEFAULT FALSE,
    sheds_fur BOOLEAN DEFAULT TRUE,
    climbs_furniture BOOLEAN DEFAULT FALSE,
    has_allergies BOOLEAN DEFAULT FALSE,

    special_needs JSONB,
    behavioral_notes TEXT,

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_pet_profiles_user_id ON pet_profiles(user_id);
CREATE INDEX idx_pet_profiles_species ON pet_profiles(species);

CREATE TABLE IF NOT EXISTS pet_friendly_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    room_id UUID REFERENCES rooms(id) ON DELETE SET NULL,

    pet_profile_ids JSONB,
    room_type VARCHAR(50) NOT NULL,

    overall_score FLOAT NOT NULL,
    safety_score FLOAT NOT NULL,
    comfort_score FLOAT NOT NULL,
    durability_score FLOAT NOT NULL,
    cleanliness_score FLOAT NOT NULL,

    hazards JSONB,
    zone_plan JSONB,
    material_recommendations JSONB,
    furniture_recommendations JSONB,
    plant_safety JSONB,
    cleaning_tips JSONB,
    product_recommendations JSONB,

    estimated_cost FLOAT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_pet_analyses_user_id ON pet_friendly_analyses(user_id);
CREATE INDEX idx_pet_analyses_room_id ON pet_friendly_analyses(room_id);
