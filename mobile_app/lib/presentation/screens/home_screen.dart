import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedNavIndex = 0;
  List<Map<String, dynamic>> _recentDesigns = [];
  bool _isLoadingDesigns = true;
  final _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _loadRecentDesigns();
  }

  Future<void> _loadRecentDesigns() async {
    try {
      final response = await ApiClient().dio.get('/room/');
      final rooms = response.data as List;

      List<Map<String, dynamic>> designs = [];
      for (final room in rooms.take(5)) {
        designs.add({
          'id': room['id'],
          'room_type': room['room_type'] ?? 'Room',
          'image_url': room['image_url'],
          'created_at': room['created_at'],
        });
      }

      if (mounted) {
        setState(() {
          _recentDesigns = designs;
          _isLoadingDesigns = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoadingDesigns = false);
      }
    }
  }

  void _onNavTap(int index) {
    setState(() => _selectedNavIndex = index);
    switch (index) {
      case 0:
        break;
      case 1:
        context.push('/scan').then((_) => _resetBottomNavigation());
        break;
      case 2:
        _openAssistantPicker();
        break;
      case 3:
        context.push('/profile').then((_) => _resetBottomNavigation());
        break;
    }
  }

  void _resetBottomNavigation() {
    if (mounted) setState(() => _selectedNavIndex = 0);
  }

  void _openAssistantPicker() {
    if (_recentDesigns.isNotEmpty) {
      context
          .push('/assistant/${_recentDesigns.first['id']}')
          .then((_) => _resetBottomNavigation());
    } else {
      _resetBottomNavigation();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Scan a room first to use the AI assistant')),
      );
    }
  }

  /// Resolves a real design id for the most recent room before navigating to a
  /// design-dependent route (AR / Cost). The home list holds room ids, but those
  /// routes require a design id, so we look up the room's designs first.
  Future<void> _openDesignRoute(String prefix, String emptyMessage) async {
    if (_recentDesigns.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(emptyMessage)),
      );
      return;
    }
    final roomId = _recentDesigns.first['id'].toString();
    try {
      final designs = await _apiService.listDesigns(roomId: roomId);
      if (!mounted) return;
      if (designs.isNotEmpty) {
        context.push('$prefix/${designs.first.id}');
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Generate a design for this room first')),
        );
        context.push('/design/$roomId');
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not load designs for this room')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 20),
              Text(
                'Smart Interior AI',
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 8),
              Text(
                'Redesign your space with AI-powered interior design',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: Colors.grey[600],
                    ),
              ),
              const SizedBox(height: 32),
              _buildScanCard(context),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                      child: _buildFeatureCard(
                    context,
                    icon: Icons.auto_awesome,
                    title: 'AI Design',
                    subtitle: 'Generate designs',
                    color: AppTheme.secondaryColor,
                    onTap: () {
                      if (_recentDesigns.isNotEmpty) {
                        context.push('/design/${_recentDesigns.first['id']}');
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Scan a room first to generate designs')),
                        );
                      }
                    },
                  )),
                  const SizedBox(width: 12),
                  Expanded(
                      child: _buildFeatureCard(
                    context,
                    icon: Icons.view_in_ar,
                    title: 'AR View',
                    subtitle: 'See in your room',
                    color: AppTheme.accentColor,
                    onTap: () => _openDesignRoute(
                      '/ar',
                      'Generate a design first to use AR view',
                    ),
                  )),
                ],
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                      child: _buildFeatureCard(
                    context,
                    icon: Icons.chair,
                    title: 'Furniture',
                    subtitle: 'Get recommendations',
                    color: AppTheme.successColor,
                    onTap: () {
                      if (_recentDesigns.isNotEmpty) {
                        context.push('/furniture/${_recentDesigns.first['id']}');
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Scan a room first to get furniture recommendations')),
                        );
                      }
                    },
                  )),
                  const SizedBox(width: 12),
                  Expanded(
                      child: _buildFeatureCard(
                    context,
                    icon: Icons.calculate,
                    title: 'Cost',
                    subtitle: 'Estimate budget',
                    color: AppTheme.warningColor,
                    onTap: () => _openDesignRoute(
                      '/cost',
                      'Generate a design first to estimate costs',
                    ),
                  )),
                ],
              ),
              const SizedBox(height: 16),
              _buildMultiRoomCard(context),
              const SizedBox(height: 12),
              _buildSmartLightingCard(context),
              const SizedBox(height: 12),
              _buildFengShuiCard(context),
              const SizedBox(height: 12),
              _buildSeasonalCard(context),
              const SizedBox(height: 12),
              _buildPetFriendlyCard(context),
              const SizedBox(height: 12),
              _build3DWalkthroughCard(context),
              const SizedBox(height: 24),
              Text(
                'Recent Rooms',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 12),
              _buildRecentDesigns(context),
            ],
          ),
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedNavIndex,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.camera_alt), label: 'Scan'),
          NavigationDestination(icon: Icon(Icons.chat), label: 'Assistant'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
        onDestinationSelected: _onNavTap,
      ),
    );
  }

  Widget _buildRecentDesigns(BuildContext context) {
    if (_isLoadingDesigns) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (_recentDesigns.isEmpty) {
      return _buildEmptyState(context);
    }

    return Column(
      children: _recentDesigns.map((design) {
        return Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
              child: const Icon(Icons.design_services, color: AppTheme.primaryColor),
            ),
            title: Text(
              design['room_type'] as String? ?? 'Room',
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
            subtitle: Text(
              _formatDate(design['created_at'] as String?),
              style: TextStyle(color: Colors.grey[500], fontSize: 12),
            ),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () => context.push('/design/${design['id']}'),
          ),
        );
      }).toList(),
    );
  }

  String _formatDate(String? dateStr) {
    if (dateStr == null) return '';
    try {
      final date = DateTime.parse(dateStr);
      final now = DateTime.now();
      final diff = now.difference(date);
      if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
      if (diff.inHours < 24) return '${diff.inHours}h ago';
      if (diff.inDays < 7) return '${diff.inDays}d ago';
      return '${date.day}/${date.month}/${date.year}';
    } catch (e) {
      return '';
    }
  }

  Widget _buildScanCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/scan'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Icon(Icons.camera_alt, color: Colors.white, size: 40),
            const SizedBox(height: 16),
            const Text(
              'Scan Your Room',
              style: TextStyle(
                color: Colors.white,
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Take a photo and let AI redesign your space',
              style:
                  TextStyle(color: Colors.white.withOpacity(0.9), fontSize: 14),
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(25),
              ),
              child: const Text(
                'Start Scanning',
                style: TextStyle(
                  color: AppTheme.primaryColor,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMultiRoomCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/house/new'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [AppTheme.accentColor, AppTheme.successColor],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.home_work, color: Colors.white, size: 32),
                  const SizedBox(height: 12),
                  const Text(
                    'Multi-Room House Design',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Redesign your entire home with a unified theme',
                    style: TextStyle(
                        color: Colors.white.withOpacity(0.9), fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.arrow_forward, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSmartLightingCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/lighting'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [const Color(0xFF9575CD), const Color(0xFFFFB74D)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.lightbulb, color: Colors.white, size: 32),
                  const SizedBox(height: 12),
                  const Text(
                    'Smart Lighting & Mood',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'AI-powered lighting that adapts to your mood',
                    style: TextStyle(
                        color: Colors.white.withOpacity(0.9), fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.arrow_forward, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFengShuiCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/feng-shui'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [const Color(0xFF8B4513), const Color(0xFFD2691E)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.compass_calibration,
                      color: Colors.white, size: 32),
                  const SizedBox(height: 12),
                  const Text(
                    'Feng Shui Analysis',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Harmonize your space with ancient wisdom + AI',
                    style: TextStyle(
                        color: Colors.white.withOpacity(0.9), fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.arrow_forward, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSeasonalCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/seasonal'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [const Color(0xFFFF8A65), const Color(0xFF81C784)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.park, color: Colors.white, size: 32),
                  const SizedBox(height: 12),
                  const Text(
                    'Seasonal & Holiday Themes',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Plan seasonal decor for a scanned room',
                    style: TextStyle(
                        color: Colors.white.withOpacity(0.9), fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.arrow_forward, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPetFriendlyCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/pet-friendly'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [const Color(0xFF8D6E63), const Color(0xFFFFCC80)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.pets, color: Colors.white, size: 32),
                  const SizedBox(height: 12),
                  const Text(
                    'Pet-Friendly Design',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Design a safe, comfortable room for you and your pets',
                    style: TextStyle(
                        color: Colors.white.withOpacity(0.9), fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.arrow_forward, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _build3DWalkthroughCard(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/3d-walkthrough'),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [const Color(0xFF1A1A2E), const Color(0xFF16213E)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(Icons.view_in_ar, color: Colors.white, size: 32),
                  const SizedBox(height: 12),
                  const Text(
                    '3D Room Walkthrough',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Explore your redesigned room in interactive 3D',
                    style: TextStyle(
                        color: Colors.white.withOpacity(0.9), fontSize: 13),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.arrow_forward, color: Colors.white),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String subtitle,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 12),
            Text(title,
                style:
                    const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
            const SizedBox(height: 4),
            Text(subtitle,
                style: TextStyle(color: Colors.grey[600], fontSize: 12)),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        children: [
          Icon(Icons.design_services, size: 48, color: Colors.grey[400]),
          const SizedBox(height: 12),
          Text(
            'No designs yet',
            style: TextStyle(color: Colors.grey[600], fontSize: 16),
          ),
          const SizedBox(height: 4),
          Text(
            'Scan a room to get started',
            style: TextStyle(color: Colors.grey[400], fontSize: 13),
          ),
        ],
      ),
    );
  }
}
