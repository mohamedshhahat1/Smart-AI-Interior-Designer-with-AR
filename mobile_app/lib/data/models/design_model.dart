class DesignModel {
  final String id;
  final String roomId;
  final String? style;
  final String? prompt;
  final String? generatedImageUrl;
  final Map<String, dynamic>? colorPalette;
  final List<Map<String, dynamic>>? furnitureList;
  final double? estimatedCost;
  final Map<String, dynamic>? costBreakdown;
  final DateTime createdAt;

  DesignModel({
    required this.id,
    required this.roomId,
    this.style,
    this.prompt,
    this.generatedImageUrl,
    this.colorPalette,
    this.furnitureList,
    this.estimatedCost,
    this.costBreakdown,
    required this.createdAt,
  });

  factory DesignModel.fromJson(Map<String, dynamic> json) {
    return DesignModel(
      id: json['id'] as String,
      roomId: json['room_id'] as String,
      style: json['style'] as String?,
      prompt: json['prompt'] as String?,
      generatedImageUrl: json['generated_image_url'] as String?,
      colorPalette: json['color_palette'] as Map<String, dynamic>?,
      furnitureList: (json['furniture_list'] as List<dynamic>?)
          ?.map((e) => e as Map<String, dynamic>)
          .toList(),
      estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
      costBreakdown: json['cost_breakdown'] as Map<String, dynamic>?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'room_id': roomId,
      'style': style,
      'prompt': prompt,
      'generated_image_url': generatedImageUrl,
      'color_palette': colorPalette,
      'furniture_list': furnitureList,
      'estimated_cost': estimatedCost,
      'cost_breakdown': costBreakdown,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
