class HouseRoomDesignModel {
  final String id;
  final String roomLabel;
  final String roomType;
  final int orderIndex;
  final String? roomId;
  final String? generatedImageUrl;
  final Map<String, dynamic>? roomColorPalette;
  final List<Map<String, dynamic>>? furnitureList;
  final double? estimatedCost;
  final String? designNotes;
  final String status;
  final DateTime createdAt;

  HouseRoomDesignModel({
    required this.id,
    required this.roomLabel,
    required this.roomType,
    required this.orderIndex,
    this.roomId,
    this.generatedImageUrl,
    this.roomColorPalette,
    this.furnitureList,
    this.estimatedCost,
    this.designNotes,
    required this.status,
    required this.createdAt,
  });

  factory HouseRoomDesignModel.fromJson(Map<String, dynamic> json) {
    return HouseRoomDesignModel(
      id: json['id'] as String,
      roomLabel: json['room_label'] as String,
      roomType: json['room_type'] as String,
      orderIndex: json['order_index'] as int,
      roomId: json['room_id'] as String?,
      generatedImageUrl: json['generated_image_url'] as String?,
      roomColorPalette: json['room_color_palette'] as Map<String, dynamic>?,
      furnitureList: (json['furniture_list'] as List<dynamic>?)
          ?.map((e) => e as Map<String, dynamic>)
          .toList(),
      estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
      designNotes: json['design_notes'] as String?,
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}

class SharedThemeModel {
  final String style;
  final List<String> primaryColors;
  final List<String> accentColors;
  final List<String> materials;
  final String lighting;
  final List<String> designPrinciples;

  SharedThemeModel({
    required this.style,
    required this.primaryColors,
    required this.accentColors,
    required this.materials,
    required this.lighting,
    required this.designPrinciples,
  });

  factory SharedThemeModel.fromJson(Map<String, dynamic> json) {
    return SharedThemeModel(
      style: json['style'] as String,
      primaryColors: List<String>.from(json['primary_colors'] ?? []),
      accentColors: List<String>.from(json['accent_colors'] ?? []),
      materials: List<String>.from(json['materials'] ?? []),
      lighting: json['lighting'] as String? ?? '',
      designPrinciples: List<String>.from(json['design_principles'] ?? []),
    );
  }
}

class HouseProjectModel {
  final String id;
  final String userId;
  final String name;
  final String? description;
  final String style;
  final double? budget;
  final String currency;
  final SharedThemeModel? sharedTheme;
  final int roomCount;
  final double? totalEstimatedCost;
  final Map<String, dynamic>? costBreakdownByRoom;
  final String status;
  final List<HouseRoomDesignModel> rooms;
  final DateTime createdAt;
  final DateTime updatedAt;

  HouseProjectModel({
    required this.id,
    required this.userId,
    required this.name,
    this.description,
    required this.style,
    this.budget,
    this.currency = 'USD',
    this.sharedTheme,
    required this.roomCount,
    this.totalEstimatedCost,
    this.costBreakdownByRoom,
    required this.status,
    required this.rooms,
    required this.createdAt,
    required this.updatedAt,
  });

  factory HouseProjectModel.fromJson(Map<String, dynamic> json) {
    return HouseProjectModel(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      name: json['name'] as String,
      description: json['description'] as String?,
      style: json['style'] as String,
      budget: (json['budget'] as num?)?.toDouble(),
      currency: json['currency'] as String? ?? 'USD',
      sharedTheme: json['shared_theme'] != null
          ? SharedThemeModel.fromJson(json['shared_theme'])
          : null,
      roomCount: json['room_count'] as int,
      totalEstimatedCost: (json['total_estimated_cost'] as num?)?.toDouble(),
      costBreakdownByRoom: json['cost_breakdown_by_room'] as Map<String, dynamic>?,
      status: json['status'] as String,
      rooms: (json['rooms'] as List<dynamic>)
          .map((e) => HouseRoomDesignModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}

class HouseProjectSummaryModel {
  final String id;
  final String name;
  final String style;
  final int roomCount;
  final double? totalEstimatedCost;
  final String status;
  final DateTime createdAt;

  HouseProjectSummaryModel({
    required this.id,
    required this.name,
    required this.style,
    required this.roomCount,
    this.totalEstimatedCost,
    required this.status,
    required this.createdAt,
  });

  factory HouseProjectSummaryModel.fromJson(Map<String, dynamic> json) {
    return HouseProjectSummaryModel(
      id: json['id'] as String,
      name: json['name'] as String,
      style: json['style'] as String,
      roomCount: json['room_count'] as int,
      totalEstimatedCost: (json['total_estimated_cost'] as num?)?.toDouble(),
      status: json['status'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }
}
