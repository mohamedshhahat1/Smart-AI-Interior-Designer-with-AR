import 'dart:io';
import 'package:dio/dio.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/room_model.dart';
import 'package:smart_interior_ai/data/models/design_model.dart';
import 'package:smart_interior_ai/data/models/furniture_model.dart';

class ApiService {
  final Dio _dio = ApiClient().dio;

  Future<Map<String, dynamic>> register(String name, String email, String password) async {
    final response = await _dio.post('/auth/register', data: {
      'name': name,
      'email': email,
      'password': password,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });
    return response.data;
  }

  Future<RoomModel> uploadRoom(File imageFile) async {
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(
        imageFile.path,
        filename: imageFile.path.split('/').last,
      ),
    });
    final response = await _dio.post('/room/upload', data: formData);
    return RoomModel.fromJson(response.data);
  }

  Future<RoomModel> getRoom(String roomId) async {
    final response = await _dio.get('/room/$roomId');
    return RoomModel.fromJson(response.data);
  }

  Future<List<RoomModel>> listRooms() async {
    final response = await _dio.get('/room/');
    return (response.data as List).map((e) => RoomModel.fromJson(e)).toList();
  }

  Future<DesignModel> generateDesign({
    required String roomId,
    required String style,
    String? prompt,
    double? budget,
    bool preserveLayout = true,
  }) async {
    final response = await _dio.post('/design/generate', data: {
      'room_id': roomId,
      'style': style,
      'prompt': prompt,
      'budget': budget,
      'preserve_layout': preserveLayout,
    });
    return DesignModel.fromJson(response.data);
  }

  Future<DesignModel> enhanceDesign({
    required String designId,
    required String instruction,
  }) async {
    final response = await _dio.post('/design/enhance', data: {
      'design_id': designId,
      'instruction': instruction,
    });
    return DesignModel.fromJson(response.data);
  }

  Future<List<FurnitureModel>> recommendFurniture({
    required String roomId,
    String? style,
    double? budget,
  }) async {
    final response = await _dio.post('/furniture/recommend', data: {
      'room_id': roomId,
      'style': style,
      'budget': budget,
    });
    final data = response.data;
    final recommendations = data['recommendations'] as List;
    return recommendations.map((e) => FurnitureModel.fromJson(e)).toList();
  }

  Future<Map<String, dynamic>> calculateCost({
    required String designId,
    bool includeLabor = true,
    bool includeDecoration = true,
  }) async {
    final response = await _dio.post('/cost/calculate', data: {
      'design_id': designId,
      'include_labor': includeLabor,
      'include_decoration': includeDecoration,
    });
    return response.data;
  }
}
