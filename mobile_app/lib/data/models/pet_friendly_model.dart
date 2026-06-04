class PetProfileModel {
  final String id;
  final String name;
  final String species;
  final String? breed;
  final String size;
  final double? ageYears;
  final String energyLevel;
  final bool isIndoor;
  final bool isDestructive;
  final bool shedsFur;
  final bool climbsFurniture;
  final bool hasAllergies;
  final DateTime createdAt;

  PetProfileModel({
    required this.id, required this.name, required this.species, this.breed,
    required this.size, this.ageYears, required this.energyLevel,
    required this.isIndoor, required this.isDestructive, required this.shedsFur,
    required this.climbsFurniture, required this.hasAllergies, required this.createdAt,
  });

  factory PetProfileModel.fromJson(Map<String, dynamic> json) => PetProfileModel(
    id: json['id'] as String, name: json['name'] as String,
    species: json['species'] as String, breed: json['breed'] as String?,
    size: json['size'] as String, ageYears: (json['age_years'] as num?)?.toDouble(),
    energyLevel: json['energy_level'] as String? ?? 'medium',
    isIndoor: json['is_indoor'] as bool? ?? true,
    isDestructive: json['is_destructive'] as bool? ?? false,
    shedsFur: json['sheds_fur'] as bool? ?? true,
    climbsFurniture: json['climbs_furniture'] as bool? ?? false,
    hasAllergies: json['has_allergies'] as bool? ?? false,
    createdAt: DateTime.parse(json['created_at'] as String),
  );
}

class PetHazardModel {
  final String hazardType;
  final String severity;
  final String item;
  final String description;
  final String solution;
  final double? estimatedCost;

  PetHazardModel({required this.hazardType, required this.severity, required this.item, required this.description, required this.solution, this.estimatedCost});

  factory PetHazardModel.fromJson(Map<String, dynamic> json) => PetHazardModel(
    hazardType: json['hazard_type'] as String, severity: json['severity'] as String,
    item: json['item'] as String, description: json['description'] as String,
    solution: json['solution'] as String, estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
  );
}

class PetZoneModel {
  final String zoneName;
  final String zoneType;
  final String location;
  final String description;
  final List<String> itemsNeeded;
  final double estimatedCost;

  PetZoneModel({required this.zoneName, required this.zoneType, required this.location, required this.description, required this.itemsNeeded, required this.estimatedCost});

  factory PetZoneModel.fromJson(Map<String, dynamic> json) => PetZoneModel(
    zoneName: json['zone_name'] as String, zoneType: json['zone_type'] as String,
    location: json['location'] as String, description: json['description'] as String,
    itemsNeeded: List<String>.from(json['items_needed'] ?? []),
    estimatedCost: (json['estimated_cost'] as num).toDouble(),
  );
}

class PetFriendlyAnalysisModel {
  final String id;
  final String roomType;
  final double overallScore;
  final double safetyScore;
  final double comfortScore;
  final double durabilityScore;
  final double cleanlinessScore;
  final String scoreInterpretation;
  final List<PetHazardModel> hazards;
  final List<PetZoneModel> zonePlan;
  final List<Map<String, dynamic>> materialRecommendations;
  final Map<String, dynamic>? plantSafety;
  final List<String> cleaningTips;
  final List<Map<String, dynamic>>? productRecommendations;
  final double? estimatedCost;
  final DateTime createdAt;

  PetFriendlyAnalysisModel({
    required this.id, required this.roomType, required this.overallScore,
    required this.safetyScore, required this.comfortScore, required this.durabilityScore,
    required this.cleanlinessScore, required this.scoreInterpretation,
    required this.hazards, required this.zonePlan, required this.materialRecommendations,
    this.plantSafety, required this.cleaningTips, this.productRecommendations,
    this.estimatedCost, required this.createdAt,
  });

  factory PetFriendlyAnalysisModel.fromJson(Map<String, dynamic> json) => PetFriendlyAnalysisModel(
    id: json['id'] as String, roomType: json['room_type'] as String,
    overallScore: (json['overall_score'] as num).toDouble(),
    safetyScore: (json['safety_score'] as num).toDouble(),
    comfortScore: (json['comfort_score'] as num).toDouble(),
    durabilityScore: (json['durability_score'] as num).toDouble(),
    cleanlinessScore: (json['cleanliness_score'] as num).toDouble(),
    scoreInterpretation: json['score_interpretation'] as String,
    hazards: (json['hazards'] as List).map((e) => PetHazardModel.fromJson(e)).toList(),
    zonePlan: (json['zone_plan'] as List).map((e) => PetZoneModel.fromJson(e)).toList(),
    materialRecommendations: (json['material_recommendations'] as List).map((e) => e as Map<String, dynamic>).toList(),
    plantSafety: json['plant_safety'] as Map<String, dynamic>?,
    cleaningTips: List<String>.from(json['cleaning_tips'] ?? []),
    productRecommendations: (json['product_recommendations'] as List?)?.map((e) => e as Map<String, dynamic>).toList(),
    estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
    createdAt: DateTime.parse(json['created_at'] as String),
  );
}
