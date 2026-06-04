class LightingSceneModel {
  final String id;
  final String name;
  final String mood;
  final String? timeOfDay;
  final String? activity;
  final int colorTemperature;
  final double brightness;
  final String? colorHex;
  final double saturation;
  final List<Map<String, dynamic>>? fixtures;
  final List<Map<String, dynamic>>? zones;
  final double transitionDuration;
  final bool isCircadian;
  final bool isFavorite;
  final int usageCount;
  final DateTime createdAt;

  LightingSceneModel({
    required this.id,
    required this.name,
    required this.mood,
    this.timeOfDay,
    this.activity,
    required this.colorTemperature,
    required this.brightness,
    this.colorHex,
    this.saturation = 0.0,
    this.fixtures,
    this.zones,
    this.transitionDuration = 2.0,
    this.isCircadian = false,
    this.isFavorite = false,
    this.usageCount = 0,
    required this.createdAt,
  });

  factory LightingSceneModel.fromJson(Map<String, dynamic> json) {
    return LightingSceneModel(
      id: json['id'] as String,
      name: json['name'] as String,
      mood: json['mood'] as String,
      timeOfDay: json['time_of_day'] as String?,
      activity: json['activity'] as String?,
      colorTemperature: json['color_temperature'] as int,
      brightness: (json['brightness'] as num).toDouble(),
      colorHex: json['color_hex'] as String?,
      saturation: (json['saturation'] as num?)?.toDouble() ?? 0.0,
      fixtures: (json['fixtures'] as List?)?.map((e) => e as Map<String, dynamic>).toList(),
      zones: (json['zones'] as List?)?.map((e) => e as Map<String, dynamic>).toList(),
      transitionDuration: (json['transition_duration'] as num?)?.toDouble() ?? 2.0,
      isCircadian: json['is_circadian'] as bool? ?? false,
      isFavorite: json['is_favorite'] as bool? ?? false,
      usageCount: json['usage_count'] as int? ?? 0,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

class MoodAnalysisModel {
  final String detectedMood;
  final double confidence;
  final double energyLevel;
  final double warmthScore;
  final List<String> suggestedMoods;
  final String analysisSource;

  MoodAnalysisModel({
    required this.detectedMood,
    required this.confidence,
    required this.energyLevel,
    required this.warmthScore,
    required this.suggestedMoods,
    required this.analysisSource,
  });

  factory MoodAnalysisModel.fromJson(Map<String, dynamic> json) {
    return MoodAnalysisModel(
      detectedMood: json['detected_mood'] as String,
      confidence: (json['confidence'] as num).toDouble(),
      energyLevel: (json['energy_level'] as num).toDouble(),
      warmthScore: (json['warmth_score'] as num).toDouble(),
      suggestedMoods: List<String>.from(json['suggested_moods'] ?? []),
      analysisSource: json['analysis_source'] as String,
    );
  }
}

class LightingRecommendationModel {
  final int colorTemperature;
  final double brightness;
  final String? colorHex;
  final double saturation;
  final String description;
  final String mood;
  final String timeOfDay;
  final String ambianceNotes;
  final double transitionDuration;

  LightingRecommendationModel({
    required this.colorTemperature,
    required this.brightness,
    this.colorHex,
    required this.saturation,
    required this.description,
    required this.mood,
    required this.timeOfDay,
    required this.ambianceNotes,
    required this.transitionDuration,
  });

  factory LightingRecommendationModel.fromJson(Map<String, dynamic> json) {
    return LightingRecommendationModel(
      colorTemperature: json['color_temperature'] as int,
      brightness: (json['brightness'] as num).toDouble(),
      colorHex: json['color_hex'] as String?,
      saturation: (json['saturation'] as num).toDouble(),
      description: json['description'] as String,
      mood: json['mood'] as String,
      timeOfDay: json['time_of_day'] as String,
      ambianceNotes: json['ambiance_notes'] as String,
      transitionDuration: (json['transition_duration'] as num).toDouble(),
    );
  }
}

class MoodDetectResponseModel {
  final MoodAnalysisModel moodAnalysis;
  final LightingRecommendationModel recommendation;
  final List<Map<String, dynamic>> alternativeScenes;
  final String? circadianNote;

  MoodDetectResponseModel({
    required this.moodAnalysis,
    required this.recommendation,
    required this.alternativeScenes,
    this.circadianNote,
  });

  factory MoodDetectResponseModel.fromJson(Map<String, dynamic> json) {
    return MoodDetectResponseModel(
      moodAnalysis: MoodAnalysisModel.fromJson(json['mood_analysis']),
      recommendation: LightingRecommendationModel.fromJson(json['lighting_recommendation']),
      alternativeScenes: (json['alternative_scenes'] as List).map((e) => e as Map<String, dynamic>).toList(),
      circadianNote: json['circadian_note'] as String?,
    );
  }
}
