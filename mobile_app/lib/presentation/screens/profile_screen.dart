import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _apiService = ApiService();
  Map<String, dynamic>? _user;
  List<Map<String, dynamic>> _rooms = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final profile = await _apiService.getProfile();
      _user = profile;

      try {
        final roomsResponse = await ApiClient().dio.get('/room/');
        _rooms = (roomsResponse.data as List).cast<Map<String, dynamic>>();
      } catch (_) {}

      if (mounted) setState(() => _isLoading = false);
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Failed to load profile. Please log in.';
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _logout() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Sign Out'),
        content: const Text('Are you sure you want to sign out?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Sign Out', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirm == true && mounted) {
      await ApiClient().clearToken();
      if (mounted) context.go('/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          if (_user != null)
            IconButton(
              icon: const Icon(Icons.logout),
              onPressed: _logout,
              tooltip: 'Sign Out',
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _errorMessage != null
              ? _buildErrorState()
              : _buildProfileContent(),
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.person_off, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text(_errorMessage!, style: const TextStyle(color: Colors.grey, fontSize: 16)),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () => context.go('/login'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppTheme.primaryColor,
                foregroundColor: Colors.white,
              ),
              child: const Text('Sign In'),
            ),
            const SizedBox(height: 12),
            TextButton(onPressed: _loadProfile, child: const Text('Retry')),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileContent() {
    final name = _user?['name'] ?? 'User';
    final email = _user?['email'] ?? '';
    final createdAt = _user?['created_at'] as String?;
    final initials = name.isNotEmpty ? name[0].toUpperCase() : 'U';

    return RefreshIndicator(
      onRefresh: _loadProfile,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const SizedBox(height: 20),
          Center(
            child: CircleAvatar(
              radius: 50,
              backgroundColor: AppTheme.primaryColor,
              child: Text(
                initials,
                style: const TextStyle(fontSize: 36, fontWeight: FontWeight.bold, color: Colors.white),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Center(
            child: Text(
              name,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
            ),
          ),
          const SizedBox(height: 4),
          Center(
            child: Text(email, style: TextStyle(color: Colors.grey[600], fontSize: 15)),
          ),
          if (createdAt != null) ...[
            const SizedBox(height: 4),
            Center(
              child: Text(
                'Member since ${_formatDate(createdAt)}',
                style: TextStyle(color: Colors.grey[400], fontSize: 13),
              ),
            ),
          ],
          const SizedBox(height: 32),
          _buildStatsRow(),
          const SizedBox(height: 24),
          _buildSectionTitle('Account'),
          _buildMenuItem(Icons.person_outline, 'Edit Profile', () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Profile editing coming soon')),
            );
          }),
          _buildMenuItem(Icons.lock_outline, 'Change Password', () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Password change coming soon')),
            );
          }),
          const SizedBox(height: 16),
          _buildSectionTitle('My Rooms'),
          if (_rooms.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16),
              child: Text('No rooms scanned yet', style: TextStyle(color: Colors.grey[500])),
            )
          else
            ..._rooms.take(5).map((room) => _buildRoomTile(room)),
          const SizedBox(height: 24),
          _buildSectionTitle('App'),
          _buildMenuItem(Icons.info_outline, 'About', () {
            showAboutDialog(
              context: context,
              applicationName: 'Smart Interior AI',
              applicationVersion: '1.0.0',
              children: [const Text('AI-Powered Room Redesign with AR Visualization')],
            );
          }),
          const SizedBox(height: 32),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: _logout,
              icon: const Icon(Icons.logout, color: Colors.red),
              label: const Text('Sign Out', style: TextStyle(color: Colors.red)),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: Colors.red),
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
            ),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildStatsRow() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildStat('Rooms', _rooms.length.toString()),
        _buildStat('Designs', '-'),
        _buildStat('AR Sessions', '-'),
      ],
    );
  }

  Widget _buildStat(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: AppTheme.primaryColor)),
        const SizedBox(height: 4),
        Text(label, style: TextStyle(color: Colors.grey[600], fontSize: 13)),
      ],
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildMenuItem(IconData icon, String title, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppTheme.primaryColor),
        title: Text(title),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: onTap,
      ),
    );
  }

  Widget _buildRoomTile(Map<String, dynamic> room) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
          child: const Icon(Icons.meeting_room, color: AppTheme.primaryColor),
        ),
        title: Text(room['room_type'] as String? ?? 'Room', style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(_formatDate(room['created_at'] as String?), style: TextStyle(color: Colors.grey[500], fontSize: 12)),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () => context.go('/design/${room['id']}'),
      ),
    );
  }

  String _formatDate(String? dateStr) {
    if (dateStr == null) return '';
    try {
      final date = DateTime.parse(dateStr);
      return '${date.day}/${date.month}/${date.year}';
    } catch (e) {
      return '';
    }
  }
}
