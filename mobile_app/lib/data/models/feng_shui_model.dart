class BaguaZoneModel {
  final String zone;
  final String direction;
  final String element;
  final String lifeArea;
  final List<String> colors;
  final String status;
  final double score;
  final String? enhancement;

  BaguaZoneModel({
    required this.zone, required this.direction, required this.element,
    required this.lifeArea, required this.colors, required this.status,
    required this.score, this.enhancement,
  });

  factory BaguaZoneModel.fromJson(Map<String, dynamic> json) => BaguaZoneModel(
    zone: json['zone'] as String, direction: json['direction'] as String,
    element: json['element'] as String, lifeArea: json['life_area'] as String,
    colors: List<String>.from(json['colors'] ?? []), status: json['status'] as String,
    score: (json['score'] as num).toDouble(), enhancement: json['enhancement'] as String?,
  );
}

class ElementBalanceModel {
  final String element;
  final double currentLevel;
  final double idealLevel;
  final String status;
  final List<String> associatedColors;
  final List<String> enhancementItems;

  ElementBalanceModel({
    required this.element, required this.currentLevel, required this.idealLevel,
    required this.status, required this.associatedColors, required this.enhancementItems,
  });

  factory ElementBalanceModel.fromJson(Map<String, dynamic> json) => ElementBalanceModel(
    element: json['element'] as String,
    currentLevel: (json['current_level'] as num).toDouble(),
    idealLevel: (json['ideal_level'] as num).toDouble(),
    status: json['status'] as String,
    associatedColors: List<String>.from(json['associated_colors'] ?? []),
    enhancementItems: List<String>.from(json['enhancement_items'] ?? []),
  );
}

class ChiFlowIssueModel {
  final String issueType;
  final String severity;
  final String location;
  final String description;
  final String impact;

  ChiFlowIssueModel({
    required this.issueType, required this.severity, required this.location,
    required this.description, required this.impact,
  });

  factory ChiFlowIssueModel.fromJson(Map<String, dynamic> json) => ChiFlowIssueModel(
    issueType: json['issue_type'] as String, severity: json['severity'] as String,
    location: json['location'] as String, description: json['description'] as String,
    impact: json['impact'] as String,
  );
}

class FengShuiCureModel {
  final String id;
  final String category;
  final String severity;
  final String issueDescription;
  final String cureDescription;
  final String? element;
  final String? placement;
  final double? estimatedCost;
  final int priority;
  final bool isApplied;

  FengShuiCureModel({
    required this.id, required this.category, required this.severity,
    required this.issueDescription, required this.cureDescription,
    this.element, this.placement, this.estimatedCost,
    required this.priority, required this.isApplied,
  });

  factory FengShuiCureModel.fromJson(Map<String, dynamic> json) => FengShuiCureModel(
    id: json['id'] as String, category: json['category'] as String,
    severity: json['severity'] as String,
    issueDescription: json['issue_description'] as String,
    cureDescription: json['cure_description'] as String,
    element: json['element'] as String?, placement: json['placement'] as String?,
    estimatedCost: (json['estimated_cost'] as num?)?.toDouble(),
    priority: json['priority'] as int, isApplied: json['is_applied'] as bool,
  );
}

class FengShuiAnalysisModel {
  final String id;
  final String roomType;
  final String? compassDirection;
  final double overallScore;
  final double chiFlowScore;
  final double elementBalanceScore;
  final double yinYangScore;
  final double clutterScore;
  final double commandingPositionScore;
  final String scoreInterpretation;
  final List<BaguaZoneModel>? baguaMap;
  final List<ElementBalanceModel>? elementAnalysis;
  final List<ChiFlowIssueModel>? chiFlowIssues;
  final List<FengShuiCureModel> cures;
  final Map<String, dynamic>? colorRecommendations;
  final Map<String, dynamic>? luckyDirections;
  final String? birthElement;
  final String summary;
  final DateTime createdAt;

  FengShuiAnalysisModel({
    required this.id, required this.roomType, this.compassDirection,
    required this.overallScore, required this.chiFlowScore,
    required this.elementBalanceScore, required this.yinYangScore,
    required this.clutterScore, required this.commandingPositionScore,
    required this.scoreInterpretation, this.baguaMap, this.elementAnalysis,
    this.chiFlowIssues, required this.cures, this.colorRecommendations,
    this.luckyDirections, this.birthElement, required this.summary,
    required this.createdAt,
  });

  factory FengShuiAnalysisModel.fromJson(Map<String, dynamic> json) => FengShuiAnalysisModel(
    id: json['id'] as String, roomType: json['room_type'] as String,
    compassDirection: json['compass_direction'] as String?,
    overallScore: (json['overall_score'] as num).toDouble(),
    chiFlowScore: (json['chi_flow_score'] as num).toDouble(),
    elementBalanceScore: (json['element_balance_score'] as num).toDouble(),
    yinYangScore: (json['yin_yang_score'] as num).toDouble(),
    clutterScore: (json['clutter_score'] as num).toDouble(),
    commandingPositionScore: (json['commanding_position_score'] as num).toDouble(),
    scoreInterpretation: json['score_interpretation'] as String,
    baguaMap: (json['bagua_map'] as List?)?.map((e) => BaguaZoneModel.fromJson(e)).toList(),
    elementAnalysis: (json['element_analysis'] as List?)?.map((e) => ElementBalanceModel.fromJson(e)).toList(),
    chiFlowIssues: (json['chi_flow_issues'] as List?)?.map((e) => ChiFlowIssueModel.fromJson(e)).toList(),
    cures: (json['cures'] as List).map((e) => FengShuiCureModel.fromJson(e)).toList(),
    colorRecommendations: json['color_recommendations'] as Map<String, dynamic>?,
    luckyDirections: json['lucky_directions'] as Map<String, dynamic>?,
    birthElement: json['birth_element'] as String?,
    summary: json['summary'] as String,
    createdAt: DateTime.parse(json['created_at'] as String),
  );
}
