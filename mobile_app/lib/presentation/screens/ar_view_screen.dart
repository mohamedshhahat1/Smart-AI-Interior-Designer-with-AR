import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';

class ARViewScreen extends StatefulWidget {
  final String designId;
  const ARViewScreen({super.key, required this.designId});

  @override
  State<ARViewScreen> createState() => _ARViewScreenState();
}

class _ARViewScreenState extends State<ARViewScreen> {
  bool _isARReady = false;
  bool _showFurniturePanel = false;
  final List<String> _placedItems = [];

  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _isARReady = true);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.white,
        title: const Text('AR View'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => setState(() {
              _placedItems.clear();
              _isARReady = false;
              Future.delayed(const Duration(seconds: 1), () {
                if (mounted) setState(() => _isARReady = true);
              });
            }),
          ),
        ],
      ),
      body: Stack(
        children: [
          Container(
            width: double.infinity,
            height: double.infinity,
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [Colors.grey[900]!, Colors.grey[800]!],
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
              ),
            ),
            child: Center(
              child: _isARReady
                  ? Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.view_in_ar, size: 80, color: Colors.white.withOpacity(0.5)),
                        const SizedBox(height: 16),
                        Text(
                          'AR Camera View',
                          style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 18),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Point your camera at a flat surface',
                          style: TextStyle(color: Colors.white.withOpacity(0.5)),
                        ),
                        if (_placedItems.isNotEmpty) ...[
                          const SizedBox(height: 24),
                          Text(
                            '${_placedItems.length} items placed',
                            style: const TextStyle(color: AppTheme.successColor, fontSize: 16),
                          ),
                        ],
                      ],
                    )
                  : const Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(color: Colors.white),
                        SizedBox(height: 16),
                        Text('Initializing AR...', style: TextStyle(color: Colors.white70)),
                      ],
                    ),
            ),
          ),
          if (_isARReady)
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: _buildBottomPanel(),
            ),
        ],
      ),
    );
  }

  Widget _buildBottomPanel() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.8),
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _buildARButton(Icons.chair, 'Sofa', () => _placeFurniture('Sofa')),
              _buildARButton(Icons.table_bar, 'Table', () => _placeFurniture('Table')),
              _buildARButton(Icons.light, 'Lamp', () => _placeFurniture('Lamp')),
              _buildARButton(Icons.more_horiz, 'More', () => setState(() => _showFurniturePanel = !_showFurniturePanel)),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.camera),
                  label: const Text('Capture'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryColor,
                    foregroundColor: Colors.white,
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.share, color: Colors.white),
                  label: const Text('Share', style: TextStyle(color: Colors.white)),
                  style: OutlinedButton.styleFrom(side: const BorderSide(color: Colors.white54)),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildARButton(IconData icon, String label, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.15),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: Colors.white, size: 24),
          ),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
        ],
      ),
    );
  }

  void _placeFurniture(String item) {
    setState(() => _placedItems.add(item));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$item placed in scene'),
        duration: const Duration(seconds: 1),
      ),
    );
  }
}
