import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';

class ARViewScreen extends StatefulWidget {
  final String designId;
  const ARViewScreen({super.key, required this.designId});

  @override
  State<ARViewScreen> createState() => _ARViewScreenState();
}

class _ARViewScreenState extends State<ARViewScreen> {
  CameraController? _cameraController;
  bool _isCameraReady = false;
  bool _isLoading = true;
  bool _showFurniturePanel = false;
  final List<Map<String, dynamic>> _placedItems = [];
  List<Map<String, dynamic>> _availableFurniture = [];
  String? _errorMessage;
  final GlobalKey _captureKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    _initializeCamera();
    _loadDesignData();
  }

  Future<void> _initializeCamera() async {
    final status = await Permission.camera.request();
    if (!status.isGranted) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Camera permission is required for AR view';
          _isLoading = false;
        });
      }
      return;
    }

    try {
      final cameras = await availableCameras();
      if (cameras.isEmpty) {
        if (mounted) {
          setState(() {
            _errorMessage = 'No camera available on this device';
            _isLoading = false;
          });
        }
        return;
      }

      _cameraController = CameraController(
        cameras.first,
        ResolutionPreset.high,
        enableAudio: false,
      );

      await _cameraController!.initialize();
      if (mounted) {
        setState(() {
          _isCameraReady = true;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Failed to initialize camera';
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _loadDesignData() async {
    try {
      final response = await ApiClient().dio.get('/design/${widget.designId}');
      final data = response.data;
      final furnitureList = data['furniture_list'];

      if (furnitureList != null && mounted) {
        List<Map<String, dynamic>> items = [];
        if (furnitureList is List) {
          items = furnitureList.cast<Map<String, dynamic>>();
        } else if (furnitureList is Map) {
          furnitureList.forEach((key, value) {
            items.add({
              'name': key,
              'category': value is Map ? value['category'] ?? 'furniture' : 'furniture',
              'icon': _iconForCategory(key.toString()),
            });
          });
        }

        setState(() => _availableFurniture = items);
      }
    } catch (e) {
      _availableFurniture = [
        {'name': 'Sofa', 'category': 'seating', 'icon': Icons.chair},
        {'name': 'Table', 'category': 'table', 'icon': Icons.table_bar},
        {'name': 'Lamp', 'category': 'lighting', 'icon': Icons.light},
        {'name': 'Bookshelf', 'category': 'storage', 'icon': Icons.shelves},
        {'name': 'Plant', 'category': 'decor', 'icon': Icons.yard},
        {'name': 'Rug', 'category': 'decor', 'icon': Icons.rectangle},
      ];
      if (mounted) setState(() {});
    }
  }

  IconData _iconForCategory(String name) {
    final lower = name.toLowerCase();
    if (lower.contains('sofa') || lower.contains('chair') || lower.contains('seat')) return Icons.chair;
    if (lower.contains('table') || lower.contains('desk')) return Icons.table_bar;
    if (lower.contains('lamp') || lower.contains('light')) return Icons.light;
    if (lower.contains('shelf') || lower.contains('cabinet')) return Icons.shelves;
    if (lower.contains('plant')) return Icons.yard;
    if (lower.contains('bed')) return Icons.bed;
    if (lower.contains('rug') || lower.contains('carpet')) return Icons.rectangle;
    return Icons.widgets;
  }

  Future<void> _captureScene() async {
    try {
      if (_cameraController != null && _cameraController!.value.isInitialized) {
        final image = await _cameraController!.takePicture();
        final dir = await getApplicationDocumentsDirectory();
        final timestamp = DateTime.now().millisecondsSinceEpoch;
        final savedPath = '${dir.path}/ar_capture_$timestamp.jpg';
        await File(image.path).copy(savedPath);

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Scene captured and saved'),
              action: SnackBarAction(
                label: 'View',
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (_) => Dialog(
                      child: Image.file(File(savedPath)),
                    ),
                  );
                },
              ),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to capture scene')),
        );
      }
    }
  }

  Future<void> _shareScene() async {
    try {
      if (_cameraController != null && _cameraController!.value.isInitialized) {
        final image = await _cameraController!.takePicture();
        final dir = await getApplicationDocumentsDirectory();
        final timestamp = DateTime.now().millisecondsSinceEpoch;
        final savedPath = '${dir.path}/ar_share_$timestamp.jpg';
        await File(image.path).copy(savedPath);

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Image saved to: $savedPath')),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to share scene')),
        );
      }
    }
  }

  void _placeFurniture(Map<String, dynamic> item) {
    setState(() => _placedItems.add(item));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('${item['name']} placed in scene'),
        duration: const Duration(seconds: 1),
      ),
    );
  }

  void _removeLastItem() {
    if (_placedItems.isNotEmpty) {
      final removed = _placedItems.removeLast();
      setState(() {});
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('${removed['name']} removed'),
          duration: const Duration(seconds: 1),
        ),
      );
    }
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
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
          if (_placedItems.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.undo),
              onPressed: _removeLastItem,
              tooltip: 'Remove last item',
            ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                _placedItems.clear();
              });
            },
          ),
        ],
      ),
      body: RepaintBoundary(
        key: _captureKey,
        child: Stack(
          children: [
            _buildCameraView(),
            if (_placedItems.isNotEmpty)
              Positioned(
                top: MediaQuery.of(context).padding.top + 56,
                left: 16,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${_placedItems.length} items placed',
                    style: const TextStyle(color: Colors.white, fontSize: 13),
                  ),
                ),
              ),
            for (int i = 0; i < _placedItems.length; i++)
              Positioned(
                left: 60.0 + (i % 3) * 100,
                top: 200.0 + (i ~/ 3) * 120,
                child: _buildPlacedItemOverlay(_placedItems[i]),
              ),
            if (_isCameraReady)
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: _buildBottomPanel(),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildCameraView() {
    if (_isLoading) {
      return Container(
        color: Colors.black,
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(color: Colors.white),
              SizedBox(height: 16),
              Text('Initializing camera...', style: TextStyle(color: Colors.white70)),
            ],
          ),
        ),
      );
    }

    if (_errorMessage != null) {
      return Container(
        color: Colors.black,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, color: Colors.white54, size: 64),
              const SizedBox(height: 16),
              Text(_errorMessage!, style: const TextStyle(color: Colors.white70)),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    _isLoading = true;
                    _errorMessage = null;
                  });
                  _initializeCamera();
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }

    if (_isCameraReady && _cameraController != null) {
      return SizedBox.expand(
        child: FittedBox(
          fit: BoxFit.cover,
          child: SizedBox(
            width: _cameraController!.value.previewSize!.height,
            height: _cameraController!.value.previewSize!.width,
            child: CameraPreview(_cameraController!),
          ),
        ),
      );
    }

    return Container(color: Colors.black);
  }

  Widget _buildPlacedItemOverlay(Map<String, dynamic> item) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: AppTheme.primaryColor.withOpacity(0.8),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white54),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            item['icon'] as IconData? ?? Icons.widgets,
            color: Colors.white,
            size: 28,
          ),
          const SizedBox(height: 2),
          Text(
            item['name'] as String? ?? 'Item',
            style: const TextStyle(color: Colors.white, fontSize: 10),
          ),
        ],
      ),
    );
  }

  Widget _buildBottomPanel() {
    final displayItems = _availableFurniture.isNotEmpty
        ? _availableFurniture.take(4).toList()
        : [
            {'name': 'Sofa', 'icon': Icons.chair},
            {'name': 'Table', 'icon': Icons.table_bar},
            {'name': 'Lamp', 'icon': Icons.light},
          ];

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
              ...displayItems.map((item) => _buildARButton(
                    item['icon'] as IconData? ?? Icons.widgets,
                    item['name'] as String? ?? 'Item',
                    () => _placeFurniture(item),
                  )),
              if (_availableFurniture.length > 4)
                _buildARButton(Icons.more_horiz, 'More', () {
                  setState(() => _showFurniturePanel = !_showFurniturePanel);
                }),
            ],
          ),
          if (_showFurniturePanel && _availableFurniture.length > 4) ...[
            const SizedBox(height: 12),
            SizedBox(
              height: 80,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: _availableFurniture.length - 4,
                itemBuilder: (context, index) {
                  final item = _availableFurniture[index + 4];
                  return Padding(
                    padding: const EdgeInsets.only(right: 12),
                    child: _buildARButton(
                      item['icon'] as IconData? ?? Icons.widgets,
                      item['name'] as String? ?? 'Item',
                      () => _placeFurniture(item),
                    ),
                  );
                },
              ),
            ),
          ],
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: _captureScene,
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
                  onPressed: _shareScene,
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
}
