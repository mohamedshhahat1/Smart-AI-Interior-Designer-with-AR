import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/room_model.dart';
import 'package:smart_interior_ai/data/models/seasonal_model.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';
import 'package:smart_interior_ai/presentation/widgets/scanned_room_picker.dart';

class SeasonalThemeScreen extends StatefulWidget {
  const SeasonalThemeScreen({super.key});

  @override
  State<SeasonalThemeScreen> createState() => _SeasonalThemeScreenState();
}

class _SeasonalThemeScreenState extends State<SeasonalThemeScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _apiService = ApiService();
  List<RoomModel> _rooms = [];
  RoomModel? _selectedRoom;
  bool _isLoadingRooms = true;
  String _selectedType = 'season';
  String? _selectedSeason;
  String? _selectedHoliday;
  String _budgetTier = 'medium';
  double _intensity = 0.7;
  bool _includeDiy = true;
  bool _includeScents = true;
  bool _isGenerating = false;
  SeasonalThemeModel? _generatedTheme;

  final _seasons = {
    'spring': {'icon': Icons.local_florist, 'color': Color(0xFF81C784)},
    'summer': {'icon': Icons.wb_sunny, 'color': Color(0xFFFFB74D)},
    'autumn': {'icon': Icons.eco, 'color': Color(0xFFFF8A65)},
    'winter': {'icon': Icons.ac_unit, 'color': Color(0xFF90CAF9)},
  };

  final _holidays = [
    {'key': 'christmas', 'label': 'Christmas', 'icon': Icons.park, 'color': Color(0xFFC62828)},
    {'key': 'halloween', 'label': 'Halloween', 'icon': Icons.nights_stay, 'color': Color(0xFFFF6F00)},
    {'key': 'eid', 'label': 'Eid', 'icon': Icons.mosque, 'color': Color(0xFF2E7D32)},
    {'key': 'diwali', 'label': 'Diwali', 'icon': Icons.auto_awesome, 'color': Color(0xFFFF8F00)},
    {'key': 'valentines', 'label': "Valentine's", 'icon': Icons.favorite, 'color': Color(0xFFE91E63)},
    {'key': 'thanksgiving', 'label': 'Thanksgiving', 'icon': Icons.dinner_dining, 'color': Color(0xFF795548)},
    {'key': 'easter', 'label': 'Easter', 'icon': Icons.egg, 'color': Color(0xFF7E57C2)},
    {'key': 'lunar_new_year', 'label': 'Lunar New Year', 'icon': Icons.celebration, 'color': Color(0xFFD32F2F)},
    {'key': 'hanukkah', 'label': 'Hanukkah', 'icon': Icons.light, 'color': Color(0xFF1976D2)},
    {'key': 'new_year', 'label': 'New Year', 'icon': Icons.celebration, 'color': Color(0xFFFFD700)},
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadRooms();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _generate() async {
    if (_selectedRoom == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Select a scanned room first')),
      );
      return;
    }
    setState(() => _isGenerating = true);
    try {
      final response = await ApiClient().dio.post('/seasonal/generate', data: {
        'theme_type': _selectedType,
        'season': _selectedType == 'season' ? _selectedSeason : null,
        'holiday': _selectedType == 'holiday' ? _selectedHoliday : null,
        'room_id': _selectedRoom!.id,
        'room_type': _selectedRoom!.roomType ?? 'living_room',
        'budget_tier': _budgetTier,
        'intensity': _intensity,
        'include_diy': _includeDiy,
        'include_scents': _includeScents,
      });
      setState(() {
        _generatedTheme = SeasonalThemeModel.fromJson(response.data);
        _isGenerating = false;
        _tabController.animateTo(1);
      });
    } catch (e) {
      setState(() => _isGenerating = false);
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Failed to generate theme')));
    }
  }

  Future<void> _loadRooms() async {
    try {
      final rooms = await _apiService.listRooms();
      if (!mounted) return;
      setState(() {
        _rooms = rooms;
        _isLoadingRooms = false;
      });
    } catch (_) {
      if (mounted) setState(() => _isLoadingRooms = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Seasonal Themes'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.palette), text: 'Create'),
            Tab(icon: Icon(Icons.auto_awesome), text: 'Theme'),
            Tab(icon: Icon(Icons.handyman), text: 'DIY'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [_buildCreateTab(), _buildThemeTab(), _buildDiyTab()],
      ),
    );
  }

  Widget _buildCreateTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Theme Type', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Row(children: [
            Expanded(child: _typeButton('Season', Icons.wb_sunny, 'season')),
            const SizedBox(width: 12),
            Expanded(child: _typeButton('Holiday', Icons.celebration, 'holiday')),
          ]),
          const SizedBox(height: 24),

          if (_selectedType == 'season') ...[
            const Text('Select Season', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Row(children: _seasons.entries.map((e) {
              final isSelected = _selectedSeason == e.key;
              return Expanded(child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 4),
                child: GestureDetector(
                  onTap: () => setState(() => _selectedSeason = e.key),
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 20),
                    decoration: BoxDecoration(
                      color: isSelected ? (e.value['color'] as Color).withOpacity(0.2) : Colors.grey[100],
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: isSelected ? e.value['color'] as Color : Colors.grey[300]!, width: isSelected ? 2 : 1),
                    ),
                    child: Column(children: [
                      Icon(e.value['icon'] as IconData, color: e.value['color'] as Color, size: 32),
                      const SizedBox(height: 8),
                      Text(e.key[0].toUpperCase() + e.key.substring(1), style: TextStyle(fontWeight: FontWeight.w600, fontSize: 12, color: isSelected ? e.value['color'] as Color : Colors.grey[700])),
                    ]),
                  ),
                ),
              ));
            }).toList()),
          ],

          if (_selectedType == 'holiday') ...[
            const Text('Select Holiday', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            GridView.builder(
              shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, mainAxisSpacing: 10, crossAxisSpacing: 10, childAspectRatio: 1.0),
              itemCount: _holidays.length,
              itemBuilder: (ctx, i) {
                final h = _holidays[i];
                final isSelected = _selectedHoliday == h['key'];
                return GestureDetector(
                  onTap: () => setState(() => _selectedHoliday = h['key'] as String),
                  child: Container(
                    decoration: BoxDecoration(
                      color: isSelected ? (h['color'] as Color).withOpacity(0.15) : Colors.grey[100],
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: isSelected ? h['color'] as Color : Colors.grey[300]!, width: isSelected ? 2 : 1),
                    ),
                    child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                      Icon(h['icon'] as IconData, color: h['color'] as Color, size: 28),
                      const SizedBox(height: 6),
                      Text(h['label'] as String, textAlign: TextAlign.center, style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: isSelected ? h['color'] as Color : Colors.grey[700])),
                    ]),
                  ),
                );
              },
            ),
          ],
          const SizedBox(height: 24),

          const Text('Budget', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Row(children: ['budget', 'medium', 'premium'].map((t) {
            final labels = {'budget': 'Budget', 'medium': 'Medium', 'premium': 'Premium'};
            final icons = {'budget': Icons.savings, 'medium': Icons.account_balance_wallet, 'premium': Icons.diamond};
            return Expanded(child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4),
              child: ChoiceChip(label: Text(labels[t]!), avatar: Icon(icons[t], size: 16), selected: _budgetTier == t,
                onSelected: (_) => setState(() => _budgetTier = t), selectedColor: AppTheme.primaryColor.withOpacity(0.2)),
            ));
          }).toList()),
          const SizedBox(height: 20),

          Row(children: [
            const Text('Intensity', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const Spacer(),
            Text(_intensity < 0.3 ? 'Subtle' : _intensity < 0.7 ? 'Moderate' : 'Full Transform', style: const TextStyle(fontWeight: FontWeight.w600)),
          ]),
          Slider(value: _intensity, onChanged: (v) => setState(() => _intensity = v), activeColor: AppTheme.primaryColor, divisions: 10),
          const SizedBox(height: 12),

          SwitchListTile(title: const Text('Include DIY Projects'), value: _includeDiy, onChanged: (v) => setState(() => _includeDiy = v)),
          SwitchListTile(title: const Text('Include Scent Recommendations'), value: _includeScents, onChanged: (v) => setState(() => _includeScents = v)),
          const SizedBox(height: 24),

          SizedBox(width: double.infinity, child: ElevatedButton.icon(
            onPressed: (_isGenerating || (_selectedType == 'season' && _selectedSeason == null) || (_selectedType == 'holiday' && _selectedHoliday == null)) ? null : _generate,
            icon: _isGenerating ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white)) : const Icon(Icons.auto_awesome),
            label: Text(_isGenerating ? 'Generating...' : 'Generate Theme'),
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryColor, foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(vertical: 16)),
          )),
        ],
      ),
    );
  }

  Widget _typeButton(String label, IconData icon, String type) {
    final isSelected = _selectedType == type;
    return GestureDetector(
      onTap: () => setState(() => _selectedType = type),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 20),
        decoration: BoxDecoration(
          color: isSelected ? AppTheme.primaryColor.withOpacity(0.1) : Colors.grey[100],
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: isSelected ? AppTheme.primaryColor : Colors.grey[300]!, width: isSelected ? 2 : 1),
        ),
        child: Column(children: [
          Icon(icon, color: isSelected ? AppTheme.primaryColor : Colors.grey, size: 32),
          const SizedBox(height: 8),
          Text(label, style: TextStyle(fontWeight: FontWeight.bold, color: isSelected ? AppTheme.primaryColor : Colors.grey[700])),
        ]),
      ),
    );
  }

  Widget _buildThemeTab() {
    if (_generatedTheme == null) return _emptyState('Generate a theme first', Icons.palette);

    final t = _generatedTheme!;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity, padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              gradient: LinearGradient(colors: _themeGradient(t.season, t.holiday)),
              borderRadius: BorderRadius.circular(20),
            ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Room Context', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ScannedRoomPicker(
          rooms: _rooms,
          selectedRoomId: _selectedRoom?.id,
          isLoading: _isLoadingRooms,
          onChanged: (room) => setState(() => _selectedRoom = room),
        ),
        const SizedBox(height: 24),
              Text(t.name, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
              if (t.description != null) ...[const SizedBox(height: 8), Text(t.description!, style: TextStyle(color: Colors.white.withOpacity(0.9), fontSize: 13))],
              const SizedBox(height: 16),
              Row(children: [
                _tag(t.themeType.toUpperCase()),
                const SizedBox(width: 8),
                _tag(t.budgetTier.toUpperCase()),
                const Spacer(),
                if (t.estimatedCost != null) Text('\$${t.estimatedCost!.toStringAsFixed(0)}', style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
              ]),
            ]),
          ),
          const SizedBox(height: 20),

          if (t.colorPalette != null) _buildColorSection(t.colorPalette!),
          const SizedBox(height: 16),

          if (t.textures != null && t.textures!.isNotEmpty) ...[
            const Text('Textures & Materials', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Wrap(spacing: 6, runSpacing: 6, children: [...(t.textures ?? []), ...(t.materials ?? [])].map((m) => Chip(label: Text(m, style: const TextStyle(fontSize: 11)))).toList()),
            const SizedBox(height: 16),
          ],

          if (t.decorItems != null && t.decorItems!.isNotEmpty) ...[
            Text('Decor Items (${t.decorItems!.length})', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...t.decorItems!.map((d) => Card(child: ListTile(
              leading: CircleAvatar(backgroundColor: d.reusable ? AppTheme.successColor.withOpacity(0.1) : AppTheme.warningColor.withOpacity(0.1),
                child: Icon(d.reusable ? Icons.recycling : Icons.shopping_cart, color: d.reusable ? AppTheme.successColor : AppTheme.warningColor, size: 18)),
              title: Text(d.name, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              subtitle: Text('${d.category} • ${d.placement}', style: const TextStyle(fontSize: 12)),
              trailing: d.estimatedCost != null ? Text('\$${d.estimatedCost!.toStringAsFixed(0)}', style: const TextStyle(fontWeight: FontWeight.bold)) : null,
            ))),
            const SizedBox(height: 16),
          ],

          if (t.scentRecommendations != null && t.scentRecommendations!.isNotEmpty) ...[
            const Text('Scents', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...t.scentRecommendations!.map((s) => Card(child: ListTile(
              leading: const Icon(Icons.air, color: AppTheme.accentColor),
              title: Text(s.scent, style: const TextStyle(fontSize: 14)),
              subtitle: Text('${s.method} • ${s.placement}'),
              trailing: Chip(label: Text(s.intensity, style: const TextStyle(fontSize: 10))),
            ))),
          ],

          if (t.reusabilityScore != null) ...[
            const SizedBox(height: 16),
            Card(color: AppTheme.successColor.withOpacity(0.05), child: ListTile(
              leading: const Icon(Icons.recycling, color: AppTheme.successColor),
              title: Text('${(t.reusabilityScore! * 100).round()}% Reusable'),
              subtitle: const Text('Items you can use again next year'),
            )),
          ],
        ],
      ),
    );
  }

  Widget _buildDiyTab() {
    if (_generatedTheme == null || _generatedTheme!.diyProjects == null || _generatedTheme!.diyProjects!.isEmpty) {
      return _emptyState('No DIY projects yet', Icons.handyman);
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _generatedTheme!.diyProjects!.length + 1,
      itemBuilder: (ctx, i) {
        if (i == 0) return Padding(padding: const EdgeInsets.only(bottom: 16), child: const Text('DIY Projects', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)));
        final p = _generatedTheme!.diyProjects![i - 1];
        final diffColor = p.difficulty == 'easy' ? AppTheme.successColor : p.difficulty == 'medium' ? AppTheme.warningColor : AppTheme.errorColor;

        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: Padding(padding: const EdgeInsets.all(16), child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                Expanded(child: Text(p.name, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
                Container(padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2), decoration: BoxDecoration(color: diffColor.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                  child: Text(p.difficulty.toUpperCase(), style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: diffColor))),
              ]),
              const SizedBox(height: 8),
              Row(children: [
                Icon(Icons.timer, size: 14, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text('${p.timeMinutes} min', style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                const SizedBox(width: 16),
                Icon(Icons.attach_money, size: 14, color: Colors.grey[600]),
                Text('\$${p.estimatedCost.toStringAsFixed(0)}', style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              ]),
              const SizedBox(height: 12),
              const Text('Materials:', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
              const SizedBox(height: 4),
              Wrap(spacing: 6, children: p.materials.map((m) => Chip(label: Text(m, style: const TextStyle(fontSize: 10)), materialTapTargetSize: MaterialTapTargetSize.shrinkWrap)).toList()),
              const SizedBox(height: 12),
              const Text('Instructions:', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
              const SizedBox(height: 4),
              Text(p.instructions, style: TextStyle(color: Colors.grey[700], fontSize: 13, height: 1.4)),
            ],
          )),
        );
      },
    );
  }

  Widget _buildColorSection(Map<String, dynamic> palette) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Color Palette', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        ...['primary', 'accent', 'neutrals'].where((k) => palette[k] != null).map((key) {
          final colors = List<String>.from(palette[key] ?? []);
          return Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Row(children: [
              SizedBox(width: 60, child: Text(key[0].toUpperCase() + key.substring(1), style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600))),
              ...colors.map((hex) => Container(
                width: 32, height: 32, margin: const EdgeInsets.only(right: 6),
                decoration: BoxDecoration(
                  color: _hexToColor(hex),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.grey[300]!),
                ),
              )),
            ]),
          );
        }),
      ],
    );
  }

  Widget _tag(String text) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
    decoration: BoxDecoration(color: Colors.white.withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
    child: Text(text, style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
  );

  Widget _emptyState(String msg, IconData icon) => Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
    Icon(icon, size: 64, color: Colors.grey[300]), const SizedBox(height: 16),
    Text(msg, style: TextStyle(color: Colors.grey[500], fontSize: 16)),
  ]));

  List<Color> _themeGradient(String? season, String? holiday) {
    if (holiday != null) {
      final map = {'christmas': [Color(0xFFC62828), Color(0xFF2E7D32)], 'halloween': [Color(0xFFFF6F00), Color(0xFF1A1A2E)],
        'eid': [Color(0xFF2E7D32), Color(0xFFDAA520)], 'diwali': [Color(0xFFFF8F00), Color(0xFFD32F2F)],
        'valentines': [Color(0xFFE91E63), Color(0xFFAD1457)], 'thanksgiving': [Color(0xFF795548), Color(0xFFD2691E)]};
      return map[holiday] ?? [AppTheme.primaryColor, AppTheme.secondaryColor];
    }
    final map = {'spring': [Color(0xFF81C784), Color(0xFF66BB6A)], 'summer': [Color(0xFFFFB74D), Color(0xFFFF7043)],
      'autumn': [Color(0xFFFF8A65), Color(0xFF8D6E63)], 'winter': [Color(0xFF90CAF9), Color(0xFF5C6BC0)]};
    return map[season] ?? [AppTheme.primaryColor, AppTheme.secondaryColor];
  }

  Color _hexToColor(String hex) {
    hex = hex.replaceFirst('#', '');
    if (hex.length == 6) hex = 'FF$hex';
    return Color(int.parse(hex, radix: 16));
  }
}
