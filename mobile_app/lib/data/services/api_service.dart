import 'dart:io';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/room_model.dart';
import 'package:smart_interior_ai/data/models/design_model.dart';
import 'package:smart_interior_ai/data/models/furniture_model.dart';

class ApiService {
  final Dio _dio = ApiClient().dio;

  Future<Map<String, dynamic>> register(
      String name, String email, String password) async {
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

  Future<RoomModel> uploadRoomBytes(Uint8List bytes, String filename) async {
    final formData = FormData.fromMap({
      'file': MultipartFile.fromBytes(bytes, filename: filename),
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

  Future<Map<String, dynamic>> chatWithAssistant({
    required String roomId,
    required String message,
    List<Map<String, String>>? conversationHistory,
  }) async {
    final response = await _dio.post('/assistant/chat', data: {
      'room_id': roomId,
      'message': message,
      'conversation_history': conversationHistory,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> generateCircadianSchedule({
    String wakeTime = '07:00',
    String sleepTime = '23:00',
    List<String>? workHours,
  }) async {
    final response = await _dio.post('/lighting/circadian', data: {
      'wake_time': wakeTime,
      'sleep_time': sleepTime,
      'work_hours': workHours,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> saveLightingScene({
    required String name,
    required String mood,
    required int colorTemperature,
    required double brightness,
    String? colorHex,
    double saturation = 0.0,
    List<Map<String, dynamic>>? fixtures,
    List<Map<String, dynamic>>? zones,
    double transitionDuration = 2.0,
    String? timeOfDay,
    String? activity,
  }) async {
    final response = await _dio.post('/lighting/scenes', data: {
      'name': name,
      'mood': mood,
      'color_temperature': colorTemperature,
      'brightness': brightness,
      'color_hex': colorHex,
      'saturation': saturation,
      'fixtures': fixtures,
      'zones': zones,
      'transition_duration': transitionDuration,
      'time_of_day': timeOfDay,
      'activity': activity,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> exportToSmartHome({
    required String sceneId,
    required String platform,
  }) async {
    final response = await _dio.post('/lighting/export', data: {
      'scene_id': sceneId,
      'platform': platform,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> generateARScene({
    required String designId,
    Map<String, dynamic>? roomDimensions,
  }) async {
    final response = await _dio.post('/ar/generate-scene', data: {
      'design_id': designId,
      'room_dimensions': roomDimensions,
    });
    return response.data;
  }

  Future<Map<String, dynamic>> getProfile() async {
    final response = await _dio.get('/auth/me');
    return response.data;
  }

  Future<List<DesignModel>> listDesigns() async {
    final response = await _dio.get('/design/');
    return (response.data as List).map((e) => DesignModel.fromJson(e)).toList();
  }

  Future<DesignModel> getDesign(String designId) async {
    final response = await _dio.get('/design/$designId');
    return DesignModel.fromJson(response.data);
  }
}
