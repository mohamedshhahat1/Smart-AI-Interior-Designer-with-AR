import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/models/pet_friendly_model.dart';
import 'package:smart_interior_ai/data/models/room_model.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';
import 'package:smart_interior_ai/presentation/widgets/scanned_room_picker.dart';

class PetFriendlyScreen extends StatefulWidget {
  const PetFriendlyScreen({super.key});

  @override
  State<PetFriendlyScreen> createState() => _PetFriendlyScreenState();
}

class _PetFriendlyScreenState extends State<PetFriendlyScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _apiService = ApiService();
  List<RoomModel> _rooms = [];
  RoomModel? _selectedRoom;
  bool _isLoadingRooms = true;

  String _petName = '';
  String _species = 'dog';
  String _size = 'medium';
  String _energy = 'medium';
  bool _isDestructive = false;
  bool _shedsFur = true;
  bool _climbs = false;
  bool _isAnalyzing = false;
  PetFriendlyAnalysisModel? _analysis;
  String? _createdProfileId;

  final _speciesOptions = {
    'dog': {'icon': Icons.pets, 'color': Color(0xFF8D6E63)},
    'cat': {'icon': Icons.pets, 'color': Color(0xFFFF7043)},
    'bird': {'icon': Icons.flutter_dash, 'color': Color(0xFF42A5F5)},
    'rabbit': {'icon': Icons.cruelty_free, 'color': Color(0xFFAB47BC)},
  };

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _loadRooms();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _analyzeRoom() async {
    if (_petName.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Enter your pet\'s name')));
      return;
    }
    if (_selectedRoom == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Select a scanned room first')),
      );
      return;
    }
    setState(() => _isAnalyzing = true);
    try {
      final profileRes = await ApiClient().dio.post('/pet-friendly/profiles', data: {
        'name': _petName, 'species': _species, 'size': _size,
        'energy_level': _energy, 'is_destructive': _isDestructive,
        'sheds_fur': _shedsFur, 'climbs_furniture': _climbs,
      });
      _createdProfileId = profileRes.data['id'];

      final analysisRes = await ApiClient().dio.post('/pet-friendly/analyze', data: {
        'pet_profile_ids': [_createdProfileId],
        'room_id': _selectedRoom!.id,
        'room_type': _selectedRoom!.roomType ?? 'living_room',
        'detected_objects': _selectedRoom!.detectedObjects,
        'include_products': true,
      });
      setState(() {
        _analysis = PetFriendlyAnalysisModel.fromJson(analysisRes.data);
        _isAnalyzing = false;
        _tabController.animateTo(1);
      });
    } catch (e) {
      setState(() => _isAnalyzing = false);
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Analysis failed')));
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
        title: const Text('Pet-Friendly Design'),
        bottom: TabBar(controller: _tabController, isScrollable: true, tabs: const [
          Tab(icon: Icon(Icons.pets), text: 'Pet Profile'),
          Tab(icon: Icon(Icons.shield), text: 'Safety'),
          Tab(icon: Icon(Icons.map), text: 'Zones'),
          Tab(icon: Icon(Icons.shopping_bag), text: 'Products'),
        ]),
      ),
      body: TabBarView(controller: _tabController, children: [
        _buildProfileTab(), _buildSafetyTab(), _buildZonesTab(), _buildProductsTab(),
      ]),
    );
  }

  Widget _buildProfileTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('Room Context', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ScannedRoomPicker(
          rooms: _rooms,
          selectedRoomId: _selectedRoom?.id,
          isLoading: _isLoadingRooms,
          onChanged: (room) => setState(() => _selectedRoom = room),
        ),
        const SizedBox(height: 24),
        const Text('Your Pet', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        TextField(
          decoration: const InputDecoration(labelText: 'Pet Name', prefixIcon: Icon(Icons.badge), hintText: 'e.g. Luna, Max, Buddy'),
          onChanged: (v) => _petName = v,
        ),
        const SizedBox(height: 20),
        const Text('Species', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Row(children: _speciesOptions.entries.map((e) {
          final isSelected = _species == e.key;
          return Expanded(child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: GestureDetector(
              onTap: () => setState(() {
                _species = e.key;
                _climbs = e.key == 'cat';
              }),
              child: Container(
                padding: const EdgeInsets.symmetric(vertical: 18),
                decoration: BoxDecoration(
                  color: isSelected ? (e.value['color'] as Color).withOpacity(0.15) : Colors.grey[100],
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: isSelected ? e.value['color'] as Color : Colors.grey[300]!, width: isSelected ? 2 : 1),
                ),
                child: Column(children: [
                  Icon(e.value['icon'] as IconData, color: e.value['color'] as Color, size: 28),
                  const SizedBox(height: 6),
                  Text(e.key[0].toUpperCase() + e.key.substring(1), style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: isSelected ? e.value['color'] as Color : Colors.grey[600])),
                ]),
              ),
            ),
          ));
        }).toList()),
        const SizedBox(height: 20),
        const Text('Size', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(spacing: 8, children: ['small', 'medium', 'large', 'extra_large'].map((s) =>
          ChoiceChip(label: Text(s.replaceAll('_', ' ').toUpperCase()), selected: _size == s,
            onSelected: (_) => setState(() => _size = s), selectedColor: AppTheme.primaryColor.withOpacity(0.2)),
        ).toList()),
        const SizedBox(height: 20),
        const Text('Energy Level', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(spacing: 8, children: ['low', 'medium', 'high'].map((e) =>
          ChoiceChip(label: Text(e.toUpperCase()), selected: _energy == e,
            onSelected: (_) => setState(() => _energy = e), selectedColor: AppTheme.warningColor.withOpacity(0.2)),
        ).toList()),
        const SizedBox(height: 20),
        const Text('Behavioral Traits', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        SwitchListTile(title: const Text('Destructive (chews/scratches furniture)'), value: _isDestructive, onChanged: (v) => setState(() => _isDestructive = v)),
        SwitchListTile(title: const Text('Sheds fur'), value: _shedsFur, onChanged: (v) => setState(() => _shedsFur = v)),
        SwitchListTile(title: const Text('Climbs furniture'), value: _climbs, onChanged: (v) => setState(() => _climbs = v)),
        const SizedBox(height: 24),
        SizedBox(width: double.infinity, child: ElevatedButton.icon(
          onPressed: _isAnalyzing ? null : _analyzeRoom,
          icon: _isAnalyzing ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white)) : const Icon(Icons.shield),
          label: Text(_isAnalyzing ? 'Analyzing...' : 'Analyze Room Safety'),
          style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF8D6E63), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(vertical: 16)),
        )),
      ]),
    );
  }

  Widget _buildSafetyTab() {
    if (_analysis == null) return _emptyState('Create a pet profile and analyze first');
    final a = _analysis!;

    return SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Container(
        width: double.infinity, padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(gradient: LinearGradient(colors: [const Color(0xFF8D6E63), const Color(0xFFBCAAA4)]), borderRadius: BorderRadius.circular(20)),
        child: Column(children: [
          const Text('Pet Safety Score', style: TextStyle(color: Colors.white70)),
          const SizedBox(height: 8),
          Text(a.overallScore.toStringAsFixed(1), style: const TextStyle(color: Colors.white, fontSize: 48, fontWeight: FontWeight.bold)),
          Text('/ 10', style: TextStyle(color: Colors.white.withOpacity(0.6), fontSize: 18)),
          const SizedBox(height: 8),
          Text(a.scoreInterpretation, style: const TextStyle(color: Colors.white, fontSize: 12), textAlign: TextAlign.center),
        ]),
      ),
      const SizedBox(height: 16),
      _scoreRow('Safety', a.safetyScore, Icons.shield),
      _scoreRow('Comfort', a.comfortScore, Icons.weekend),
      _scoreRow('Durability', a.durabilityScore, Icons.build),
      _scoreRow('Cleanliness', a.cleanlinessScore, Icons.cleaning_services),
      const SizedBox(height: 20),
      if (a.hazards.isNotEmpty) ...[
        Text('Hazards (${a.hazards.length})', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        ...a.hazards.map((h) {
          final sevColor = h.severity == 'critical' ? AppTheme.errorColor : h.severity == 'high' ? Colors.deepOrange : AppTheme.warningColor;
          return Card(color: sevColor.withOpacity(0.05), margin: const EdgeInsets.only(bottom: 8), child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                Icon(Icons.warning_amber, color: sevColor, size: 18),
                const SizedBox(width: 6),
                Container(padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2), decoration: BoxDecoration(color: sevColor.withOpacity(0.1), borderRadius: BorderRadius.circular(6)),
                  child: Text(h.severity.toUpperCase(), style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: sevColor))),
                const SizedBox(width: 6),
                Expanded(child: Text(h.item, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14))),
                if (h.estimatedCost != null) Text('\$${h.estimatedCost!.toStringAsFixed(0)}', style: const TextStyle(fontWeight: FontWeight.w600)),
              ]),
              const SizedBox(height: 6),
              Text(h.description, style: TextStyle(fontSize: 13, color: Colors.grey[700])),
              const SizedBox(height: 6),
              Row(children: [const Icon(Icons.lightbulb, size: 14, color: AppTheme.successColor), const SizedBox(width: 4),
                Expanded(child: Text(h.solution, style: const TextStyle(fontSize: 12, color: AppTheme.successColor)))]),
            ]),
          ));
        }),
      ] else ...[
        Card(color: AppTheme.successColor.withOpacity(0.05), child: const ListTile(
          leading: Icon(Icons.check_circle, color: AppTheme.successColor),
          title: Text('No hazards detected!'),
          subtitle: Text('Your room appears safe for your pet'),
        )),
      ],
      const SizedBox(height: 16),
      if (a.cleaningTips.isNotEmpty) ...[
        const Text('Cleaning Tips', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        ...a.cleaningTips.take(5).map((tip) => Card(child: ListTile(
          leading: const Icon(Icons.cleaning_services, color: AppTheme.accentColor, size: 20),
          title: Text(tip, style: const TextStyle(fontSize: 13)),
        ))),
      ],
    ]));
  }

  Widget _buildZonesTab() {
    if (_analysis == null) return _emptyState('Analyze a room first');

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _analysis!.zonePlan.length + 1,
      itemBuilder: (ctx, i) {
        if (i == 0) return Padding(padding: const EdgeInsets.only(bottom: 16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Pet Zone Plan', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          Text('Designated areas for your pet\'s needs', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
        ]));
        final zone = _analysis!.zonePlan[i - 1];
        final typeIcons = {'rest': Icons.bed, 'dining': Icons.restaurant, 'activity': Icons.sports_soccer, 'enrichment': Icons.psychology, 'hygiene': Icons.wash, 'habitat': Icons.home};
        final icon = typeIcons[zone.zoneType] ?? Icons.place;

        return Card(margin: const EdgeInsets.only(bottom: 10), child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              CircleAvatar(backgroundColor: const Color(0xFF8D6E63).withOpacity(0.1), child: Icon(icon, color: const Color(0xFF8D6E63), size: 20)),
              const SizedBox(width: 12),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(zone.zoneName, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                Text(zone.location, style: TextStyle(color: Colors.grey[600], fontSize: 12)),
              ])),
              Text('\$${zone.estimatedCost.toStringAsFixed(0)}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
            ]),
            const SizedBox(height: 8),
            Text(zone.description, style: TextStyle(color: Colors.grey[700], fontSize: 13)),
            const SizedBox(height: 8),
            Wrap(spacing: 6, children: zone.itemsNeeded.map((item) => Chip(label: Text(item, style: const TextStyle(fontSize: 10)), materialTapTargetSize: MaterialTapTargetSize.shrinkWrap)).toList()),
          ]),
        ));
      },
    );
  }

  Widget _buildProductsTab() {
    if (_analysis == null || _analysis!.productRecommendations == null) return _emptyState('Run analysis to see product recommendations');

    final products = _analysis!.productRecommendations!;
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: products.length + 1,
      itemBuilder: (ctx, i) {
        if (i == 0) return Padding(padding: const EdgeInsets.only(bottom: 16), child: const Text('Recommended Products', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)));
        final p = products[i - 1];
        final priorityColor = p['priority'] == 'essential' ? AppTheme.errorColor : p['priority'] == 'recommended' ? AppTheme.warningColor : Colors.grey;
        final catIcons = {'bedding': Icons.bed, 'feeding': Icons.restaurant, 'safety': Icons.shield, 'furniture_protection': Icons.weekend,
          'cleaning': Icons.cleaning_services, 'enrichment': Icons.psychology, 'tech': Icons.smart_toy, 'furniture': Icons.chair,
          'hygiene': Icons.wash, 'habitat': Icons.home, 'health': Icons.favorite};

        return Card(margin: const EdgeInsets.only(bottom: 10), child: ListTile(
          leading: CircleAvatar(backgroundColor: priorityColor.withOpacity(0.1),
            child: Icon(catIcons[p['category']] ?? Icons.shopping_bag, color: priorityColor, size: 20)),
          title: Text(p['name'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
          subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(p['description'] ?? '', style: const TextStyle(fontSize: 12)),
            const SizedBox(height: 4),
            Row(children: [
              Container(padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2), decoration: BoxDecoration(color: priorityColor.withOpacity(0.1), borderRadius: BorderRadius.circular(6)),
                child: Text((p['priority'] ?? '').toString().toUpperCase(), style: TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: priorityColor))),
              const SizedBox(width: 8),
              Text(p['price_range'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ]),
          ]),
          isThreeLine: true,
        ));
      },
    );
  }

  Widget _scoreRow(String label, double score, IconData icon) {
    final color = score >= 7 ? AppTheme.successColor : score >= 5 ? AppTheme.warningColor : AppTheme.errorColor;
    return Padding(padding: const EdgeInsets.only(bottom: 6), child: Card(child: ListTile(
      leading: Icon(icon, color: color), title: Text(label),
      trailing: Row(mainAxisSize: MainAxisSize.min, children: [Text(score.toStringAsFixed(1), style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: color)), Text('/10', style: TextStyle(color: Colors.grey[400], fontSize: 12))]),
    )));
  }

  Widget _emptyState(String msg) => Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
    Icon(Icons.pets, size: 64, color: Colors.grey[300]), const SizedBox(height: 16),
    Text(msg, style: TextStyle(color: Colors.grey[500], fontSize: 16)),
  ]));
}
