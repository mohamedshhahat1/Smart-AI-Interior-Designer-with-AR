import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';

class RoomScanScreen extends StatefulWidget {
  const RoomScanScreen({super.key});

  @override
  State<RoomScanScreen> createState() => _RoomScanScreenState();
}

class _RoomScanScreenState extends State<RoomScanScreen> {
  final _apiService = ApiService();
  final _picker = ImagePicker();
  File? _selectedImage;
  Uint8List? _selectedImageBytes;
  XFile? _selectedXFile;
  bool _isAnalyzing = false;
  String? _selectedStyle;

  Future<void> _pickImage(ImageSource source) async {
    final picked = await _picker.pickImage(
      source: source,
      maxWidth: AppConstants.maxImageDimension,
      imageQuality: AppConstants.imageQuality,
    );
    if (picked != null) {
      final bytes = await picked.readAsBytes();
      setState(() {
        _selectedXFile = picked;
        _selectedImageBytes = bytes;
        if (!kIsWeb) {
          _selectedImage = File(picked.path);
        }
      });
    }
  }

  Future<void> _analyzeRoom() async {
    if (_selectedImageBytes == null) return;

    final hasToken = await ApiClient().hasToken();
    if (!hasToken) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Text('Please login first to analyze rooms'),
            action: SnackBarAction(
                label: 'Login', onPressed: () => context.go('/login')),
            duration: const Duration(seconds: 5),
          ),
        );
      }
      return;
    }

    setState(() => _isAnalyzing = true);

    try {
      final room = await _apiService.uploadRoomBytes(
        _selectedImageBytes!,
        _selectedXFile?.name ?? 'room_image.jpg',
      );

      if (mounted) {
        context.go('/design/${room.id}');
      }
    } catch (e, stackTrace) {
      debugPrint('Room upload error: $e');
      debugPrint('Stack trace: $stackTrace');
      if (mounted) {
        String errorMsg = 'Error: ${e.toString()}';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content: Text(errorMsg), duration: const Duration(seconds: 10)),
        );
      }
    } finally {
      if (mounted) setState(() => _isAnalyzing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan Room'),
        leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () => context.go('/')),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (_selectedImageBytes == null) ...[
              _buildCaptureOptions(),
            ] else ...[
              _buildImagePreview(),
              const SizedBox(height: 20),
              _buildStyleSelector(),
              const SizedBox(height: 20),
              _buildAnalyzeButton(),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildCaptureOptions() {
    return Column(
      children: [
        const SizedBox(height: 40),
        Icon(Icons.camera_alt, size: 80, color: Colors.grey[300]),
        const SizedBox(height: 16),
        Text('Capture or select a room photo',
            style: TextStyle(fontSize: 18, color: Colors.grey[600])),
        const SizedBox(height: 32),
        SizedBox(
          width: double.infinity,
          child: ElevatedButton.icon(
            onPressed: () => _pickImage(ImageSource.camera),
            icon: const Icon(Icons.camera_alt),
            label: const Text('Take Photo'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
        ),
        const SizedBox(height: 12),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () => _pickImage(ImageSource.gallery),
            icon: const Icon(Icons.photo_library),
            label: const Text('Choose from Gallery'),
            style: OutlinedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildImagePreview() {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: Stack(
        children: [
          if (kIsWeb && _selectedImageBytes != null)
            Image.memory(_selectedImageBytes!,
                width: double.infinity, height: 250, fit: BoxFit.cover)
          else if (_selectedImage != null)
            Image.file(_selectedImage!,
                width: double.infinity, height: 250, fit: BoxFit.cover),
          Positioned(
            top: 8,
            right: 8,
            child: IconButton(
              icon: const Icon(Icons.close, color: Colors.white),
              style: IconButton.styleFrom(backgroundColor: Colors.black54),
              onPressed: () => setState(() {
                _selectedImage = null;
                _selectedImageBytes = null;
                _selectedXFile = null;
              }),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStyleSelector() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Choose Design Style',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: AppConstants.supportedStyles.map((style) {
            final isSelected = _selectedStyle == style;
            return ChoiceChip(
              label: Text(style),
              selected: isSelected,
              onSelected: (selected) =>
                  setState(() => _selectedStyle = selected ? style : null),
              selectedColor: AppTheme.primaryColor.withOpacity(0.2),
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildAnalyzeButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: _isAnalyzing ? null : _analyzeRoom,
        style: ElevatedButton.styleFrom(
          backgroundColor: AppTheme.primaryColor,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 16),
        ),
        child: _isAnalyzing
            ? const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                          strokeWidth: 2, color: Colors.white)),
                  SizedBox(width: 12),
                  Text('Analyzing Room...'),
                ],
              )
            : const Text('Analyze & Generate Design',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
      ),
    );
  }
}
