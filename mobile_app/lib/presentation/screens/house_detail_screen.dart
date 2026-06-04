import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/house_project_model.dart';

class HouseDetailScreen extends StatefulWidget {
  final String projectId;
  const HouseDetailScreen({super.key, required this.projectId});

  @override
  State<HouseDetailScreen> createState() => _HouseDetailScreenState();
}

class _HouseDetailScreenState extends State<HouseDetailScreen> {
  HouseProjectModel? _project;
  bool _isLoading = true;
  bool _isGenerating = false;

  @override
  void initState() {
    super.initState();
    _loadProject();
  }

  Future<void> _loadProject() async {
    setState(() => _isLoading = true);
    try {
      final response = await ApiClient().dio.get('/house/project/${widget.projectId}');
      setState(() {
        _project = HouseProjectModel.fromJson(response.data);
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to load project')),
        );
      }
    }
  }

  Future<void> _generateDesigns() async {
    setState(() => _isGenerating = true);
    try {
      final response = await ApiClient().dio.post(
        '/house/project/${widget.projectId}/generate',
        data: {'project_id': widget.projectId, 'preserve_layout': true},
      );
      setState(() {
        _project = HouseProjectModel.fromJson(response.data);
        _isGenerating = false;
      });
    } catch (e) {
      setState(() => _isGenerating = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Generation failed. Please try again.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('House Project')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_project == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('House Project')),
        body: const Center(child: Text('Project not found')),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(_project!.name),
        actions: [
          IconButton(
            icon: const Icon(Icons.calculate),
            onPressed: () => context.go('/house/${widget.projectId}/cost'),
            tooltip: 'Cost Report',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildThemeCard(),
            const SizedBox(height: 20),
            if (_project!.totalEstimatedCost != null) _buildCostSummary(),
            if (_project!.totalEstimatedCost != null) const SizedBox(height: 20),
            _buildRoomsList(),
            const SizedBox(height: 20),
            if (_project!.status == 'draft') _buildGenerateButton(),
          ],
        ),
      ),
    );
  }

  Widget _buildThemeCard() {
    final theme = _project!.sharedTheme;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.palette, color: Colors.white, size: 28),
              const SizedBox(width: 10),
              Text(
                'Shared Design Theme',
                style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 16),
          _themeRow('Style', _project!.style.replaceAll('_', ' ').toUpperCase()),
          if (theme != null) ...[
            const SizedBox(height: 8),
            _themeRow('Colors', theme.primaryColors.join(', ')),
            const SizedBox(height: 8),
            _themeRow('Materials', theme.materials.join(', ')),
            const SizedBox(height: 8),
            _themeRow('Lighting', theme.lighting),
          ],
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: _statusColor(_project!.status).withOpacity(0.3),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              _project!.status.toUpperCase(),
              style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
    );
  }

  Widget _themeRow(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 80,
          child: Text(label, style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 13)),
        ),
        Expanded(
          child: Text(value, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w500)),
        ),
      ],
    );
  }

  Widget _buildCostSummary() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            const Icon(Icons.attach_money, color: AppTheme.successColor, size: 32),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Total Estimated Cost', style: TextStyle(fontSize: 13, color: Colors.grey)),
                  Text(
                    '\$${_project!.totalEstimatedCost!.toStringAsFixed(2)}',
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
            if (_project!.budget != null)
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  const Text('Budget', style: TextStyle(fontSize: 13, color: Colors.grey)),
                  Text('\$${_project!.budget!.toStringAsFixed(0)}',
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                ],
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildRoomsList() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Rooms (${_project!.rooms.length})', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...List.generate(_project!.rooms.length, (i) {
          final room = _project!.rooms[i];
          return _buildRoomCard(room, i);
        }),
      ],
    );
  }

  Widget _buildRoomCard(HouseRoomDesignModel room, int index) {
    final statusColor = _statusColor(room.status);
    final roomIcon = _roomIcon(room.roomType);

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: InkWell(
        onTap: room.status == 'completed' ? () => _showRoomDetail(room) : null,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              CircleAvatar(
                radius: 24,
                backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
                child: Icon(roomIcon, color: AppTheme.primaryColor),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(room.roomLabel, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                    const SizedBox(height: 4),
                    Text(
                      room.roomType.replaceAll('_', ' '),
                      style: TextStyle(color: Colors.grey[600], fontSize: 13),
                    ),
                    if (room.estimatedCost != null) ...[
                      const SizedBox(height: 4),
                      Text(
                        '\$${room.estimatedCost!.toStringAsFixed(2)}',
                        style: const TextStyle(fontWeight: FontWeight.w600, color: AppTheme.primaryColor),
                      ),
                    ],
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: statusColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  room.status,
                  style: TextStyle(color: statusColor, fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ),
              if (room.status == 'completed')
                const Padding(
                  padding: EdgeInsets.only(left: 8),
                  child: Icon(Icons.chevron_right, color: Colors.grey),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildGenerateButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton.icon(
        onPressed: _isGenerating ? null : _generateDesigns,
        icon: _isGenerating
            ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
            : const Icon(Icons.auto_awesome),
        label: Text(_isGenerating ? 'Generating All Rooms...' : 'Generate All Room Designs'),
        style: ElevatedButton.styleFrom(
          backgroundColor: AppTheme.primaryColor,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 16),
        ),
      ),
    );
  }

  void _showRoomDetail(HouseRoomDesignModel room) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return DraggableScrollableSheet(
          initialChildSize: 0.7,
          minChildSize: 0.4,
          maxChildSize: 0.95,
          expand: false,
          builder: (ctx, scrollController) {
            return SingleChildScrollView(
              controller: scrollController,
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Center(
                    child: Container(
                      width: 40, height: 4,
                      decoration: BoxDecoration(color: Colors.grey[300], borderRadius: BorderRadius.circular(2)),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(room.roomLabel, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text(room.roomType.replaceAll('_', ' '), style: TextStyle(color: Colors.grey[600])),
                  const SizedBox(height: 16),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(16),
                    child: Container(
                      width: double.infinity,
                      height: 220,
                      color: Colors.grey[200],
                      child: const Center(child: Icon(Icons.image, size: 64, color: Colors.grey)),
                    ),
                  ),
                  const SizedBox(height: 16),
                  if (room.estimatedCost != null)
                    Card(
                      child: ListTile(
                        leading: const Icon(Icons.attach_money, color: AppTheme.successColor),
                        title: Text('\$${room.estimatedCost!.toStringAsFixed(2)}'),
                        subtitle: const Text('Room cost estimate'),
                      ),
                    ),
                  if (room.designNotes != null && room.designNotes!.isNotEmpty) ...[
                    const SizedBox(height: 12),
                    const Text('Design Notes', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                    const SizedBox(height: 8),
                    Text(room.designNotes!, style: TextStyle(color: Colors.grey[700])),
                  ],
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () {
                            Navigator.pop(ctx);
                            if (room.roomId != null) context.go('/ar/${room.id}');
                          },
                          icon: const Icon(Icons.view_in_ar),
                          label: const Text('View in AR'),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => Navigator.pop(ctx),
                          icon: const Icon(Icons.edit),
                          label: const Text('Refine'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.primaryColor,
                            foregroundColor: Colors.white,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  Color _statusColor(String status) {
    switch (status) {
      case 'completed': return AppTheme.successColor;
      case 'generating': return AppTheme.warningColor;
      case 'failed': return AppTheme.errorColor;
      default: return Colors.grey;
    }
  }

  IconData _roomIcon(String roomType) {
    switch (roomType) {
      case 'living_room': return Icons.weekend;
      case 'bedroom': return Icons.bed;
      case 'kitchen': return Icons.kitchen;
      case 'bathroom': return Icons.bathtub;
      case 'dining_room': return Icons.restaurant;
      case 'office': return Icons.computer;
      case 'hallway': return Icons.door_front_door;
      default: return Icons.meeting_room;
    }
  }
}
