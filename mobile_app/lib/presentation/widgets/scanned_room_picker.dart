import 'package:flutter/material.dart';
import 'package:smart_interior_ai/data/models/room_model.dart';

class ScannedRoomPicker extends StatelessWidget {
  final List<RoomModel> rooms;
  final String? selectedRoomId;
  final bool isLoading;
  final ValueChanged<RoomModel?> onChanged;

  const ScannedRoomPicker({
    super.key,
    required this.rooms,
    required this.selectedRoomId,
    required this.isLoading,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const LinearProgressIndicator();
    }
    if (rooms.isEmpty) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(12),
          child: Row(
            children: [
              Icon(Icons.info_outline),
              SizedBox(width: 8),
              Expanded(
                child: Text('Scan a room before running this analysis.'),
              ),
            ],
          ),
        ),
      );
    }

    return DropdownButtonFormField<String>(
      value: selectedRoomId,
      isExpanded: true,
      decoration: const InputDecoration(
        labelText: 'Scanned room',
        prefixIcon: Icon(Icons.meeting_room_outlined),
      ),
      items: rooms
          .map(
            (room) => DropdownMenuItem(
              value: room.id,
              child: Text((room.roomType ?? 'Room').replaceAll('_', ' ')),
            ),
          )
          .toList(),
      onChanged: (id) {
        RoomModel? selected;
        for (final room in rooms) {
          if (room.id == id) {
            selected = room;
            break;
          }
        }
        onChanged(selected);
      },
    );
  }
}
