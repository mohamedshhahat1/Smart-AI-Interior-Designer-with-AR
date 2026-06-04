class Furniture3DModel {
  final String objectId;
  final String name;
  final String category;
  final String? modelUrl;
  final Map<String, dynamic> position;
  final Map<String, dynamic> rotation;
  final Map<String, dynamic> scale;
  final String? material;
  final bool interactable;

  Furniture3DModel({required this.objectId, required this.name, required this.category, this.modelUrl, required this.position, required this.rotation, required this.scale, this.material, this.interactable = true});

  factory Furniture3DModel.fromJson(Map<String, dynamic> json) => Furniture3DModel(
    objectId: json['object_id'] as String, name: json['name'] as String,
    category: json['category'] as String, modelUrl: json['model_url'] as String?,
    position: json['position'] as Map<String, dynamic>, rotation: json['rotation'] as Map<String, dynamic>,
    scale: json['scale'] as Map<String, dynamic>, material: json['material'] as String?,
    interactable: json['interactable'] as bool? ?? true,
  );
}

class CameraPositionModel {
  final String positionId;
  final String label;
  final Map<String, dynamic> position;
  final Map<String, dynamic> lookAt;
  final double fov;

  CameraPositionModel({required this.positionId, required this.label, required this.position, required this.lookAt, this.fov = 60.0});

  factory CameraPositionModel.fromJson(Map<String, dynamic> json) => CameraPositionModel(
    positionId: json['position_id'] as String, label: json['label'] as String,
    position: json['position'] as Map<String, dynamic>, lookAt: json['look_at'] as Map<String, dynamic>,
    fov: (json['fov'] as num?)?.toDouble() ?? 60.0,
  );
}

class WalkthroughPathModel {
  final int index;
  final Map<String, dynamic> position;
  final Map<String, dynamic> lookAt;
  final double durationSeconds;
  final String easing;

  WalkthroughPathModel({required this.index, required this.position, required this.lookAt, required this.durationSeconds, this.easing = 'ease_in_out'});

  factory WalkthroughPathModel.fromJson(Map<String, dynamic> json) => WalkthroughPathModel(
    index: json['index'] as int, position: json['position'] as Map<String, dynamic>,
    lookAt: json['look_at'] as Map<String, dynamic>,
    durationSeconds: (json['duration_seconds'] as num).toDouble(),
    easing: json['easing'] as String? ?? 'ease_in_out',
  );
}

class Room3DModelData {
  final String id;
  final String name;
  final String roomType;
  final String status;
  final String reconstructionMethod;
  final String qualityLevel;
  final Map<String, dynamic>? dimensions;
  final String? glbModelUrl;
  final String? usdzModelUrl;
  final List<Furniture3DModel>? furnitureObjects;
  final List<CameraPositionModel>? cameraPositions;
  final List<WalkthroughPathModel>? walkthroughPath;
  final int? polygonCount;
  final double? fileSizeMb;
  final double? processingTimeSeconds;
  final int viewCount;
  final DateTime createdAt;

  Room3DModelData({
    required this.id, required this.name, required this.roomType, required this.status,
    required this.reconstructionMethod, required this.qualityLevel, this.dimensions,
    this.glbModelUrl, this.usdzModelUrl, this.furnitureObjects, this.cameraPositions,
    this.walkthroughPath, this.polygonCount, this.fileSizeMb, this.processingTimeSeconds,
    this.viewCount = 0, required this.createdAt,
  });

  factory Room3DModelData.fromJson(Map<String, dynamic> json) => Room3DModelData(
    id: json['id'] as String, name: json['name'] as String,
    roomType: json['room_type'] as String, status: json['status'] as String,
    reconstructionMethod: json['reconstruction_method'] as String,
    qualityLevel: json['quality_level'] as String,
    dimensions: json['dimensions'] as Map<String, dynamic>?,
    glbModelUrl: json['glb_model_url'] as String?,
    usdzModelUrl: json['usdz_model_url'] as String?,
    furnitureObjects: (json['furniture_objects'] as List?)?.map((e) => Furniture3DModel.fromJson(e)).toList(),
    cameraPositions: (json['camera_positions'] as List?)?.map((e) => CameraPositionModel.fromJson(e)).toList(),
    walkthroughPath: (json['walkthrough_path'] as List?)?.map((e) => WalkthroughPathModel.fromJson(e)).toList(),
    polygonCount: json['polygon_count'] as int?,
    fileSizeMb: (json['file_size_mb'] as num?)?.toDouble(),
    processingTimeSeconds: (json['processing_time_seconds'] as num?)?.toDouble(),
    viewCount: json['view_count'] as int? ?? 0,
    createdAt: DateTime.parse(json['created_at'] as String),
  );
}
