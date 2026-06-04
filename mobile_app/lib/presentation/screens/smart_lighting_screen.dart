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
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.save),
              label: const Text('Save This Scene'),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryColor, foregroundColor: Colors.white),
            ),
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
          const SizedBox(height: 20),
          ...[
            _circadianEntry('06:30', 'Gentle Wake', '2200K', 0.15, Icons.alarm, Colors.deepPurple),
            _circadianEntry('07:00', 'Sunrise Simulation', '3000K', 0.45, Icons.wb_sunny, Colors.orange),
            _circadianEntry('09:00', 'Morning Focus', '5000K', 0.85, Icons.psychology, Colors.blue),
            _circadianEntry('12:00', 'Peak Daylight', '5500K', 0.95, Icons.wb_sunny, Colors.amber),
            _circadianEntry('16:00', 'Creative Hour', '4500K', 0.75, Icons.palette, Colors.purple),
            _circadianEntry('18:00', 'Golden Hour', '3500K', 0.60, Icons.wb_twilight, Colors.deepOrange),
            _circadianEntry('21:00', 'Cozy Evening', '2500K', 0.30, Icons.local_fire_department, Colors.brown),
            _circadianEntry('22:00', 'Sleep Prep', '2000K', 0.15, Icons.bedtime, Colors.indigo),
            _circadianEntry('23:00', 'Sleep Mode', '1800K', 0.03, Icons.nightlight, Colors.grey),
          ],
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.download),
              label: const Text('Export to Smart Home'),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.accentColor, foregroundColor: Colors.white),
            ),
          ),
        ],
      ),
    );
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
