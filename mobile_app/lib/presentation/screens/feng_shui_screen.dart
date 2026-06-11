import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/feng_shui_model.dart';

class FengShuiScreen extends StatefulWidget {
  const FengShuiScreen({super.key});

  @override
  State<FengShuiScreen> createState() => _FengShuiScreenState();
}

class _FengShuiScreenState extends State<FengShuiScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  String _selectedRoom = 'living_room';
  String? _selectedDirection;
  String? _birthYear;
  bool _isAnalyzing = false;
  FengShuiAnalysisModel? _analysis;

  final _directions = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest'];
  final _roomTypes = {'living_room': 'Living Room', 'bedroom': 'Bedroom', 'office': 'Office', 'kitchen': 'Kitchen', 'bathroom': 'Bathroom', 'dining_room': 'Dining Room'};
  final _elementIcons = {'wood': Icons.park, 'fire': Icons.local_fire_department, 'earth': Icons.landscape, 'metal': Icons.settings, 'water': Icons.water_drop};
  final _elementColors = {'wood': Color(0xFF4CAF50), 'fire': Color(0xFFFF5722), 'earth': Color(0xFFFF9800), 'metal': Color(0xFF9E9E9E), 'water': Color(0xFF2196F3)};

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _runAnalysis() async {
    setState(() => _isAnalyzing = true);
    try {
      final response = await ApiClient().dio.post('/feng-shui/analyze', data: {
        'room_type': _selectedRoom,
        'compass_direction': _selectedDirection,
        'birth_year': _birthYear != null ? int.tryParse(_birthYear!) : null,
        'include_bagua': true,
        'include_element_analysis': true,
      });
      setState(() {
        _analysis = FengShuiAnalysisModel.fromJson(response.data);
        _isAnalyzing = false;
        _tabController.animateTo(1);
      });
    } catch (e) {
      setState(() => _isAnalyzing = false);
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Analysis failed')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Feng Shui Analysis'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: const [
            Tab(icon: Icon(Icons.compass_calibration), text: 'Setup'),
            Tab(icon: Icon(Icons.analytics), text: 'Score'),
            Tab(icon: Icon(Icons.grid_view), text: 'Bagua'),
            Tab(icon: Icon(Icons.healing), text: 'Cures'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [_buildSetupTab(), _buildScoreTab(), _buildBaguaTab(), _buildCuresTab()],
      ),
    );
  }

  Widget _buildSetupTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Room Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Wrap(spacing: 8, runSpacing: 8, children: _roomTypes.entries.map((e) =>
            ChoiceChip(label: Text(e.value), selected: _selectedRoom == e.key,
              onSelected: (_) => setState(() => _selectedRoom = e.key),
              selectedColor: AppTheme.primaryColor.withOpacity(0.2)),
          ).toList()),
          const SizedBox(height: 24),
          const Text('Compass Direction (optional)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text('Which direction does the room entrance face?', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
          const SizedBox(height: 12),
          _buildCompassWheel(),
          const SizedBox(height: 24),
          const Text('Birth Year (optional)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text('For personal Kua number and lucky directions', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
          const SizedBox(height: 12),
          TextField(
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: 'Birth Year', hintText: 'e.g. 1995', prefixIcon: Icon(Icons.calendar_today)),
            onChanged: (v) => _birthYear = v,
          ),
          const SizedBox(height: 32),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isAnalyzing ? null : _runAnalysis,
              icon: _isAnalyzing
                  ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.auto_awesome),
              label: Text(_isAnalyzing ? 'Analyzing...' : 'Analyze Feng Shui'),
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF8B4513), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(vertical: 16)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCompassWheel() {
    return Center(
      child: SizedBox(
        width: 260, height: 260,
        child: Stack(
          alignment: Alignment.center,
          children: [
            Container(
              width: 260, height: 260,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: Colors.grey[300]!, width: 2),
                color: Colors.grey[50],
              ),
            ),
            ..._directions.asMap().entries.map((entry) {
              final i = entry.key;
              final dir = entry.value;
              final radius = 100.0;
              final x = radius * _cos(i * 45 - 90);
              final y = radius * _sin(i * 45 - 90);
              final isSelected = _selectedDirection == dir;

              return Positioned(
                left: 130 + x - 28, top: 130 + y - 28,
                child: GestureDetector(
                  onTap: () => setState(() => _selectedDirection = _selectedDirection == dir ? null : dir),
                  child: Container(
                    width: 56, height: 56,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: isSelected ? const Color(0xFF8B4513) : Colors.white,
                      border: Border.all(color: isSelected ? const Color(0xFF8B4513) : Colors.grey[400]!),
                      boxShadow: isSelected ? [BoxShadow(color: const Color(0xFF8B4513).withOpacity(0.3), blurRadius: 8)] : null,
                    ),
                    child: Center(
                      child: Text(dir.substring(0, 1).toUpperCase() + (dir.length > 5 ? dir.substring(1, 2).toUpperCase() : ''),
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: isSelected ? Colors.white : Colors.grey[700])),
                    ),
                  ),
                ),
              );
            }),
            Icon(Icons.explore, size: 32, color: Colors.grey[400]),
          ],
        ),
      ),
    );
  }

  Widget _buildScoreTab() {
    if (_analysis == null) return _emptyState('Run analysis first');

    final a = _analysis!;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          _buildOverallScoreCard(a),
          const SizedBox(height: 16),
          _buildScoreRow('Chi Flow', a.chiFlowScore, Icons.air),
          _buildScoreRow('Element Balance', a.elementBalanceScore, Icons.balance),
          _buildScoreRow('Yin-Yang', a.yinYangScore, Icons.contrast),
          _buildScoreRow('Clutter', a.clutterScore, Icons.cleaning_services),
          _buildScoreRow('Commanding Position', a.commandingPositionScore, Icons.visibility),
          const SizedBox(height: 16),
          if (a.elementAnalysis != null) _buildElementChart(a.elementAnalysis!),
          const SizedBox(height: 16),
          if (a.chiFlowIssues != null && a.chiFlowIssues!.isNotEmpty) ...[
            const Text('Chi Flow Issues', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...a.chiFlowIssues!.map((i) => Card(
              color: _severityColor(i.severity).withOpacity(0.05),
              child: ListTile(
                leading: Icon(Icons.warning_amber, color: _severityColor(i.severity)),
                title: Text(i.description, style: const TextStyle(fontSize: 13)),
                subtitle: Text(i.impact, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              ),
            )),
          ],
          if (a.birthElement != null) ...[
            const SizedBox(height: 16),
            Card(
              child: ListTile(
                leading: Icon(_elementIcons[a.birthElement] ?? Icons.circle, color: _elementColors[a.birthElement] ?? Colors.grey),
                title: Text('Your Element: ${a.birthElement!.toUpperCase()}'),
                subtitle: Text(a.luckyDirections != null ? 'Lucky: ${(a.luckyDirections!["lucky"] as List?)?.take(3).join(", ") ?? ""}' : ''),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildOverallScoreCard(FengShuiAnalysisModel a) {
    final color = a.overallScore >= 7 ? AppTheme.successColor : a.overallScore >= 5 ? AppTheme.warningColor : AppTheme.errorColor;
    return Container(
      width: double.infinity, padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [const Color(0xFF8B4513), const Color(0xFFD2691E)]),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(children: [
        const Text('Feng Shui Score', style: TextStyle(color: Colors.white70)),
        const SizedBox(height: 8),
        Text(a.overallScore.toStringAsFixed(1), style: const TextStyle(color: Colors.white, fontSize: 48, fontWeight: FontWeight.bold)),
        Text('/ 10', style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 18)),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
          decoration: BoxDecoration(color: color.withOpacity(0.3), borderRadius: BorderRadius.circular(20)),
          child: Text(a.scoreInterpretation, style: const TextStyle(color: Colors.white, fontSize: 12), textAlign: TextAlign.center),
        ),
      ]),
    );
  }

  Widget _buildScoreRow(String label, double score, IconData icon) {
    final color = score >= 7 ? AppTheme.successColor : score >= 5 ? AppTheme.warningColor : AppTheme.errorColor;
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Card(
        child: ListTile(
          leading: Icon(icon, color: color),
          title: Text(label),
          trailing: Row(mainAxisSize: MainAxisSize.min, children: [
            Text(score.toStringAsFixed(1), style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: color)),
            Text('/10', style: TextStyle(color: Colors.grey[400], fontSize: 12)),
          ]),
        ),
      ),
    );
  }

  Widget _buildElementChart(List<ElementBalanceModel> elements) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Five Elements', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...elements.map((e) {
          final color = _elementColors[e.element] ?? Colors.grey;
          final icon = _elementIcons[e.element] ?? Icons.circle;
          return Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Row(children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              SizedBox(width: 50, child: Text(e.element[0].toUpperCase() + e.element.substring(1), style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600))),
              Expanded(
                child: Stack(children: [
                  Container(height: 16, decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(8))),
                  FractionallySizedBox(widthFactor: e.currentLevel.clamp(0, 1),
                    child: Container(height: 16, decoration: BoxDecoration(color: color.withOpacity(0.7), borderRadius: BorderRadius.circular(8)))),
                  Positioned(left: (e.idealLevel * 100).clamp(0, 95).toDouble(), child: Container(width: 2, height: 16, color: Colors.black54)),
                ]),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: e.status == 'balanced' ? AppTheme.successColor.withOpacity(0.1) : AppTheme.warningColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(e.status, style: TextStyle(fontSize: 10, fontWeight: FontWeight.w600,
                  color: e.status == 'balanced' ? AppTheme.successColor : AppTheme.warningColor)),
              ),
            ]),
          );
        }),
      ],
    );
  }

  Widget _buildBaguaTab() {
    if (_analysis == null || _analysis!.baguaMap == null) return _emptyState('Run analysis to see Bagua map');

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Bagua Map', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Text('Each zone represents a life area affected by your room\'s energy', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
          const SizedBox(height: 16),
          ..._analysis!.baguaMap!.map((zone) => _buildBaguaCard(zone)),
          if (_analysis!.colorRecommendations != null) ...[
            const SizedBox(height: 20),
            const Text('Color Recommendations', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Card(child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                _colorRow('Primary', _analysis!.colorRecommendations!['primary']),
                const SizedBox(height: 8),
                _colorRow('Accent', _analysis!.colorRecommendations!['accent']),
                const SizedBox(height: 8),
                _colorRow('Avoid', _analysis!.colorRecommendations!['avoid']),
                const SizedBox(height: 8),
                Text(_analysis!.colorRecommendations!['reason'] ?? '', style: TextStyle(color: Colors.grey[600], fontSize: 12, fontStyle: FontStyle.italic)),
              ]),
            )),
          ],
        ],
      ),
    );
  }

  Widget _buildBaguaCard(BaguaZoneModel zone) {
    final color = _elementColors[zone.element] ?? Colors.grey;
    final statusColor = zone.score >= 7 ? AppTheme.successColor : zone.score >= 5 ? AppTheme.warningColor : AppTheme.errorColor;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ExpansionTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.15), child: Icon(_elementIcons[zone.element] ?? Icons.circle, color: color, size: 18)),
        title: Text(zone.zone, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        subtitle: Row(children: [
          Text('${zone.direction.toUpperCase()} \u2022 ${zone.element}', style: TextStyle(fontSize: 12, color: Colors.grey[600])),
          const Spacer(),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(color: statusColor.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
            child: Text(zone.score.toStringAsFixed(1), style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: statusColor)),
          ),
        ]),
        children: [
          Padding(padding: const EdgeInsets.fromLTRB(16, 0, 16, 16), child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(zone.lifeArea, style: TextStyle(color: Colors.grey[700], fontSize: 13)),
              const SizedBox(height: 8),
              Wrap(spacing: 4, children: zone.colors.map((c) => Chip(label: Text(c, style: const TextStyle(fontSize: 10)), materialTapTargetSize: MaterialTapTargetSize.shrinkWrap)).toList()),
              if (zone.enhancement != null) ...[
                const SizedBox(height: 8),
                Row(children: [
                  const Icon(Icons.lightbulb, size: 16, color: AppTheme.warningColor),
                  const SizedBox(width: 4),
                  Expanded(child: Text(zone.enhancement!, style: const TextStyle(fontSize: 12, color: AppTheme.warningColor))),
                ]),
              ],
            ],
          )),
        ],
      ),
    );
  }

  Widget _buildCuresTab() {
    if (_analysis == null) return _emptyState('Run analysis to see cures');

    final cures = _analysis!.cures;
    if (cures.isEmpty) {
      return Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        const Icon(Icons.check_circle, size: 64, color: AppTheme.successColor),
        const SizedBox(height: 16),
        const Text('No cures needed!', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        Text('Your room has excellent Feng Shui', style: TextStyle(color: Colors.grey[600])),
      ]));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: cures.length + 1,
      itemBuilder: (context, i) {
        if (i == 0) return Padding(padding: const EdgeInsets.only(bottom: 16), child: Text('${cures.length} Recommended Cures', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)));
        final cure = cures[i - 1];
        final sevColor = _severityColor(cure.severity);

        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          child: Padding(padding: const EdgeInsets.all(14), child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2), decoration: BoxDecoration(color: sevColor.withOpacity(0.1), borderRadius: BorderRadius.circular(6)),
                  child: Text(cure.severity.toUpperCase(), style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: sevColor))),
                const SizedBox(width: 8),
                Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2), decoration: BoxDecoration(color: Colors.grey[100], borderRadius: BorderRadius.circular(6)),
                  child: Text(cure.category.replaceAll('_', ' '), style: TextStyle(fontSize: 10, color: Colors.grey[700]))),
                const Spacer(),
                if (cure.element != null) Icon(_elementIcons[cure.element] ?? Icons.circle, size: 16, color: _elementColors[cure.element] ?? Colors.grey),
                if (cure.estimatedCost != null) ...[const SizedBox(width: 8), Text('\$${cure.estimatedCost!.toStringAsFixed(0)}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13))],
              ]),
              const SizedBox(height: 10),
              Text(cure.issueDescription, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              const SizedBox(height: 6),
              Text(cure.cureDescription, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
              if (cure.placement != null) ...[
                const SizedBox(height: 4),
                Row(children: [Icon(Icons.place, size: 14, color: Colors.grey[500]), const SizedBox(width: 4),
                  Text(cure.placement!, style: TextStyle(fontSize: 12, color: Colors.grey[500]))]),
              ],
            ],
          )),
        );
      },
    );
  }

  Widget _emptyState(String message) => Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
    Icon(Icons.compass_calibration, size: 64, color: Colors.grey[300]), const SizedBox(height: 16),
    Text(message, style: TextStyle(color: Colors.grey[500], fontSize: 16)),
  ]));

  Widget _colorRow(String label, dynamic colors) {
    final list = colors is List ? colors.map((e) => e.toString()).toList() : <String>[];
    return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
      SizedBox(width: 60, child: Text(label, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13))),
      Expanded(child: Wrap(spacing: 4, children: list.map((c) => Chip(label: Text(c, style: const TextStyle(fontSize: 10)), materialTapTargetSize: MaterialTapTargetSize.shrinkWrap)).toList())),
    ]);
  }

  Color _severityColor(String severity) => severity == 'high' ? AppTheme.errorColor : severity == 'medium' ? AppTheme.warningColor : AppTheme.accentColor;
  double _cos(int degrees) => _cosTable[degrees % 360] ?? 0;
  double _sin(int degrees) => _sinTable[degrees % 360] ?? 0;

  static final _cosTable = {0: 1.0, 45: 0.707, 90: 0.0, 135: -0.707, 180: -1.0, 225: -0.707, 270: 0.0, 315: 0.707};
  static final _sinTable = {0: 0.0, 45: 0.707, 90: 1.0, 135: 0.707, 180: 0.0, 225: -0.707, 270: -1.0, 315: -0.707};
}
