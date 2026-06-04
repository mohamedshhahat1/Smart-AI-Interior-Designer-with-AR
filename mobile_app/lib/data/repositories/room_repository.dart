import 'dart:io';
import 'package:smart_interior_ai/data/models/room_model.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class RoomRepository {
  final ApiService _apiService;

  RoomRepository({ApiService? apiService})
      : _apiService = apiService ?? ApiService();

  Future<RoomModel> uploadRoom(File imageFile) async {
    return await _apiService.uploadRoom(imageFile);
  }

  Future<RoomModel> getRoom(String roomId) async {
    return await _apiService.getRoom(roomId);
  }

  Future<List<RoomModel>> listRooms() async {
    return await _apiService.listRooms();
  }
}
