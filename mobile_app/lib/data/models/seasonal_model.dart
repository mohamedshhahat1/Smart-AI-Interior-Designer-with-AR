class DecorItemModel {
  final String name;
  final String category;
  final String placement;
  final double? estimatedCost;
  final bool reusable;
  final bool diyPossible;

  DecorItemModel({required this.name, required this.category, required this.placement, this.estimatedCost, this.reusable = true, this.diyPossible = false});

  factory DecorItemModel.fromJson(Map<String, dynamic> json) => DecorItemModel(
    name: json['name'] as String, category: json['category'] as String,
    placement: json['placement'] as String,
    estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
    reusable: json['reusable'] as bool? ?? true,
    diyPossible: json['diy_possible'] as bool? ?? false,
  );
}

class DIYProjectModel {
  final String name;
  final String difficulty;
  final int timeMinutes;
  final List<String> materials;
  final String instructions;
  final double estimatedCost;

  DIYProjectModel({required this.name, required this.difficulty, required this.timeMinutes, required this.materials, required this.instructions, required this.estimatedCost});

  factory DIYProjectModel.fromJson(Map<String, dynamic> json) => DIYProjectModel(
    name: json['name'] as String, difficulty: json['difficulty'] as String,
    timeMinutes: json['time_minutes'] as int,
    materials: List<String>.from(json['materials'] ?? []),
    instructions: json['instructions'] as String,
    estimatedCost: (json['estimated_cost'] as num).toDouble(),
  );
}

class ScentModel {
  final String scent;
  final String method;
  final String placement;
  final String intensity;

  ScentModel({required this.scent, required this.method, required this.placement, required this.intensity});

  factory ScentModel.fromJson(Map<String, dynamic> json) => ScentModel(
    scent: json['scent'] as String, method: json['method'] as String,
    placement: json['placement'] as String, intensity: json['intensity'] as String,
  );
}

class SeasonalThemeModel {
  final String id;
  final String themeType;
  final String? season;
  final String? holiday;
  final String name;
  final String? description;
  final Map<String, dynamic>? colorPalette;
  final List<String>? textures;
  final List<String>? materials;
  final String? lightingMood;
  final List<DecorItemModel>? decorItems;
  final List<DIYProjectModel>? diyProjects;
  final List<ScentModel>? scentRecommendations;
  final String? musicPlaylistMood;
  final String budgetTier;
  final double? estimatedCost;
  final double? reusabilityScore;
  final bool isFavorite;
  final DateTime createdAt;

  SeasonalThemeModel({
    required this.id, required this.themeType, this.season, this.holiday,
    required this.name, this.description, this.colorPalette, this.textures,
    this.materials, this.lightingMood, this.decorItems, this.diyProjects,
    this.scentRecommendations, this.musicPlaylistMood, required this.budgetTier,
    this.estimatedCost, this.reusabilityScore, required this.isFavorite, required this.createdAt,
  });

  factory SeasonalThemeModel.fromJson(Map<String, dynamic> json) => SeasonalThemeModel(
    id: json['id'] as String, themeType: json['theme_type'] as String,
    season: json['season'] as String?, holiday: json['holiday'] as String?,
    name: json['name'] as String, description: json['description'] as String?,
    colorPalette: json['color_palette'] as Map<String, dynamic>?,
    textures: (json['textures'] as List?)?.map((e) => e.toString()).toList(),
    materials: (json['materials'] as List?)?.map((e) => e.toString()).toList(),
    lightingMood: json['lighting_mood'] as String?,
    decorItems: (json['decor_items'] as List?)?.map((e) => DecorItemModel.fromJson(e)).toList(),
    diyProjects: (json['diy_projects'] as List?)?.map((e) => DIYProjectModel.fromJson(e)).toList(),
    scentRecommendations: (json['scent_recommendations'] as List?)?.map((e) => ScentModel.fromJson(e)).toList(),
    musicPlaylistMood: json['music_playlist_mood'] as String?,
    budgetTier: json['budget_tier'] as String? ?? 'medium',
    estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
    reusabilityScore: (json['reusability_score'] as num?)?.toDouble(),
    isFavorite: json['is_favorite'] as bool? ?? false,
    createdAt: DateTime.parse(json['created_at'] as String),
  );
}
