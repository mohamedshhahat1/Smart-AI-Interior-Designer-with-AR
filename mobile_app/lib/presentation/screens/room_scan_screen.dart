import 'dart:io';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';
import 'package:smart_interior_ai/data/services/api_service.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';

class RoomScanScreen extends StatefulWidget {
  const RoomScanScreen({super.key});

  @override
  State<RoomScanScreen> createState() => _RoomScanScreenState();
}

class _RoomScanScreenState extends State<RoomScanScreen> with WidgetsBindingObserver {
  final _apiService = ApiService();
  final _picker = ImagePicker();
  File? _selectedImage;
  Uint8List? _selectedImageBytes;
  XFile? _selectedXFile;
  bool _isAnalyzing = false;
  String? _selectedStyle;

  CameraController? _cameraController;
  bool _isCameraOpen = false;
  bool _isCameraInitializing = false;
  FlashMode _flashMode = FlashMode.auto;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _cameraController?.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      return;
    }
    if (state == AppLifecycleState.inactive) {
      _cameraController?.dispose();
      _cameraController = null;
    } else if (state == AppLifecycleState.resumed && _isCameraOpen) {
      _initCamera();
    }
  }

  Future<void> _initCamera() async {
    setState(() => _isCameraInitializing = true);

    final status = await Permission.camera.request();
    if (!status.isGranted) {
      if (mounted) {
        setState(() => _isCameraInitializing = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Camera permission is required')),
        );
      }
      return;
    }

    try {
      final cameras = await availableCameras();
      if (cameras.isEmpty) {
        if (mounted) {
          setState(() => _isCameraInitializing = false);
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('No camera found on this device')),
          );
        }
        return;
      }

      final backCamera = cameras.firstWhere(
        (c) => c.lensDirection == CameraLensDirection.back,
        orElse: () => cameras.first,
      );

      _cameraController?.dispose();
      _cameraController = CameraController(
        backCamera,
        ResolutionPreset.high,
        enableAudio: false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );

      await _cameraController!.initialize();
      await _cameraController!.setFlashMode(_flashMode);

      if (mounted) {
        setState(() {
          _isCameraOpen = true;
          _isCameraInitializing = false;
        });
      }
    } catch (e) {
      debugPrint('Camera init error: $e');
      if (mounted) {
        setState(() => _isCameraInitializing = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Camera error: ${e.toString()}')),
        );
      }
    }
  }

  Future<void> _capturePhoto() async {
    if (_cameraController == null || !_cameraController!.value.isInitialized) {
      return;
    }
    if (_cameraController!.value.isTakingPicture) return;

    try {
      final xFile = await _cameraController!.takePicture();
      final bytes = await xFile.readAsBytes();

      _cameraController?.dispose();
      _cameraController = null;

      if (mounted) {
        setState(() {
          _selectedXFile = xFile;
          _selectedImageBytes = bytes;
          if (!kIsWeb) {
            _selectedImage = File(xFile.path);
          }
          _isCameraOpen = false;
        });
      }
    } catch (e) {
      debugPrint('Capture error: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Capture failed: ${e.toString()}')),
        );
      }
    }
  }

  void _closeCamera() {
    _cameraController?.dispose();
    _cameraController = null;
    setState(() => _isCameraOpen = false);
  }

  void _toggleFlash() {
    if (_cameraController == null) return;
    setState(() {
      switch (_flashMode) {
        case FlashMode.auto:
          _flashMode = FlashMode.always;
          break;
        case FlashMode.always:
          _flashMode = FlashMode.off;
          break;
        default:
          _flashMode = FlashMode.auto;
      }
    });
    _cameraController!.setFlashMode(_flashMode);
  }

  IconData get _flashIcon {
    switch (_flashMode) {
      case FlashMode.auto:
        return Icons.flash_auto;
      case FlashMode.always:
        return Icons.flash_on;
      case FlashMode.off:
        return Icons.flash_off;
      default:
        return Icons.flash_auto;
    }
  }

  Future<void> _pickFromGallery() async {
    final picked = await _picker.pickImage(
      source: ImageSource.gallery,
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
        final stylePath = _selectedStyle != null
            ? '/design/${room.id}?style=${Uri.encodeComponent(_selectedStyle!)}'
            : '/design/${room.id}';
        context.go(stylePath);
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
    if (_isCameraOpen) {
      return _buildCameraView();
    }

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

  Widget _buildCameraView() {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(
          fit: StackFit.expand,
          children: [
            if (_cameraController != null &&
                _cameraController!.value.isInitialized)
              Center(
                child: AspectRatio(
                  aspectRatio: _cameraController!.value.aspectRatio,
                  child: CameraPreview(_cameraController!),
                ),
              )
            else
              const Center(
                child: CircularProgressIndicator(color: Colors.white),
              ),

            Positioned(
              top: 16,
              left: 16,
              right: 16,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white, size: 28),
                    style: IconButton.styleFrom(backgroundColor: Colors.black45),
                    onPressed: _closeCamera,
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.black45,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Text(
                      'Point at your room',
                      style: TextStyle(color: Colors.white, fontSize: 14),
                    ),
                  ),
                  IconButton(
                    icon: Icon(_flashIcon, color: Colors.white, size: 28),
                    style: IconButton.styleFrom(backgroundColor: Colors.black45),
                    onPressed: _toggleFlash,
                  ),
                ],
              ),
            ),

            Positioned(
              bottom: 40,
              left: 0,
              right: 0,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  IconButton(
                    icon: const Icon(Icons.photo_library,
                        color: Colors.white, size: 30),
                    onPressed: () {
                      _closeCamera();
                      _pickFromGallery();
                    },
                  ),
                  GestureDetector(
                    onTap: _capturePhoto,
                    child: Container(
                      width: 72,
                      height: 72,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.white, width: 4),
                      ),
                      child: Container(
                        margin: const EdgeInsets.all(4),
                        decoration: const BoxDecoration(
                          shape: BoxShape.circle,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 48),
                ],
              ),
            ),
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
            onPressed: _isCameraInitializing ? null : _initCamera,
            icon: _isCameraInitializing
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(
                        strokeWidth: 2, color: Colors.white),
                  )
                : const Icon(Icons.camera_alt),
            label: Text(_isCameraInitializing ? 'Opening Camera...' : 'Take Photo'),
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
            onPressed: _pickFromGallery,
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
          Positioned(
            bottom: 8,
            right: 8,
            child: IconButton(
              icon: const Icon(Icons.camera_alt, color: Colors.white),
              style: IconButton.styleFrom(backgroundColor: Colors.black54),
              onPressed: _initCamera,
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
