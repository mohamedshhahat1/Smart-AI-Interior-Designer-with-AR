import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/data/models/design_model.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class DesignResultScreen extends StatefulWidget {
  final String roomId;
  final String? style;
  const DesignResultScreen({super.key, required this.roomId, this.style});

  @override
  State<DesignResultScreen> createState() => _DesignResultScreenState();
}

class _DesignResultScreenState extends State<DesignResultScreen> {
  final _apiService = ApiService();
  final _promptController = TextEditingController();
  DesignModel? _design;
  bool _isLoading = true;
  bool _isEnhancing = false;

  @override
  void initState() {
    super.initState();
    _loadOrGenerateDesign();
  }

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  Future<void> _loadOrGenerateDesign() async {
    setState(() => _isLoading = true);
    try {
      final existing = await _apiService.listDesigns(roomId: widget.roomId);
      if (existing.isNotEmpty) {
        setState(() {
          _design = existing.first;
          _isLoading = false;
        });
        return;
      }
    } catch (_) {}

    await _generateDesign();
  }

  Future<void> _generateDesign() async {
    setState(() => _isLoading = true);
    try {
      final design = await _apiService.generateDesign(
        roomId: widget.roomId,
        style: widget.style ?? 'modern',
      );
      setState(() {
        _design = design;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to generate design')),
        );
      }
    }
  }

  Future<void> _enhanceDesign() async {
    if (_design == null || _promptController.text.isEmpty) return;

    setState(() => _isEnhancing = true);
    try {
      final enhanced = await _apiService.enhanceDesign(
        designId: _design!.id,
        instruction: _promptController.text,
      );
      setState(() {
        _design = enhanced;
        _isEnhancing = false;
      });
      _promptController.clear();
    } catch (e) {
      setState(() => _isEnhancing = false);
    }
  }

  Widget _buildDesignImage() {
    final imageUrl = _design?.generatedImageUrl;
    if (imageUrl != null && imageUrl.isNotEmpty) {
      return ClipRRect(
        borderRadius: BorderRadius.circular(16),
        child: Image.network(
          imageUrl,
          width: double.infinity,
          height: 300,
          fit: BoxFit.cover,
          errorBuilder: (context, error, stackTrace) => _buildImagePlaceholder(),
          loadingBuilder: (context, child, loadingProgress) {
            if (loadingProgress == null) return child;
            return Container(
              width: double.infinity,
              height: 300,
              color: Colors.grey[200],
              child: const Center(child: CircularProgressIndicator()),
            );
          },
        ),
      );
    }
    return _buildImagePlaceholder();
  }

  Widget _buildImagePlaceholder() {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: double.infinity,
        height: 300,
        color: Colors.grey[200],
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.image, size: 64, color: Colors.grey),
              SizedBox(height: 8),
              Text('Design Generated', style: TextStyle(color: Colors.grey)),
              SizedBox(height: 4),
              Text('Image preview not available',
                  style: TextStyle(color: Colors.grey, fontSize: 12)),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Design Result'),
        actions: [
          if (_design != null) ...[
            IconButton(
              icon: const Icon(Icons.refresh),
              onPressed: _generateDesign,
              tooltip: 'Regenerate Design',
            ),
            IconButton(
              icon: const Icon(Icons.view_in_ar),
              onPressed: () => context.go('/ar/${_design!.id}'),
              tooltip: 'View in AR',
            ),
            IconButton(
              icon: const Icon(Icons.calculate),
              onPressed: () => context.go('/cost/${_design!.id}'),
              tooltip: 'Cost Estimation',
            ),
          ],
        ],
      ),
      body: _isLoading
          ? const Center(
              child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircularProgressIndicator(),
                SizedBox(height: 16),
                Text('Generating your design...'),
              ],
            ))
          : _design == null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('Failed to generate design'),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _generateDesign,
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                )
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildDesignImage(),
                      const SizedBox(height: 16),
                      if (_design!.style != null)
                        Chip(
                            label: Text(_design!.style!),
                            backgroundColor:
                                AppTheme.primaryColor.withOpacity(0.1)),
                      const SizedBox(height: 16),
                      if (_design!.estimatedCost != null)
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Row(
                              children: [
                                const Icon(Icons.attach_money,
                                    color: AppTheme.successColor),
                                const SizedBox(width: 8),
                                Text(
                                    'Estimated Cost: \$${_design!.estimatedCost!.toStringAsFixed(2)}',
                                    style: const TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold)),
                              ],
                            ),
                          ),
                        ),
                      if (_design!.furnitureList != null &&
                          _design!.furnitureList!.isNotEmpty) ...[
                        const SizedBox(height: 16),
                        const Text('Furniture',
                            style: TextStyle(
                                fontSize: 18, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        ..._design!.furnitureList!.take(5).map((item) => Card(
                              child: ListTile(
                                leading: const Icon(Icons.chair,
                                    color: AppTheme.primaryColor),
                                title: Text(
                                    item['name']?.toString() ?? 'Furniture'),
                                subtitle: item['category'] != null
                                    ? Text(item['category'].toString())
                                    : null,
                                trailing: item['price'] != null
                                    ? Text(
                                        '\$${(item['price'] as num).toStringAsFixed(0)}',
                                        style: const TextStyle(
                                            fontWeight: FontWeight.bold))
                                    : null,
                              ),
                            )),
                      ],
                      const SizedBox(height: 24),
                      const Text('Refine Your Design',
                          style: TextStyle(
                              fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: TextField(
                              controller: _promptController,
                              decoration: const InputDecoration(
                                hintText:
                                    'e.g., Make the room look larger...',
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          IconButton(
                            onPressed: _isEnhancing ? null : _enhanceDesign,
                            icon: _isEnhancing
                                ? const SizedBox(
                                    height: 20,
                                    width: 20,
                                    child: CircularProgressIndicator(
                                        strokeWidth: 2))
                                : const Icon(Icons.send,
                                    color: AppTheme.primaryColor),
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),
                      Row(
                        children: [
                          Expanded(
                            child: OutlinedButton.icon(
                              onPressed: () =>
                                  context.go('/ar/${_design!.id}'),
                              icon: const Icon(Icons.view_in_ar),
                              label: const Text('View in AR'),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: ElevatedButton.icon(
                              onPressed: () =>
                                  context.go('/cost/${_design!.id}'),
                              icon: const Icon(Icons.calculate),
                              label: const Text('Get Cost'),
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
                ),
    );
  }
}
