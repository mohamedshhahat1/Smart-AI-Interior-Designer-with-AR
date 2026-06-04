import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class HouseProjectScreen extends StatefulWidget {
  const HouseProjectScreen({super.key});

  @override
  State<HouseProjectScreen> createState() => _HouseProjectScreenState();
}

class _HouseProjectScreenState extends State<HouseProjectScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _budgetController = TextEditingController();
  final _apiService = ApiService();

  String _selectedStyle = 'scandinavian';
  String _lightingPreference = 'Warm ambient lighting';
  final List<Map<String, String>> _rooms = [];
  final List<String> _selectedColors = [];
  bool _isCreating = false;

  final List<String> _availableColors = [
    'White', 'Light Blue', 'Natural Oak', 'Cream', 'Sage Green',
    'Charcoal', 'Terracotta', 'Navy', 'Blush Pink', 'Forest Green',
    'Gold', 'Slate Grey', 'Warm Beige', 'Dusty Rose', 'Olive',
  ];

  final List<String> _lightingOptions = [
    'Warm ambient lighting',
    'Bright natural light emphasis',
    'Layered lighting with dimmers',
    'Edison bulb industrial',
    'Recessed minimal lighting',
    'String lights and lanterns',
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    _budgetController.dispose();
    super.dispose();
  }

  void _addRoom() {
    showDialog(
      context: context,
      builder: (ctx) {
        String roomLabel = '';
        String roomType = 'living_room';
        return AlertDialog(
          title: const Text('Add Room'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                decoration: const InputDecoration(labelText: 'Room Name', hintText: 'e.g. Master Bedroom'),
                onChanged: (v) => roomLabel = v,
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: roomType,
                decoration: const InputDecoration(labelText: 'Room Type'),
                items: const [
                  DropdownMenuItem(value: 'living_room', child: Text('Living Room')),
                  DropdownMenuItem(value: 'bedroom', child: Text('Bedroom')),
                  DropdownMenuItem(value: 'kitchen', child: Text('Kitchen')),
                  DropdownMenuItem(value: 'bathroom', child: Text('Bathroom')),
                  DropdownMenuItem(value: 'dining_room', child: Text('Dining Room')),
                  DropdownMenuItem(value: 'office', child: Text('Office')),
                  DropdownMenuItem(value: 'hallway', child: Text('Hallway')),
                  DropdownMenuItem(value: 'studio', child: Text('Studio')),
                ],
                onChanged: (v) => roomType = v ?? roomType,
              ),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
            ElevatedButton(
              onPressed: () {
                if (roomLabel.isNotEmpty) {
                  setState(() {
                    _rooms.add({'room_label': roomLabel, 'room_type': roomType});
                  });
                  Navigator.pop(ctx);
                }
              },
              child: const Text('Add'),
            ),
          ],
        );
      },
    );
  }

  Future<void> _createProject() async {
    if (!_formKey.currentState!.validate()) return;
    if (_rooms.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Add at least one room')),
      );
      return;
    }

    setState(() => _isCreating = true);

    try {
      final dio = _apiService;
      final response = await ApiService().dio.post('/house/project', data: {
        'name': _nameController.text.trim(),
        'description': _descriptionController.text.trim().isEmpty
            ? null
            : _descriptionController.text.trim(),
        'style': _selectedStyle,
        'rooms': _rooms.map((r) => {
          return {'room_label': r['room_label'], 'room_type': r['room_type']};
        }).toList(),
        'budget': _budgetController.text.isNotEmpty
            ? double.tryParse(_budgetController.text)
            : null,
        'color_preferences': _selectedColors.isNotEmpty ? _selectedColors : null,
        'lighting_preference': _lightingPreference,
      });

      if (mounted) {
        final projectId = response.data['id'];
        context.go('/house/$projectId');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to create project')),
        );
      }
    } finally {
      if (mounted) setState(() => _isCreating = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('New House Project')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildSectionHeader('Project Details'),
              const SizedBox(height: 12),
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Project Name',
                  hintText: 'e.g. My Apartment Redesign',
                  prefixIcon: Icon(Icons.home),
                ),
                validator: (v) => v != null && v.length >= 2 ? null : 'Enter a project name',
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description (optional)',
                  hintText: 'Describe your vision...',
                  prefixIcon: Icon(Icons.description),
                ),
                maxLines: 2,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _budgetController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Total Budget (optional)',
                  hintText: 'e.g. 15000',
                  prefixIcon: Icon(Icons.attach_money),
                ),
              ),
              const SizedBox(height: 24),

              _buildSectionHeader('Design Style'),
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: AppConstants.supportedStyles.map((style) {
                  final styleKey = style.toLowerCase().replaceAll(' ', '_').replaceAll('-', '_');
                  final isSelected = _selectedStyle == styleKey;
                  return ChoiceChip(
                    label: Text(style),
                    selected: isSelected,
                    onSelected: (_) => setState(() => _selectedStyle = styleKey),
                    selectedColor: AppTheme.primaryColor.withOpacity(0.2),
                  );
                }).toList(),
              ),
              const SizedBox(height: 24),

              _buildSectionHeader('Color Preferences'),
              const SizedBox(height: 8),
              Text('Select colors for your unified palette', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: _availableColors.map((color) {
                  final isSelected = _selectedColors.contains(color);
                  return FilterChip(
                    label: Text(color),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() {
                        if (selected) {
                          _selectedColors.add(color);
                        } else {
                          _selectedColors.remove(color);
                        }
                      });
                    },
                    selectedColor: AppTheme.accentColor.withOpacity(0.2),
                    checkmarkColor: AppTheme.accentColor,
                  );
                }).toList(),
              ),
              const SizedBox(height: 24),

              _buildSectionHeader('Lighting'),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: _lightingPreference,
                decoration: const InputDecoration(
                  prefixIcon: Icon(Icons.light),
                ),
                items: _lightingOptions.map((opt) =>
                  DropdownMenuItem(value: opt, child: Text(opt)),
                ).toList(),
                onChanged: (v) => setState(() => _lightingPreference = v ?? _lightingPreference),
              ),
              const SizedBox(height: 24),

              _buildSectionHeader('Rooms (${_rooms.length})'),
              const SizedBox(height: 12),
              if (_rooms.isEmpty)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.grey[300]!, style: BorderStyle.solid),
                  ),
                  child: Column(
                    children: [
                      Icon(Icons.meeting_room, size: 40, color: Colors.grey[400]),
                      const SizedBox(height: 8),
                      Text('No rooms added yet', style: TextStyle(color: Colors.grey[500])),
                    ],
                  ),
                )
              else
                ...List.generate(_rooms.length, (i) {
                  final room = _rooms[i];
                  return Card(
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
                        child: Text('${i + 1}', style: const TextStyle(color: AppTheme.primaryColor, fontWeight: FontWeight.bold)),
                      ),
                      title: Text(room['room_label']!),
                      subtitle: Text(room['room_type']!.replaceAll('_', ' ')),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete_outline, color: Colors.red),
                        onPressed: () => setState(() => _rooms.removeAt(i)),
                      ),
                    ),
                  );
                }),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  onPressed: _addRoom,
                  icon: const Icon(Icons.add),
                  label: const Text('Add Room'),
                  style: OutlinedButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 14)),
                ),
              ),
              const SizedBox(height: 32),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isCreating ? null : _createProject,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryColor,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                  child: _isCreating
                      ? const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white)),
                            SizedBox(width: 12),
                            Text('Creating Project...'),
                          ],
                        )
                      : const Text('Create House Project', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                ),
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold));
  }
}
