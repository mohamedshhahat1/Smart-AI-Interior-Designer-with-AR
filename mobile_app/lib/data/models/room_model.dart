class RoomModel {
  final String id;
  final String userId;
  final String imageUrl;
  final String? roomType;
  final double? area;
  final Map<String, dynamic>? dimensions;
  final List<dynamic>? detectedObjects;
  final DateTime createdAt;

  RoomModel({
    required this.id,
    required this.userId,
    required this.imageUrl,
    this.roomType,
    this.area,
    this.dimensions,
    this.detectedObjects,
    required this.createdAt,
  });

  factory RoomModel.fromJson(Map<String, dynamic> json) {
    return RoomModel(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      imageUrl: json['image_url'] as String,
      roomType: json['room_type'] as String?,
      area: (json['area'] as num?)?.toDouble(),
      dimensions: json['dimensions'] as Map<String, dynamic>?,
      detectedObjects: json['detected_objects'] as List<dynamic>?,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'image_url': imageUrl,
      'room_type': roomType,
      'area': area,
      'dimensions': dimensions,
      'detected_objects': detectedObjects,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
