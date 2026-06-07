import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/lighting_model.dart';

class SmartLightingScreen extends StatefulWidget {
  const SmartLightingScreen({super.key});

  @override
  State<SmartLightingScreen> createState() => _SmartLightingScreenState();
}

class _SmartLightingScreenState extends State<SmartLightingScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _moodTextController = TextEditingController();

  String? _selectedActivity;
  String? _selectedTimeOfDay;
  double _energyLevel = 0.5;
  bool _isDetecting = false;
  MoodDetectResponseModel? _result;

  bool _isLoadingCircadian = false;
  List<Map<String, dynamic>> _circadianSchedule = [];
  String _wakeTime = '07:00';
  String _sleepTime = '23:00';
  bool _circadianLoaded = false;

  bool _isSavingScene = false;
  String? _savedSceneId;
  bool _isExporting = false;

  final List<Map<String, dynamic>> _moods = [
    {'label': 'Relaxed', 'icon': Icons.spa, 'color': Color(0xFF81C784)},
    {'label': 'Focused', 'icon': Icons.psychology, 'color': Color(0xFF64B5F6)},
    {'label': 'Energetic', 'icon': Icons.bolt, 'color': Color(0xFFFFB74D)},
    {'label': 'Romantic', 'icon': Icons.favorite, 'color': Color(0xFFE57373)},
    {'label': 'Cozy', 'icon': Icons.local_fire_department, 'color': Color(0xFFFFCC80)},
    {'label': 'Creative', 'icon': Icons.palette, 'color': Color(0xFFCE93D8)},
    {'label': 'Social', 'icon': Icons.groups, 'color': Color(0xFF4DD0E1)},
    {'label': 'Sleepy', 'icon': Icons.bedtime, 'color': Color(0xFF9575CD)},
  ];

  final List<String> _activities = [
    'Relaxing', 'Working', 'Studying', 'Entertaining',
    'Sleeping', 'Cooking', 'Reading', 'Exercising',
    'Meditating', 'Dining', 'Creating', 'Gaming',
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _tabController.addListener(() {
      if (_tabController.index == 2 && !_circadianLoaded) {
        _loadCircadianSchedule();
      }
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    _moodTextController.dispose();
    super.dispose();
  }

  Future<void> _detectMood({String? quickMood}) async {
    setState(() => _isDetecting = true);
    try {
      final response = await ApiClient().dio.post('/lighting/detect-mood', data: {
        'text_input': quickMood ?? _moodTextController.text.trim().nullIfEmpty,
        'time_of_day': _selectedTimeOfDay,
        'activity': _selectedActivity?.toLowerCase(),
        'energy_level': _energyLevel,
      });
      setState(() {
        _result = MoodDetectResponseModel.fromJson(response.data);
        _isDetecting = false;
        _savedSceneId = null;
      });
    } catch (e) {
      setState(() => _isDetecting = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to detect mood')),
        );
      }
    }
  }

  Future<void> _loadCircadianSchedule() async {
    setState(() => _isLoadingCircadian = true);
    try {
      final response = await ApiClient().dio.post('/lighting/circadian', data: {
        'wake_time': _wakeTime,
        'sleep_time': _sleepTime,
      });
      final data = response.data;
      final schedule = (data['schedule'] as List?)?.cast<Map<String, dynamic>>() ?? [];
      if (mounted) {
        setState(() {
          _circadianSchedule = schedule;
          _isLoadingCircadian = false;
          _circadianLoaded = true;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoadingCircadian = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to load circadian schedule')),
        );
      }
    }
  }

  Future<void> _saveScene() async {
    if (_result == null) return;
    setState(() => _isSavingScene = true);

    try {
      final rec = _result!.recommendation;
      final analysis = _result!.moodAnalysis;

      final response = await ApiClient().dio.post('/lighting/scenes', data: {
        'name': '${analysis.detectedMood[0].toUpperCase()}${analysis.detectedMood.substring(1)} Scene',
        'mood': analysis.detectedMood,
        'color_temperature': rec.colorTemperature,
        'brightness': rec.brightness,
        'color_hex': rec.colorHex,
        'saturation': rec.saturation,
        'transition_duration': rec.transitionDuration,
        'time_of_day': rec.timeOfDay,
        'activity': _selectedActivity?.toLowerCase(),
      });

      final savedId = response.data['id'] as String?;
      if (mounted) {
        setState(() {
          _isSavingScene = false;
          _savedSceneId = savedId;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Scene saved successfully')),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isSavingScene = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to save scene')),
        );
      }
    }
  }

  Future<void> _exportToSmartHome() async {
    if (_savedSceneId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Save the scene first before exporting')),
      );
      return;
    }

    final platform = await showDialog<String>(
      context: context,
      builder: (context) => SimpleDialog(
        title: const Text('Export to Smart Home'),
        children: [
          for (final p in ['philips_hue', 'lifx', 'homekit', 'google_home', 'alexa'])
            SimpleDialogOption(
              onPressed: () => Navigator.pop(context, p),
              child: ListTile(
                leading: Icon(_platformIcon(p)),
                title: Text(_platformLabel(p)),
              ),
            ),
        ],
      ),
    );

    if (platform == null) return;

    setState(() => _isExporting = true);
    try {
      final response = await ApiClient().dio.post('/lighting/export', data: {
        'scene_id': _savedSceneId,
        'platform': platform,
      });

      final data = response.data;
      final instructions = (data['instructions'] as List?)?.cast<String>() ?? [];

      if (mounted) {
        setState(() => _isExporting = false);
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: Text('Exported to ${_platformLabel(platform)}'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Setup Instructions:', style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                ...instructions.map((i) => Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text('• $i', style: const TextStyle(fontSize: 13)),
                    )),
              ],
            ),
            actions: [
              TextButton(onPressed: () => Navigator.pop(context), child: const Text('Done')),
            ],
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isExporting = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to export scene')),
        );
      }
    }
  }

  String _platformLabel(String p) {
    const labels = {
      'philips_hue': 'Philips Hue',
      'lifx': 'LIFX',
      'homekit': 'Apple HomeKit',
      'google_home': 'Google Home',
      'alexa': 'Amazon Alexa',
    };
    return labels[p] ?? p;
  }

  IconData _platformIcon(String p) {
    const icons = {
      'philips_hue': Icons.lightbulb,
      'lifx': Icons.light_mode,
      'homekit': Icons.home,
      'google_home': Icons.speaker,
      'alexa': Icons.speaker_group,
    };
    return icons[p] ?? Icons.devices;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Lighting'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.auto_awesome), text: 'Mood'),
            Tab(icon: Icon(Icons.lightbulb), text: 'Result'),
            Tab(icon: Icon(Icons.schedule), text: 'Circadian'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildMoodTab(),
          _buildResultTab(),
          _buildCircadianTab(),
        ],
      ),
    );
  }

  Widget _buildMoodTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('How are you feeling?', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 4, mainAxisSpacing: 10, crossAxisSpacing: 10, childAspectRatio: 0.85,
            ),
            itemCount: _moods.length,
            itemBuilder: (context, i) {
              final mood = _moods[i];
              return GestureDetector(
                onTap: () => _detectMood(quickMood: 'I feel ${mood['label'].toString().toLowerCase()}'),
                child: Container(
                  decoration: BoxDecoration(
                    color: (mood['color'] as Color).withOpacity(0.15),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: (mood['color'] as Color).withOpacity(0.4)),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(mood['icon'] as IconData, color: mood['color'] as Color, size: 28),
                      const SizedBox(height: 6),
                      Text(mood['label'] as String, style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: mood['color'] as Color)),
                    ],
                  ),
                ),
              );
            },
          ),
          const SizedBox(height: 24),
          const Text('Or describe your mood', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          TextField(
            controller: _moodTextController,
            decoration: const InputDecoration(
              hintText: 'e.g. I want to relax after a long day...',
              prefixIcon: Icon(Icons.edit_note),
            ),
            maxLines: 2,
          ),
          const SizedBox(height: 20),
          const Text('Activity', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8, runSpacing: 8,
            children: _activities.map((a) => ChoiceChip(
              label: Text(a),
              selected: _selectedActivity == a,
              onSelected: (_) => setState(() => _selectedActivity = _selectedActivity == a ? null : a),
              selectedColor: AppTheme.primaryColor.withOpacity(0.2),
            )).toList(),
          ),
          const SizedBox(height: 20),
          const Text('Time of Day', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Row(
            children: ['morning', 'afternoon', 'evening', 'night'].map((t) {
              final icons = {'morning': Icons.wb_sunny, 'afternoon': Icons.wb_cloudy, 'evening': Icons.wb_twilight, 'night': Icons.nightlight};
              final isSelected = _selectedTimeOfDay == t;
              return Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  child: ChoiceChip(
                    avatar: Icon(icons[t], size: 16),
                    label: Text(t[0].toUpperCase() + t.substring(1), style: const TextStyle(fontSize: 11)),
                    selected: isSelected,
                    onSelected: (_) => setState(() => _selectedTimeOfDay = isSelected ? null : t),
                    selectedColor: AppTheme.warningColor.withOpacity(0.2),
                  ),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              const Text('Energy Level', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const Spacer(),
              Text('${(_energyLevel * 100).round()}%', style: const TextStyle(fontWeight: FontWeight.w600)),
            ],
          ),
          Slider(
            value: _energyLevel,
            onChanged: (v) => setState(() => _energyLevel = v),
            activeColor: AppTheme.primaryColor,
            divisions: 20,
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isDetecting ? null : () => _detectMood(),
              icon: _isDetecting
                  ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.auto_awesome),
              label: Text(_isDetecting ? 'Detecting Mood...' : 'Detect Mood & Recommend'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryColor, foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultTab() {
    if (_result == null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.lightbulb_outline, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text('Detect your mood first', style: TextStyle(color: Colors.grey[500], fontSize: 16)),
          ],
        ),
      );
    }

    final analysis = _result!.moodAnalysis;
    final rec = _result!.recommendation;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [_moodColor(analysis.detectedMood), _moodColor(analysis.detectedMood).withOpacity(0.6)],
              ),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Column(
              children: [
                Text('Detected Mood', style: TextStyle(color: Colors.white.withOpacity(0.8))),
                const SizedBox(height: 4),
                Text(analysis.detectedMood.toUpperCase(), style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                Text('${(analysis.confidence * 100).round()}% confidence', style: TextStyle(color: Colors.white.withOpacity(0.7))),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _miniStat('Energy', '${(analysis.energyLevel * 100).round()}%'),
                    _miniStat('Warmth', '${(analysis.warmthScore * 100).round()}%'),
                    _miniStat('Source', analysis.analysisSource),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          _buildLightingPreview(rec),
          const SizedBox(height: 20),
          const Text('Ambiance', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text(rec.ambianceNotes, style: TextStyle(color: Colors.grey[700], height: 1.5)),
          const SizedBox(height: 20),
          if (_result!.circadianNote != null) ...[
            Card(
              color: AppTheme.warningColor.withOpacity(0.1),
              child: ListTile(
                leading: const Icon(Icons.schedule, color: AppTheme.warningColor),
                title: Text(_result!.circadianNote!, style: const TextStyle(fontSize: 13)),
              ),
            ),
            const SizedBox(height: 16),
          ],
          if (_result!.alternativeScenes.isNotEmpty) ...[
            const Text('Alternatives', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ..._result!.alternativeScenes.map((alt) => Card(
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: _moodColor(alt['mood'] ?? '').withOpacity(0.2),
                  child: Icon(Icons.lightbulb, color: _moodColor(alt['mood'] ?? '')),
                ),
                title: Text((alt['mood'] as String).toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text(alt['description'] ?? ''),
                trailing: Text('${alt['color_temperature']}K', style: const TextStyle(fontWeight: FontWeight.w600)),
              ),
            )),
          ],
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: _isSavingScene ? null : _saveScene,
                  icon: _isSavingScene
                      ? const SizedBox(height: 18, width: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : Icon(_savedSceneId != null ? Icons.check : Icons.save),
                  label: Text(_savedSceneId != null ? 'Saved' : 'Save This Scene'),
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryColor, foregroundColor: Colors.white),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: _isExporting ? null : _exportToSmartHome,
                  icon: _isExporting
                      ? const SizedBox(height: 18, width: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.download),
                  label: const Text('Export'),
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.accentColor, foregroundColor: Colors.white),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildLightingPreview(LightingRecommendationModel rec) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.grey[900],
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Lighting Preview', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              Container(
                width: 24, height: 24,
                decoration: BoxDecoration(
                  color: Color(int.parse('0xFF${(rec.colorHex ?? '#FFFFFF').substring(1)}')),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white30),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _lightParam('Temp', '${rec.colorTemperature}K'),
              _lightParam('Brightness', '${(rec.brightness * 100).round()}%'),
              _lightParam('Transition', '${rec.transitionDuration.round()}s'),
            ],
          ),
          const SizedBox(height: 12),
          Container(
            width: double.infinity,
            height: 8,
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  const Color(0xFFFF6B35),
                  Color(int.parse('0xFF${(rec.colorHex ?? '#FFF5E6').substring(1)}')),
                  const Color(0xFFF0F8FF),
                ],
              ),
              borderRadius: BorderRadius.circular(4),
            ),
          ),
          const SizedBox(height: 4),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('1800K', style: TextStyle(color: Colors.grey[600], fontSize: 10)),
              Text('${rec.colorTemperature}K', style: const TextStyle(color: Colors.white70, fontSize: 10, fontWeight: FontWeight.bold)),
              Text('6500K', style: TextStyle(color: Colors.grey[600], fontSize: 10)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildCircadianTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Circadian Rhythm Schedule', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text('Lighting that follows your natural body clock', style: TextStyle(color: Colors.grey[600])),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: _buildTimePicker('Wake Time', _wakeTime, (v) {
                  setState(() => _wakeTime = v);
                }),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildTimePicker('Sleep Time', _sleepTime, (v) {
                  setState(() => _sleepTime = v);
                }),
              ),
              const SizedBox(width: 12),
              ElevatedButton(
                onPressed: _isLoadingCircadian ? null : _loadCircadianSchedule,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryColor,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
                ),
                child: _isLoadingCircadian
                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.refresh),
              ),
            ],
          ),
          const SizedBox(height: 20),
          if (_isLoadingCircadian)
            const Center(child: Padding(
              padding: EdgeInsets.all(32),
              child: CircularProgressIndicator(),
            ))
          else if (_circadianSchedule.isEmpty && _circadianLoaded)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(32),
                child: Text('No schedule generated yet', style: TextStyle(color: Colors.grey[500])),
              ),
            )
          else
            ..._circadianSchedule.map((entry) {
              final time = entry['time'] as String? ?? '';
              final label = entry['label'] as String? ?? entry['phase'] as String? ?? '';
              final temp = entry['color_temperature']?.toString() ?? '';
              final brightness = entry['brightness'];
              final brightnessPercent = brightness is num ? (brightness * 100).round() : 0;

              return _circadianEntry(
                time,
                label,
                '${temp}K',
                brightness is num ? brightness.toDouble() : 0.0,
                _circadianIcon(label),
                _circadianColor(label),
              );
            }),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _circadianSchedule.isEmpty ? null : _exportToSmartHome,
              icon: const Icon(Icons.download),
              label: const Text('Export to Smart Home'),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.accentColor, foregroundColor: Colors.white),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTimePicker(String label, String currentValue, ValueChanged<String> onChanged) {
    return GestureDetector(
      onTap: () async {
        final parts = currentValue.split(':');
        final picked = await showTimePicker(
          context: context,
          initialTime: TimeOfDay(hour: int.parse(parts[0]), minute: int.parse(parts[1])),
        );
        if (picked != null) {
          final formatted = '${picked.hour.toString().padLeft(2, '0')}:${picked.minute.toString().padLeft(2, '0')}';
          onChanged(formatted);
        }
      },
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          border: Border.all(color: Colors.grey[300]!),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Text(label, style: TextStyle(fontSize: 11, color: Colors.grey[600])),
            const SizedBox(height: 4),
            Text(currentValue, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  IconData _circadianIcon(String label) {
    final lower = label.toLowerCase();
    if (lower.contains('wake') || lower.contains('alarm')) return Icons.alarm;
    if (lower.contains('sunrise')) return Icons.wb_sunny;
    if (lower.contains('morning') || lower.contains('focus')) return Icons.psychology;
    if (lower.contains('peak') || lower.contains('daylight') || lower.contains('noon')) return Icons.wb_sunny;
    if (lower.contains('creative') || lower.contains('afternoon')) return Icons.palette;
    if (lower.contains('golden') || lower.contains('sunset') || lower.contains('evening')) return Icons.wb_twilight;
    if (lower.contains('cozy') || lower.contains('warm')) return Icons.local_fire_department;
    if (lower.contains('sleep') && lower.contains('prep')) return Icons.bedtime;
    if (lower.contains('sleep') || lower.contains('night')) return Icons.nightlight;
    return Icons.schedule;
  }

  Color _circadianColor(String label) {
    final lower = label.toLowerCase();
    if (lower.contains('wake') || lower.contains('alarm')) return Colors.deepPurple;
    if (lower.contains('sunrise')) return Colors.orange;
    if (lower.contains('morning') || lower.contains('focus')) return Colors.blue;
    if (lower.contains('peak') || lower.contains('daylight') || lower.contains('noon')) return Colors.amber;
    if (lower.contains('creative') || lower.contains('afternoon')) return Colors.purple;
    if (lower.contains('golden') || lower.contains('sunset') || lower.contains('evening')) return Colors.deepOrange;
    if (lower.contains('cozy') || lower.contains('warm')) return Colors.brown;
    if (lower.contains('sleep') && lower.contains('prep')) return Colors.indigo;
    if (lower.contains('sleep') || lower.contains('night')) return Colors.grey;
    return Colors.teal;
  }

  Widget _circadianEntry(String time, String label, String temp, double brightness, IconData icon, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Card(
        child: ListTile(
          leading: CircleAvatar(
            backgroundColor: color.withOpacity(0.15),
            child: Icon(icon, color: color, size: 20),
          ),
          title: Text(label, style: const TextStyle(fontWeight: FontWeight.w600)),
          subtitle: Text('$temp  •  ${(brightness * 100).round()}% brightness'),
          trailing: Text(time, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        ),
      ),
    );
  }

  Widget _miniStat(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15)),
        Text(label, style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 11)),
      ],
    );
  }

  Widget _lightParam(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
        Text(label, style: TextStyle(color: Colors.grey[500], fontSize: 11)),
      ],
    );
  }

  Color _moodColor(String mood) {
    const colors = {
      'relaxed': Color(0xFF81C784), 'focused': Color(0xFF64B5F6),
      'energetic': Color(0xFFFFB74D), 'romantic': Color(0xFFE57373),
      'cozy': Color(0xFFFFCC80), 'creative': Color(0xFFCE93D8),
      'social': Color(0xFF4DD0E1), 'sleepy': Color(0xFF9575CD),
      'refreshed': Color(0xFF80DEEA), 'melancholic': Color(0xFF90A4AE),
    };
    return colors[mood] ?? Colors.grey;
  }
}

extension on String {
  String? get nullIfEmpty => isEmpty ? null : this;
}
