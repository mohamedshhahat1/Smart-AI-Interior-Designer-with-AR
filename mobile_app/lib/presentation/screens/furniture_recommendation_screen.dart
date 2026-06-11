import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/data/models/furniture_model.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';
import 'package:smart_interior_ai/presentation/widgets/furniture_card.dart';

class FurnitureRecommendationScreen extends StatefulWidget {
  final String roomId;

  const FurnitureRecommendationScreen({super.key, required this.roomId});

  @override
  State<FurnitureRecommendationScreen> createState() =>
      _FurnitureRecommendationScreenState();
}

class _FurnitureRecommendationScreenState
    extends State<FurnitureRecommendationScreen> {
  final _apiService = ApiService();
  final _budgetController = TextEditingController();
  List<FurnitureModel> _recommendations = [];
  String _style = 'modern';
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadRecommendations();
  }

  @override
  void dispose() {
    _budgetController.dispose();
    super.dispose();
  }

  Future<void> _loadRecommendations() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });
    try {
      final budget = double.tryParse(_budgetController.text.trim());
      final recommendations = await _apiService.recommendFurniture(
        roomId: widget.roomId,
        style: _style,
        budget: budget,
      );
      if (!mounted) return;
      setState(() {
        _recommendations = recommendations;
        _isLoading = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _error = 'Could not load furniture recommendations.';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final total = _recommendations.fold<double>(
      0,
      (sum, item) => sum + item.price,
    );

    return Scaffold(
      appBar: AppBar(title: const Text('Furniture Recommendations')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                DropdownButtonFormField<String>(
                  value: _style,
                  decoration: const InputDecoration(
                    labelText: 'Style',
                    prefixIcon: Icon(Icons.palette_outlined),
                  ),
                  items: AppConstants.supportedStyles
                      .map(
                        (style) => DropdownMenuItem(
                          value: style.toLowerCase(),
                          child: Text(style),
                        ),
                      )
                      .toList(),
                  onChanged: (value) {
                    if (value != null) setState(() => _style = value);
                  },
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: _budgetController,
                  keyboardType: const TextInputType.numberWithOptions(
                    decimal: true,
                  ),
                  decoration: const InputDecoration(
                    labelText: 'Maximum budget (optional)',
                    prefixIcon: Icon(Icons.attach_money),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _isLoading ? null : _loadRecommendations,
                    icon: const Icon(Icons.auto_awesome),
                    label: const Text('Refresh Recommendations'),
                  ),
                ),
              ],
            ),
          ),
          if (_recommendations.isNotEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Text('${_recommendations.length} recommendations'),
                  const Spacer(),
                  Text(
                    'Total: \$${total.toStringAsFixed(0)}',
                    style: const TextStyle(
                      color: AppTheme.primaryColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          const SizedBox(height: 8),
          Expanded(child: _buildContent()),
        ],
      ),
    );
  }

  Widget _buildContent() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.error_outline, size: 48, color: Colors.grey),
              const SizedBox(height: 12),
              Text(_error!, textAlign: TextAlign.center),
              const SizedBox(height: 12),
              OutlinedButton(
                onPressed: _loadRecommendations,
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }
    if (_recommendations.isEmpty) {
      return const Center(child: Text('No matching furniture was found.'));
    }
    return GridView.builder(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 0.62,
      ),
      itemCount: _recommendations.length,
      itemBuilder: (context, index) =>
          FurnitureCard(furniture: _recommendations[index]),
    );
  }
}
