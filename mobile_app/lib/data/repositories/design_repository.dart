import 'package:smart_interior_ai/data/models/design_model.dart';
import 'package:smart_interior_ai/data/models/furniture_model.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class DesignRepository {
  final ApiService _apiService;

  DesignRepository({ApiService? apiService})
      : _apiService = apiService ?? ApiService();

  Future<DesignModel> generateDesign({
    required String roomId,
    required String style,
    String? prompt,
    double? budget,
    bool preserveLayout = true,
  }) async {
    return await _apiService.generateDesign(
      roomId: roomId,
      style: style,
      prompt: prompt,
      budget: budget,
      preserveLayout: preserveLayout,
    );
  }

  Future<DesignModel> enhanceDesign({
    required String designId,
    required String instruction,
  }) async {
    return await _apiService.enhanceDesign(
      designId: designId,
      instruction: instruction,
    );
  }

  Future<List<FurnitureModel>> recommendFurniture({
    required String roomId,
    String? style,
    double? budget,
  }) async {
    return await _apiService.recommendFurniture(
      roomId: roomId,
      style: style,
      budget: budget,
    );
  }

  Future<Map<String, dynamic>> calculateCost({
    required String designId,
    bool includeLabor = true,
    bool includeDecoration = true,
  }) async {
    return await _apiService.calculateCost(
      designId: designId,
      includeLabor: includeLabor,
      includeDecoration: includeDecoration,
    );
  }
}
