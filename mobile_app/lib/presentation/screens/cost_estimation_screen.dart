import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class CostEstimationScreen extends StatefulWidget {
  final String designId;
  const CostEstimationScreen({super.key, required this.designId});

  @override
  State<CostEstimationScreen> createState() => _CostEstimationScreenState();
}

class _CostEstimationScreenState extends State<CostEstimationScreen> {
  final _apiService = ApiService();
  Map<String, dynamic>? _costData;
  bool _isLoading = true;
  bool _includeLabor = true;
  bool _includeDecoration = true;

  @override
  void initState() {
    super.initState();
    _loadCost();
  }

  Future<void> _loadCost() async {
    setState(() => _isLoading = true);
    try {
      final data = await _apiService.calculateCost(
        designId: widget.designId,
        includeLabor: _includeLabor,
        includeDecoration: _includeDecoration,
      );
      setState(() {
        _costData = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Cost Estimation')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _costData == null
              ? const Center(child: Text('Failed to load cost data'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildTotalCard(),
                      const SizedBox(height: 20),
                      _buildToggleOptions(),
                      const SizedBox(height: 20),
                      const Text('Cost Breakdown', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 12),
                      _buildBreakdownList(),
                      const SizedBox(height: 20),
                      if (_costData!['savings_suggestions'] != null) _buildSuggestions(),
                    ],
                  ),
                ),
    );
  }

  Widget _buildTotalCard() {
    final breakdown = _costData!['breakdown'] ?? {};
    final total = breakdown['total_cost'] ?? 0.0;
    final status = _costData!['budget_status'] ?? 'unknown';

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
          const Text('Estimated Total Cost', style: TextStyle(color: Colors.white70, fontSize: 14)),
          const SizedBox(height: 8),
          Text('\$${total.toStringAsFixed(2)}',
              style: const TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
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

  Widget _buildToggleOptions() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            SwitchListTile(
              title: const Text('Include Labor Costs'),
              value: _includeLabor,
              onChanged: (v) {
                setState(() => _includeLabor = v);
                _loadCost();
              },
            ),
            SwitchListTile(
              title: const Text('Include Decoration'),
              value: _includeDecoration,
              onChanged: (v) {
                setState(() => _includeDecoration = v);
                _loadCost();
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBreakdownList() {
    final breakdown = _costData!['breakdown'] ?? {};
    final items = <MapEntry<String, dynamic>>[
      MapEntry('Furniture', breakdown['furniture_cost'] ?? 0),
      MapEntry('Decoration', breakdown['decoration_cost'] ?? 0),
      MapEntry('Lighting', breakdown['lighting_cost'] ?? 0),
      MapEntry('Flooring', breakdown['flooring_cost'] ?? 0),
      MapEntry('Labor', breakdown['labor_cost'] ?? 0),
    ];

    final icons = [Icons.chair, Icons.palette, Icons.light, Icons.grid_on, Icons.construction];
    final colors = [AppTheme.primaryColor, AppTheme.secondaryColor, AppTheme.warningColor, AppTheme.accentColor, AppTheme.successColor];

    return Column(
      children: List.generate(items.length, (i) {
        return Card(
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: colors[i].withOpacity(0.1),
              child: Icon(icons[i], color: colors[i], size: 20),
            ),
            title: Text(items[i].key),
            trailing: Text(
              '\$${(items[i].value as num).toStringAsFixed(2)}',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
          ),
        );
      }),
    );
  }

  Widget _buildSuggestions() {
    final suggestions = _costData!['savings_suggestions'] as List;
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
