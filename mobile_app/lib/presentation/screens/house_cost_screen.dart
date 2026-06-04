import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';

class HouseCostScreen extends StatefulWidget {
  final String projectId;
  const HouseCostScreen({super.key, required this.projectId});

  @override
  State<HouseCostScreen> createState() => _HouseCostScreenState();
}

class _HouseCostScreenState extends State<HouseCostScreen> {
  Map<String, dynamic>? _costReport;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadCostReport();
  }

  Future<void> _loadCostReport() async {
    try {
      final response = await ApiClient().dio.get('/house/project/${widget.projectId}/cost');
      setState(() {
        _costReport = response.data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('House Cost Report')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _costReport == null
              ? const Center(child: Text('Failed to load cost report'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildTotalCard(),
                      const SizedBox(height: 20),
                      _buildRoomCosts(),
                      const SizedBox(height: 20),
                      _buildSharedElements(),
                      const SizedBox(height: 20),
                      if (_costReport!['savings_suggestions'] != null) _buildSuggestions(),
                    ],
                  ),
                ),
    );
  }

  Widget _buildTotalCard() {
    final total = _costReport!['total_cost'] ?? 0.0;
    final budget = _costReport!['budget'];
    final status = _costReport!['budget_status'] ?? 'unknown';

    Color statusColor;
    switch (status) {
      case 'well_under_budget':
      case 'within_budget':
        statusColor = AppTheme.successColor;
        break;
      case 'slightly_over_budget':
        statusColor = AppTheme.warningColor;
        break;
      default:
        statusColor = AppTheme.errorColor;
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
        ),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        children: [
          Text(
            _costReport!['project_name'] ?? 'House Project',
            style: const TextStyle(color: Colors.white70, fontSize: 14),
          ),
          const SizedBox(height: 4),
          Text(
            _costReport!['style']?.toString().replaceAll('_', ' ').toUpperCase() ?? '',
            style: const TextStyle(color: Colors.white54, fontSize: 12),
          ),
          const SizedBox(height: 12),
          const Text('Total House Cost', style: TextStyle(color: Colors.white70, fontSize: 14)),
          const SizedBox(height: 4),
          Text(
            '\$${(total as num).toStringAsFixed(2)}',
            style: const TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold),
          ),
          if (budget != null) ...[
            const SizedBox(height: 8),
            Text('Budget: \$${(budget as num).toStringAsFixed(0)}', style: const TextStyle(color: Colors.white60)),
          ],
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: statusColor.withOpacity(0.3),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(
              status.replaceAll('_', ' ').toUpperCase(),
              style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRoomCosts() {
    final rooms = _costReport!['room_costs'] as List? ?? [];

    final icons = {
      'living_room': Icons.weekend,
      'bedroom': Icons.bed,
      'kitchen': Icons.kitchen,
      'bathroom': Icons.bathtub,
      'dining_room': Icons.restaurant,
      'office': Icons.computer,
    };

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Cost Per Room', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...rooms.map((room) {
          final roomType = room['room_type'] ?? '';
          final icon = icons[roomType] ?? Icons.meeting_room;
          final cost = (room['estimated_cost'] as num?) ?? 0;
          final status = room['status'] ?? 'pending';

          return Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
                child: Icon(icon, color: AppTheme.primaryColor, size: 20),
              ),
              title: Text(room['room_label'] ?? 'Room'),
              subtitle: Text(roomType.replaceAll('_', ' ')),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text('\$${cost.toStringAsFixed(2)}',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  Text(status, style: TextStyle(fontSize: 11, color: Colors.grey[500])),
                ],
              ),
            ),
          );
        }),
      ],
    );
  }

  Widget _buildSharedElements() {
    final shared = _costReport!['shared_elements_cost'] as Map<String, dynamic>? ?? {};

    final items = [
      {'label': 'Flooring Transitions', 'key': 'flooring_transitions', 'icon': Icons.grid_on},
      {'label': 'Consistent Paint', 'key': 'consistent_paint', 'icon': Icons.format_paint},
      {'label': 'Lighting Fixtures', 'key': 'lighting_fixtures', 'icon': Icons.light},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Text('Shared Elements', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: AppTheme.accentColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                '\$${((shared['total'] as num?) ?? 0).toStringAsFixed(2)}',
                style: const TextStyle(color: AppTheme.accentColor, fontWeight: FontWeight.bold, fontSize: 13),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        Text('Costs for maintaining consistency across rooms', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
        const SizedBox(height: 12),
        ...items.map((item) {
          final cost = (shared[item['key']] as num?) ?? 0;
          return Card(
            child: ListTile(
              leading: Icon(item['icon'] as IconData, color: AppTheme.accentColor),
              title: Text(item['label'] as String),
              trailing: Text('\$${cost.toStringAsFixed(2)}',
                  style: const TextStyle(fontWeight: FontWeight.bold)),
            ),
          );
        }),
      ],
    );
  }

  Widget _buildSuggestions() {
    final suggestions = _costReport!['savings_suggestions'] as List;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Savings Suggestions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...suggestions.map((s) => Card(
              child: ListTile(
                leading: const Icon(Icons.lightbulb, color: AppTheme.warningColor),
                title: Text(s.toString(), style: const TextStyle(fontSize: 14)),
              ),
            )),
      ],
    );
  }
}
