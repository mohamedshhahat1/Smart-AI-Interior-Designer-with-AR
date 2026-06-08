import 'dart:async';

import 'package:flutter/material.dart';
import 'package:model_viewer_plus/model_viewer_plus.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/walkthrough_3d_model.dart';

class Walkthrough3DScreen extends StatefulWidget {
  const Walkthrough3DScreen({super.key});

  @override
  State<Walkthrough3DScreen> createState() => _Walkthrough3DScreenState();
}

class _Walkthrough3DScreenState extends State<Walkthrough3DScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  String _selectedQuality = 'standard';
  String _selectedMethod = 'depth_estimation';
  bool _isGenerating = false;
  Room3DModelData? _model;
  int _currentCameraIndex = 0;
  bool _isWalkthroughPlaying = false;

  final _qualities = {
    'draft': 'Draft',
    'standard': 'Standard',
    'high': 'High',
    'ultra': 'Ultra'
  };
  Timer? _walkthroughTimer;

  final _methods = {
    'depth_estimation': {
      'label': 'Depth Estimation',
      'icon': Icons.layers,
      'desc': 'Fast single-image 3D from depth map'
    },
  };

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _walkthroughTimer?.cancel();
    super.dispose();
  }

  Future<void> _generate() async {
    setState(() => _isGenerating = true);
    try {
      final response = await ApiClient().dio.post('/3d/generate', data: {
        'name': 'My 3D Room',
        'room_type': 'living_room',
        'quality_level': _selectedQuality,
        'reconstruction_method': _selectedMethod,
        'include_furniture': true,
        'include_lighting': true,
        'generate_walkthrough_path': true,
        'output_formats': ['glb'],
      });
      setState(() {
        _model = Room3DModelData.fromJson(response.data);
        _isGenerating = false;
        _tabController.animateTo(1);
      });
    } catch (e) {
      setState(() => _isGenerating = false);
      if (mounted)
        ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('3D generation failed')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('3D Walkthrough'),
        bottom: TabBar(controller: _tabController, tabs: const [
          Tab(icon: Icon(Icons.settings), text: 'Generate'),
          Tab(icon: Icon(Icons.view_in_ar), text: '3D View'),
          Tab(icon: Icon(Icons.route), text: 'Walkthrough'),
        ]),
      ),
      body: TabBarView(controller: _tabController, children: [
        _buildGenerateTab(),
        _buildViewerTab(),
        _buildWalkthroughTab(),
      ]),
    );
  }

  Widget _buildGenerateTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Reconstruction Method',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...(_methods.entries.map((e) {
          final isSelected = _selectedMethod == e.key;
          return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: GestureDetector(
                onTap: () => setState(() => _selectedMethod = e.key),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: isSelected
                        ? AppTheme.primaryColor.withOpacity(0.08)
                        : Colors.grey[50],
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(
                        color: isSelected
                            ? AppTheme.primaryColor
                            : Colors.grey[300]!,
                        width: isSelected ? 2 : 1),
                  ),
                  child: Row(children: [
                    Icon(e.value['icon'] as IconData,
                        color: isSelected ? AppTheme.primaryColor : Colors.grey,
                        size: 28),
                    const SizedBox(width: 14),
                    Expanded(
                        child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                          Text(e.value['label'] as String,
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: isSelected
                                      ? AppTheme.primaryColor
                                      : Colors.black87)),
                          Text(e.value['desc'] as String,
                              style: TextStyle(
                                  fontSize: 12, color: Colors.grey[600])),
                        ])),
                    if (isSelected)
                      const Icon(Icons.check_circle,
                          color: AppTheme.primaryColor),
                  ]),
                ),
              ));
        })),
        const SizedBox(height: 24),
        const Text('Quality Level',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Row(
            children: _qualities.entries.map((e) {
          final isSelected = _selectedQuality == e.key;
          final icons = {
            'draft': Icons.speed,
            'standard': Icons.tune,
            'high': Icons.hd,
            'ultra': Icons.four_k
          };
          return Expanded(
              child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: GestureDetector(
              onTap: () => setState(() => _selectedQuality = e.key),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 16),
                decoration: BoxDecoration(
                  color: isSelected
                      ? AppTheme.secondaryColor.withOpacity(0.1)
                      : Colors.grey[100],
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                      color: isSelected
                          ? AppTheme.secondaryColor
                          : Colors.grey[300]!),
                ),
                child: Column(children: [
                  Icon(icons[e.key],
                      color: isSelected ? AppTheme.secondaryColor : Colors.grey,
                      size: 24),
                  const SizedBox(height: 6),
                  Text(e.value,
                      style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                          color: isSelected
                              ? AppTheme.secondaryColor
                              : Colors.grey[700])),
                ]),
              ),
            ),
          ));
        }).toList()),
        const SizedBox(height: 24),
        _buildInfoCard(),
        const SizedBox(height: 24),
        SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isGenerating ? null : _generate,
              icon: _isGenerating
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                          strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.view_in_ar),
              label: Text(_isGenerating
                  ? 'Generating 3D Model...'
                  : 'Generate 3D Room'),
              style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryColor,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16)),
            )),
      ]),
    );
  }

  Widget _buildInfoCard() {
    final info = {
      'draft': {'polys': '~5K', 'time': '~2s', 'size': '~0.5 MB'},
      'standard': {'polys': '~15K', 'time': '~8s', 'size': '~2 MB'},
      'high': {'polys': '~25K', 'time': '~20s', 'size': '~4 MB'},
      'ultra': {'polys': '~45K', 'time': '~60s', 'size': '~8 MB'},
    };
    final q = info[_selectedQuality]!;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
          color: Colors.blue[50], borderRadius: BorderRadius.circular(12)),
      child: Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
        _infoItem('Polygons', q['polys']!),
        _infoItem('Time', q['time']!),
        _infoItem('Size', q['size']!),
      ]),
    );
  }

  Widget _infoItem(String label, String value) => Column(children: [
        Text(value,
            style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 16,
                color: AppTheme.primaryColor)),
        Text(label, style: TextStyle(fontSize: 11, color: Colors.grey[600])),
      ]);

  Widget _buildViewerTab() {
    if (_model == null)
      return _emptyState('Generate a 3D model first', Icons.view_in_ar);

    final glbUrl = _model!.glbModelUrl;
    if (glbUrl == null || glbUrl.isEmpty) {
      return _emptyState('No 3D model file available', Icons.error_outline);
    }

    return Column(children: [
      Expanded(
        child: ModelViewer(
          src: glbUrl,
          alt: '3D Room Model',
          ar: true,
          autoRotate: true,
          cameraControls: true,
          backgroundColor: const Color(0xFF1A1A2E),
        ),
      ),
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        color: Colors.grey[100],
        child: Row(children: [
          Text(
              '${_model!.polygonCount ?? 0} polygons • ${_model!.fileSizeMb?.toStringAsFixed(1) ?? "?"} MB',
              style: TextStyle(fontSize: 12, color: Colors.grey[600])),
          const Spacer(),
          if (_model!.furnitureObjects != null)
            Text('${_model!.furnitureObjects!.length} objects',
                style: TextStyle(fontSize: 12, color: Colors.grey[600])),
        ]),
      ),
      if (_model!.cameraPositions != null) _buildCameraBar(),
    ]);
  }

  Widget _buildCameraBar() {
    return Container(
      padding: const EdgeInsets.all(12),
      color: Colors.grey[100],
      child: Column(children: [
        const Text('Camera Positions',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
        const SizedBox(height: 8),
        SizedBox(
            height: 40,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: _model!.cameraPositions!.length,
              itemBuilder: (ctx, i) {
                final cam = _model!.cameraPositions![i];
                final isSelected = _currentCameraIndex == i;
                return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label:
                          Text(cam.label, style: const TextStyle(fontSize: 11)),
                      selected: isSelected,
                      onSelected: (_) =>
                          setState(() => _currentCameraIndex = i),
                      selectedColor: AppTheme.primaryColor.withOpacity(0.2),
                    ));
              },
            )),
      ]),
    );
  }

  Widget _buildWalkthroughTab() {
    if (_model == null || _model!.walkthroughPath == null)
      return _emptyState(
          'Generate a model with walkthrough enabled', Icons.route);

    return SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
                gradient: const LinearGradient(
                    colors: [Color(0xFF1A1A2E), Color(0xFF16213E)]),
                borderRadius: BorderRadius.circular(20)),
            child: Column(children: [
              const Icon(Icons.route, color: Colors.white, size: 40),
              const SizedBox(height: 12),
              const Text('Interactive Walkthrough',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text(
                  '${_model!.walkthroughPath!.length} waypoints • ${_totalDuration().toStringAsFixed(0)}s total',
                  style: TextStyle(color: Colors.white.withOpacity(0.7))),
              const SizedBox(height: 16),
              SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _toggleWalkthrough,
                    icon: Icon(
                        _isWalkthroughPlaying ? Icons.pause : Icons.play_arrow),
                    label: Text(_isWalkthroughPlaying
                        ? 'Pause Walkthrough'
                        : 'Start Walkthrough'),
                    style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: const Color(0xFF1A1A2E)),
                  )),
            ]),
          ),
          const SizedBox(height: 20),
          const Text('Walkthrough Path',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          ...List.generate(_model!.walkthroughPath!.length, (i) {
            final point = _model!.walkthroughPath![i];
            final isActive = _isWalkthroughPlaying && _currentCameraIndex == i;
            return Card(
                margin: const EdgeInsets.only(bottom: 8),
                color: isActive
                    ? AppTheme.primaryColor.withOpacity(0.08)
                    : null,
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundColor: isActive
                        ? AppTheme.primaryColor
                        : AppTheme.primaryColor.withOpacity(0.1),
                    child: Text('${i + 1}',
                        style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: isActive
                                ? Colors.white
                                : AppTheme.primaryColor)),
                  ),
                  title: Text('Waypoint ${i + 1}',
                      style: const TextStyle(fontWeight: FontWeight.w600)),
                  subtitle: Text(
                    'Pos: (${point.position['x']?.toStringAsFixed(1)}, ${point.position['y']?.toStringAsFixed(1)}, ${point.position['z']?.toStringAsFixed(1)}) • ${point.durationSeconds.toStringAsFixed(1)}s • ${point.easing.replaceAll('_', ' ')}',
                    style: const TextStyle(fontSize: 12),
                  ),
                  trailing: const Icon(Icons.videocam, color: Colors.grey),
                ));
          }),
          const SizedBox(height: 16),
          if (_model!.furnitureObjects != null) ...[
            Text('Scene Objects (${_model!.furnitureObjects!.length})',
                style:
                    const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            ..._model!.furnitureObjects!.map((f) => Card(
                    child: ListTile(
                  leading: CircleAvatar(
                      backgroundColor: AppTheme.accentColor.withOpacity(0.1),
                      child: const Icon(Icons.chair,
                          color: AppTheme.accentColor, size: 18)),
                  title: Text(f.name,
                      style: const TextStyle(
                          fontWeight: FontWeight.w600, fontSize: 14)),
                  subtitle: Text('${f.category} • ${f.material ?? "default"}',
                      style: const TextStyle(fontSize: 12)),
                  trailing: Text(
                      '(${f.position['x']?.toStringAsFixed(1)}, ${f.position['z']?.toStringAsFixed(1)})',
                      style: TextStyle(color: Colors.grey[500], fontSize: 11)),
                ))),
          ],
        ]));
  }

  void _toggleWalkthrough() {
    setState(() {
      _isWalkthroughPlaying = !_isWalkthroughPlaying;
      if (_isWalkthroughPlaying) {
        final path = _model!.walkthroughPath!;
        _walkthroughTimer?.cancel();
        _walkthroughTimer = Timer.periodic(
          Duration(
              milliseconds:
                  (path[_currentCameraIndex].durationSeconds * 1000).round()),
          (_) {
            if (!mounted) {
              _walkthroughTimer?.cancel();
              return;
            }
            setState(() {
              _currentCameraIndex =
                  (_currentCameraIndex + 1) % path.length;
              if (_currentCameraIndex == 0) {
                _isWalkthroughPlaying = false;
                _walkthroughTimer?.cancel();
              }
            });
          },
        );
      } else {
        _walkthroughTimer?.cancel();
      }
    });
  }

  double _totalDuration() =>
      _model!.walkthroughPath!.fold(0.0, (sum, p) => sum + p.durationSeconds);

  Widget _emptyState(String msg, IconData icon) => Center(
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Icon(icon, size: 64, color: Colors.grey[300]),
        const SizedBox(height: 16),
        Text(msg, style: TextStyle(color: Colors.grey[500], fontSize: 16)),
      ]));
}
