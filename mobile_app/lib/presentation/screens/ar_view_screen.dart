import 'dart:io';

import 'package:flutter/material.dart';
import 'package:ar_flutter_plugin_2/ar_flutter_plugin.dart';
import 'package:ar_flutter_plugin_2/datatypes/config_planedetection.dart';
import 'package:ar_flutter_plugin_2/datatypes/hittest_result_types.dart';
import 'package:ar_flutter_plugin_2/datatypes/node_types.dart';
import 'package:ar_flutter_plugin_2/managers/ar_anchor_manager.dart';
import 'package:ar_flutter_plugin_2/managers/ar_location_manager.dart';
import 'package:ar_flutter_plugin_2/managers/ar_object_manager.dart';
import 'package:ar_flutter_plugin_2/managers/ar_session_manager.dart';
import 'package:ar_flutter_plugin_2/models/ar_anchor.dart';
import 'package:ar_flutter_plugin_2/models/ar_hittest_result.dart';
import 'package:ar_flutter_plugin_2/models/ar_node.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:vector_math/vector_math_64.dart' as vector;
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';

class ARViewScreen extends StatefulWidget {
  final String designId;
  const ARViewScreen({super.key, required this.designId});

  @override
  State<ARViewScreen> createState() => _ARViewScreenState();
}

class _ARViewScreenState extends State<ARViewScreen> {
  ARSessionManager? _arSessionManager;
  ARObjectManager? _arObjectManager;
  ARAnchorManager? _arAnchorManager;

  bool _isLoading = true;
  bool _planesDetected = false;
  bool _showFurniturePanel = false;
  String? _errorMessage;
  String? _selectedFurniture;

  List<Map<String, dynamic>> _availableFurniture = [];
  final List<ARNode> _placedNodes = [];
  final List<ARAnchor> _placedAnchors = [];
  List<Map<String, dynamic>> _sceneObjects = [];

  static const _base = 'https://raw.githubusercontent.com/ToxSam/cc0-models-Polygonal-Mind/main/projects';

  static final _default3DModels = <String, String>{
    'Sofa': '$_base/avatar-show/Sofa.glb',
    'Table': '$_base/avatar-show/Table.glb',
    'Lamp': '$_base/avatar-show/Lamp_Stand.glb',
    'Chair': '$_base/avatar-show/Arm_Chair.glb',
    'Bookshelf': '$_base/ca-world/Shelf_01_a.glb',
    'Plant': '$_base/avatar-show/Banana_Plant.glb',
    'Carpet': '$_base/avatar-show/Carpet.glb',
    'Bench': '$_base/ca-world/Bench_01.glb',
    'Stool': '$_base/ca-world/Stool_01.glb',
  };

  static String _resolveModelUrl(String name) {
    final lower = name.toLowerCase();
    for (final entry in _default3DModels.entries) {
      if (lower.contains(entry.key.toLowerCase())) return entry.value;
    }
    if (lower.contains('couch') || lower.contains('loveseat')) {
      return _default3DModels['Sofa']!;
    }
    if (lower.contains('desk') || lower.contains('coffee table') || lower.contains('dining')) {
      return _default3DModels['Table']!;
    }
    if (lower.contains('light') || lower.contains('chandelier') || lower.contains('sconce')) {
      return _default3DModels['Lamp']!;
    }
    if (lower.contains('seat') || lower.contains('armchair') || lower.contains('recliner')) {
      return _default3DModels['Chair']!;
    }
    if (lower.contains('cabinet') || lower.contains('shelf') || lower.contains('storage')) {
      return _default3DModels['Bookshelf']!;
    }
    if (lower.contains('flower') || lower.contains('pot') || lower.contains('tree') || lower.contains('fern')) {
      return _default3DModels['Plant']!;
    }
    if (lower.contains('rug') || lower.contains('mat')) {
      return _default3DModels['Carpet']!;
    }
    return _default3DModels['Chair']!;
  }

  @override
  void initState() {
    super.initState();
    _checkPermissionsAndLoadData();
  }

  Future<void> _checkPermissionsAndLoadData() async {
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
    await _loadDesignData();
    if (mounted) setState(() => _isLoading = false);
  }

  Future<void> _loadDesignData() async {
    try {
      final designResponse = await ApiClient().dio.get('/design/${widget.designId}');
      final data = designResponse.data;
      final furnitureList = data['furniture_list'];

      List<Map<String, dynamic>> items = [];
      if (furnitureList is List) {
        items = furnitureList.cast<Map<String, dynamic>>();
      } else if (furnitureList is Map) {
        furnitureList.forEach((key, value) {
          items.add({
            'name': key.toString(),
            'category': value is Map ? value['category'] ?? 'furniture' : 'furniture',
            'model_3d_url': value is Map ? value['model_3d_url'] : null,
          });
        });
      }

      try {
        final arResponse = await ApiClient().dio.post('/ar/generate-scene', data: {
          'design_id': widget.designId,
        });
        final arData = arResponse.data;
        _sceneObjects = (arData['scene_objects'] as List?)?.cast<Map<String, dynamic>>() ?? [];
      } catch (_) {}

      if (items.isEmpty) {
        items = _default3DModels.entries
            .map((e) => {'name': e.key, 'category': 'furniture', 'model_3d_url': e.value})
            .toList();
      }

      if (mounted) setState(() => _availableFurniture = items);
    } catch (e) {
      if (mounted) {
        setState(() {
          _availableFurniture = _default3DModels.entries
              .map((e) => {'name': e.key, 'category': 'furniture', 'model_3d_url': e.value})
              .toList();
        });
      }
    }
  }

  void _onARViewCreated(
    ARSessionManager arSessionManager,
    ARObjectManager arObjectManager,
    ARAnchorManager arAnchorManager,
    ARLocationManager arLocationManager,
  ) {
    _arSessionManager = arSessionManager;
    _arObjectManager = arObjectManager;
    _arAnchorManager = arAnchorManager;

    _arSessionManager!.onInitialize(
      showFeaturePoints: false,
      showPlanes: true,
      showWorldOrigin: false,
      handlePans: true,
      handleRotation: true,
    );

    _arObjectManager!.onInitialize();
    _arSessionManager!.onPlaneOrPointTap = _onPlaneOrPointTapped;

    _arAnchorManager!.initAnchorManager();
  }

  Future<void> _onPlaneOrPointTapped(List<ARHitTestResult> hitTestResults) async {
    if (_selectedFurniture == null || hitTestResults.isEmpty) return;

    final hit = hitTestResults.firstWhere(
      (r) => r.type == ARHitTestResultType.plane,
      orElse: () => hitTestResults.first,
    );

    if (!_planesDetected && mounted) {
      setState(() => _planesDetected = true);
    }

    final item = _availableFurniture.firstWhere(
      (f) => f['name'] == _selectedFurniture,
      orElse: () => _availableFurniture.first,
    );

    final sceneObj = _sceneObjects.firstWhere(
      (s) => s['name'] == _selectedFurniture,
      orElse: () => {},
    );

    final scale = sceneObj.isNotEmpty && sceneObj['scale'] != null
        ? vector.Vector3(
            (sceneObj['scale']['x'] as num?)?.toDouble() ?? 0.2,
            (sceneObj['scale']['y'] as num?)?.toDouble() ?? 0.2,
            (sceneObj['scale']['z'] as num?)?.toDouble() ?? 0.2,
          )
        : vector.Vector3(0.2, 0.2, 0.2);

    final modelUrl = item['model_3d_url'] as String?;
    final resolvedUrl = (modelUrl != null && modelUrl.isNotEmpty && !modelUrl.contains('Astronaut'))
        ? modelUrl
        : _resolveModelUrl(item['name'] as String? ?? 'Chair');

    final newNode = ARNode(
      type: NodeType.webGLB,
      uri: resolvedUrl,
      scale: scale,
      position: hit.worldTransform.getTranslation(),
      rotation: vector.Vector4(1.0, 0.0, 0.0, 0.0),
      name: '${_selectedFurniture}_${_placedNodes.length}',
    );

    final newAnchor = ARPlaneAnchor(
      transformation: hit.worldTransform,
      name: 'anchor_${_placedAnchors.length}',
    );

    bool? didAddAnchor = await _arAnchorManager?.addAnchor(newAnchor);
    if (didAddAnchor == true) {
      bool? didAddNode = await _arObjectManager?.addNode(newNode, planeAnchor: newAnchor);
      if (didAddNode == true) {
        _placedNodes.add(newNode);
        _placedAnchors.add(newAnchor);
        if (mounted) setState(() {});

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('$_selectedFurniture placed on surface'),
            duration: const Duration(seconds: 1),
          ),
        );
      }
    }
  }

  Future<void> _undoLastPlacement() async {
    if (_placedNodes.isEmpty) return;

    final lastNode = _placedNodes.removeLast();
    final lastAnchor = _placedAnchors.removeLast();

    await _arObjectManager?.removeNode(lastNode);
    await _arAnchorManager?.removeAnchor(lastAnchor);

    if (mounted) {
      setState(() {});
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('${lastNode.name?.split('_').first ?? "Item"} removed'),
          duration: const Duration(seconds: 1),
        ),
      );
    }
  }

  Future<void> _clearAll() async {
    for (final node in _placedNodes) {
      await _arObjectManager?.removeNode(node);
    }
    for (final anchor in _placedAnchors) {
      await _arAnchorManager?.removeAnchor(anchor);
    }
    _placedNodes.clear();
    _placedAnchors.clear();
    if (mounted) setState(() {});
  }

  Future<void> _captureScene() async {
    try {
      final image = await _arSessionManager?.snapshot();
      if (image != null) {
        final dir = await getApplicationDocumentsDirectory();
        final timestamp = DateTime.now().millisecondsSinceEpoch;
        final file = File('${dir.path}/ar_capture_$timestamp.png');
        await file.writeAsBytes(image);

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Text('AR scene captured'),
              action: SnackBarAction(
                label: 'View',
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (_) => Dialog(child: Image.file(file)),
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
          const SnackBar(content: Text('Failed to capture AR scene')),
        );
      }
    }
  }

  Future<void> _shareScene() async {
    try {
      final image = await _arSessionManager?.snapshot();
      if (image != null) {
        final dir = await getApplicationDocumentsDirectory();
        final timestamp = DateTime.now().millisecondsSinceEpoch;
        final file = File('${dir.path}/ar_share_$timestamp.png');
        await file.writeAsBytes(image);

        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('AR image saved to: ${file.path}')),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to share AR scene')),
        );
      }
    }
  }

  @override
  void dispose() {
    _arSessionManager?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(color: Colors.white),
              SizedBox(height: 16),
              Text('Preparing AR...', style: TextStyle(color: Colors.white70)),
            ],
          ),
        ),
      );
    }

    if (_errorMessage != null) {
      return Scaffold(
        backgroundColor: Colors.black,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          foregroundColor: Colors.white,
          title: const Text('AR View'),
        ),
        body: Center(
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
                  _checkPermissionsAndLoadData();
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        foregroundColor: Colors.white,
        title: const Text('AR View'),
        actions: [
          if (_placedNodes.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.undo),
              onPressed: _undoLastPlacement,
              tooltip: 'Undo last',
            ),
          IconButton(
            icon: const Icon(Icons.delete_sweep),
            onPressed: _clearAll,
            tooltip: 'Clear all',
          ),
        ],
      ),
      body: Stack(
        children: [
          ARView(
            onARViewCreated: _onARViewCreated,
            planeDetectionConfig: PlaneDetectionConfig.horizontalAndVertical,
          ),
          if (!_planesDetected)
            Positioned(
              top: MediaQuery.of(context).padding.top + 60,
              left: 0,
              right: 0,
              child: Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(25),
                  ),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SizedBox(
                        height: 16, width: 16,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                      ),
                      SizedBox(width: 10),
                      Text(
                        'Move your phone to detect surfaces...',
                        style: TextStyle(color: Colors.white, fontSize: 14),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          if (_placedNodes.isNotEmpty)
            Positioned(
              top: MediaQuery.of(context).padding.top + 60,
              left: 16,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  '${_placedNodes.length} item${_placedNodes.length > 1 ? 's' : ''} placed',
                  style: const TextStyle(color: Colors.white, fontSize: 13),
                ),
              ),
            ),
          if (_selectedFurniture != null && _planesDetected)
            Positioned(
              top: MediaQuery.of(context).padding.top + 60,
              right: 16,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: AppTheme.primaryColor,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  'Tap surface to place $_selectedFurniture',
                  style: const TextStyle(color: Colors.white, fontSize: 12),
                ),
              ),
            ),
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
    final displayItems = _availableFurniture.take(4).toList();

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.85),
        borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: SafeArea(
        top: false,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ...displayItems.map((item) {
                  final name = item['name'] as String? ?? 'Item';
                  final isSelected = _selectedFurniture == name;
                  return _buildARButton(
                    _iconForName(name),
                    name,
                    () => setState(() => _selectedFurniture = isSelected ? null : name),
                    isSelected: isSelected,
                  );
                }),
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
                    final name = item['name'] as String? ?? 'Item';
                    final isSelected = _selectedFurniture == name;
                    return Padding(
                      padding: const EdgeInsets.only(right: 12),
                      child: _buildARButton(
                        _iconForName(name),
                        name,
                        () => setState(() => _selectedFurniture = isSelected ? null : name),
                        isSelected: isSelected,
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
      ),
    );
  }

  Widget _buildARButton(IconData icon, String label, VoidCallback onTap, {bool isSelected = false}) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isSelected ? AppTheme.primaryColor : Colors.white.withOpacity(0.15),
              borderRadius: BorderRadius.circular(12),
              border: isSelected ? Border.all(color: Colors.white, width: 2) : null,
            ),
            child: Icon(icon, color: Colors.white, size: 24),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              color: isSelected ? AppTheme.primaryColor : Colors.white70,
              fontSize: 12,
              fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
            ),
          ),
        ],
      ),
    );
  }

  IconData _iconForName(String name) {
    final lower = name.toLowerCase();
    if (lower.contains('sofa') || lower.contains('couch')) return Icons.chair;
    if (lower.contains('chair') || lower.contains('seat')) return Icons.event_seat;
    if (lower.contains('table') || lower.contains('desk')) return Icons.table_bar;
    if (lower.contains('lamp') || lower.contains('light')) return Icons.light;
    if (lower.contains('shelf') || lower.contains('cabinet') || lower.contains('bookshelf')) return Icons.shelves;
    if (lower.contains('plant') || lower.contains('flower')) return Icons.yard;
    if (lower.contains('bed')) return Icons.bed;
    if (lower.contains('rug') || lower.contains('carpet')) return Icons.rectangle;
    if (lower.contains('tv') || lower.contains('screen')) return Icons.tv;
    return Icons.widgets;
  }
}
