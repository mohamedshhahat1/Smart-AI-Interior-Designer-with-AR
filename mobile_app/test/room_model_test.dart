import 'package:flutter_test/flutter_test.dart';
import 'package:smart_interior_ai/data/models/room_model.dart';

void main() {
  test('RoomModel preserves analysis context used by feature workflows', () {
    final room = RoomModel.fromJson({
      'id': 'room-1',
      'user_id': 'user-1',
      'image_url': 'https://example.invalid/room.jpg',
      'room_type': 'office',
      'area': 18.0,
      'dimensions': {'width': 5.0, 'depth': 3.6, 'height': 2.8},
      'detected_objects': [
        {'label': 'desk'},
      ],
      'created_at': '2026-06-11T12:00:00Z',
    });

    expect(room.roomType, 'office');
    expect(room.dimensions?['width'], 5.0);
    expect(room.detectedObjects?.first['label'], 'desk');
  });
}
