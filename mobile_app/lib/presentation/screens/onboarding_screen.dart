import 'dart:math' as math;
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lottie/lottie.dart';
import 'package:smart_interior_ai/data/repositories/onboarding_repository.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key, this.onFinished});

  final Future<void> Function()? onFinished;

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen>
    with TickerProviderStateMixin {
  late final PageController _pageController;
  late final AnimationController _ambientController;
  late final AnimationController _ctaController;
  int _currentPage = 0;
  bool _isFinishing = false;

  @override
  void initState() {
    super.initState();
    _pageController = PageController();
    _ambientController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 7),
    )..repeat();
    _ctaController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1300),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _pageController.dispose();
    _ambientController.dispose();
    _ctaController.dispose();
    super.dispose();
  }

  Future<void> _finishOnboarding() async {
    if (_isFinishing) return;
    setState(() => _isFinishing = true);

    if (widget.onFinished != null) {
      await widget.onFinished!();
    } else {
      await OnboardingRepository().complete();
      if (mounted) context.go('/login');
    }

    if (mounted) setState(() => _isFinishing = false);
  }

  Future<void> _nextPage() async {
    if (_currentPage == _pages.length - 1) {
      await _finishOnboarding();
      return;
    }

    await _pageController.nextPage(
      duration: const Duration(milliseconds: 620),
      curve: Curves.easeOutCubic,
    );
  }

  @override
  Widget build(BuildContext context) {
    final page = _pages[_currentPage];
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      body: AnimatedContainer(
        duration: const Duration(milliseconds: 700),
        curve: Curves.easeOutCubic,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: isDark
                ? [
                    const Color(0xFF050816),
                    Color.lerp(const Color(0xFF0C1631), page.accent, 0.14)!,
                    const Color(0xFF090B17),
                  ]
                : [
                    const Color(0xFFF8FAFF),
                    Color.lerp(Colors.white, page.accent, 0.09)!,
                    const Color(0xFFF3F6FF),
                  ],
          ),
        ),
        child: Stack(
          children: [
            _AmbientGlow(
              animation: _ambientController,
              accent: page.accent,
              isDark: isDark,
            ),
            Positioned.fill(
              child: IgnorePointer(
                child: Opacity(
                  opacity: isDark ? 0.42 : 0.25,
                  child: Lottie.asset(
                    'assets/animations/ai-particles.json',
                    fit: BoxFit.cover,
                    repeat: true,
                  ),
                ),
              ),
            ),
            SafeArea(
              child: Column(
                children: [
                  _TopBar(
                    onSkip: _isFinishing ? null : _finishOnboarding,
                  ),
                  Expanded(
                    child: PageView.builder(
                      controller: _pageController,
                      physics: const BouncingScrollPhysics(),
                      itemCount: _pages.length,
                      onPageChanged: (index) {
                        setState(() => _currentPage = index);
                      },
                      itemBuilder: (context, index) => _AnimatedPage(
                        index: index,
                        pageController: _pageController,
                        data: _pages[index],
                        ambientAnimation: _ambientController,
                      ),
                    ),
                  ),
                  _BottomControls(
                    currentPage: _currentPage,
                    pageCount: _pages.length,
                    accent: page.accent,
                    isLoading: _isFinishing,
                    pulseAnimation: _ctaController,
                    onNext: _nextPage,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _TopBar extends StatelessWidget {
  const _TopBar({required this.onSkip});

  final VoidCallback? onSkip;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 10, 14, 4),
      child: Row(
        children: [
          Hero(
            tag: 'smart-interior-brand',
            child: Material(
              color: Colors.transparent,
              child: Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF2F80FF), Color(0xFF8A5CFF)],
                  ),
                  borderRadius: BorderRadius.circular(15),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF4C7DFF).withValues(alpha: 0.28),
                      blurRadius: 20,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.auto_awesome_rounded,
                  color: Colors.white,
                  size: 23,
                ),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'INTERIOR AI',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.labelLarge?.copyWith(
                        fontWeight: FontWeight.w800,
                        letterSpacing: 1.5,
                      ),
                ),
                Text(
                  'Design intelligence',
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: Theme.of(context).textTheme.labelSmall?.copyWith(
                        color: colorScheme.onSurfaceVariant,
                      ),
                ),
              ],
            ),
          ),
          TextButton(
            key: const Key('onboarding_skip'),
            onPressed: onSkip,
            style: TextButton.styleFrom(
              foregroundColor: colorScheme.onSurfaceVariant,
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              shape: const StadiumBorder(),
            ),
            child: const Text('Skip'),
          ),
        ],
      ),
    );
  }
}

class _AnimatedPage extends StatelessWidget {
  const _AnimatedPage({
    required this.index,
    required this.pageController,
    required this.data,
    required this.ambientAnimation,
  });

  final int index;
  final PageController pageController;
  final _OnboardingPageData data;
  final Animation<double> ambientAnimation;

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: pageController,
      builder: (context, child) {
        final page = pageController.hasClients
            ? pageController.page ?? index.toDouble()
            : index.toDouble();
        final distance = (page - index).abs().clamp(0.0, 1.0);
        final scale = 1 - (distance * 0.055);
        final opacity = (1 - (distance * 0.38)).clamp(0.0, 1.0);

        return Opacity(
          opacity: opacity,
          child: Transform.translate(
            offset: Offset((page - index) * -26, distance * 14),
            child: Transform.scale(scale: scale, child: child),
          ),
        );
      },
      child: _OnboardingPage(
        key: Key('onboarding_page_$index'),
        index: index,
        data: data,
        ambientAnimation: ambientAnimation,
      ),
    );
  }
}

class _OnboardingPage extends StatelessWidget {
  const _OnboardingPage({
    super.key,
    required this.index,
    required this.data,
    required this.ambientAnimation,
  });

  final int index;
  final _OnboardingPageData data;
  final Animation<double> ambientAnimation;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isWide = constraints.maxWidth >= 760;
        final horizontalPadding = isWide ? 48.0 : 22.0;
        final visualHeight = isWide
            ? math.min(460.0, constraints.maxHeight - 36)
            : (constraints.maxHeight * 0.56).clamp(245.0, 390.0);

        final visual = _PremiumVisual(
          index: index,
          data: data,
          animation: ambientAnimation,
          height: visualHeight,
        );
        final copy =
            _PageCopy(data: data, compact: constraints.maxHeight < 610);

        return SingleChildScrollView(
          physics: const ClampingScrollPhysics(),
          padding:
              EdgeInsets.fromLTRB(horizontalPadding, 10, horizontalPadding, 10),
          child: ConstrainedBox(
            constraints: BoxConstraints(minHeight: constraints.maxHeight - 20),
            child: isWide
                ? Row(
                    children: [
                      Expanded(flex: 11, child: visual),
                      const SizedBox(width: 48),
                      Expanded(flex: 9, child: copy),
                    ],
                  )
                : Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      visual,
                      const SizedBox(height: 24),
                      copy,
                    ],
                  ),
          ),
        );
      },
    );
  }
}

class _PremiumVisual extends StatelessWidget {
  const _PremiumVisual({
    required this.index,
    required this.data,
    required this.animation,
    required this.height,
  });

  final int index;
  final _OnboardingPageData data;
  final Animation<double> animation;
  final double height;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return AnimatedBuilder(
      animation: animation,
      builder: (context, child) {
        final wave = math.sin(animation.value * math.pi * 2);
        return Transform.translate(
          offset: Offset(0, wave * 4),
          child: child,
        );
      },
      child: SizedBox(
        height: height,
        width: double.infinity,
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            Positioned.fill(
              child: Container(
                padding: const EdgeInsets.all(1.2),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.white.withValues(alpha: isDark ? 0.35 : 0.9),
                      data.accent.withValues(alpha: 0.72),
                      Colors.white.withValues(alpha: 0.12),
                    ],
                  ),
                  borderRadius: BorderRadius.circular(32),
                  boxShadow: [
                    BoxShadow(
                      color: data.accent.withValues(
                        alpha: isDark ? 0.22 : 0.16,
                      ),
                      blurRadius: 42,
                      spreadRadius: -8,
                      offset: const Offset(0, 22),
                    ),
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(31),
                  child: Stack(
                    fit: StackFit.expand,
                    children: [
                      Image.asset(data.imageAsset, fit: BoxFit.cover),
                      DecoratedBox(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.topCenter,
                            end: Alignment.bottomCenter,
                            colors: [
                              Colors.transparent,
                              const Color(0xFF050816).withValues(alpha: 0.08),
                              const Color(0xFF050816).withValues(alpha: 0.54),
                            ],
                          ),
                        ),
                      ),
                      _VisualOverlay(
                        index: index,
                        accent: data.accent,
                        animation: animation,
                      ),
                      Positioned(
                        left: 16,
                        top: 16,
                        child: _GlassChip(
                          icon: data.icon,
                          label: data.visualLabel,
                          accent: data.accent,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            ..._buildFloatingChips(),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildFloatingChips() {
    return [
      Positioned(
        right: -8,
        bottom: 46,
        child: _GlassChip(
          icon: data.floatingIcons.first,
          label: data.floatingLabels.first,
          accent: data.accent,
          compact: true,
        ),
      ),
      Positioned(
        left: -6,
        bottom: 18,
        child: _GlassChip(
          icon: data.floatingIcons.last,
          label: data.floatingLabels.last,
          accent: data.secondaryAccent,
          compact: true,
        ),
      ),
    ];
  }
}

class _VisualOverlay extends StatelessWidget {
  const _VisualOverlay({
    required this.index,
    required this.accent,
    required this.animation,
  });

  final int index;
  final Color accent;
  final Animation<double> animation;

  @override
  Widget build(BuildContext context) {
    if (index == 1) {
      return AnimatedBuilder(
        animation: animation,
        builder: (context, _) => Stack(
          children: [
            Positioned(
              left: 12,
              right: 12,
              top: 22 + ((animation.value * 0.72) * 280),
              child: Container(
                height: 2,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [
                      Colors.transparent,
                      accent,
                      Colors.white,
                      accent,
                      Colors.transparent,
                    ],
                  ),
                  boxShadow: [BoxShadow(color: accent, blurRadius: 14)],
                ),
              ),
            ),
            Center(
              child: Container(
                width: 72,
                height: 72,
                decoration: BoxDecoration(
                  border: Border.all(color: accent.withValues(alpha: 0.7)),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Icon(Icons.center_focus_strong_rounded, color: accent),
              ),
            ),
          ],
        ),
      );
    }

    if (index == 2) {
      return Center(
        child: AnimatedBuilder(
          animation: animation,
          builder: (context, _) {
            final scale =
                0.9 + (math.sin(animation.value * math.pi * 2) * 0.08);
            return Transform.scale(
              scale: scale,
              child: Container(
                width: 90,
                height: 90,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: accent.withValues(alpha: 0.8)),
                ),
                child: Icon(Icons.view_in_ar_rounded, color: accent, size: 30),
              ),
            );
          },
        ),
      );
    }

    return const SizedBox.shrink();
  }
}

class _PageCopy extends StatelessWidget {
  const _PageCopy({required this.data, required this.compact});

  final _OnboardingPageData data;
  final bool compact;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    return ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 570),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
            decoration: BoxDecoration(
              color: data.accent.withValues(alpha: 0.11),
              borderRadius: BorderRadius.circular(99),
              border: Border.all(color: data.accent.withValues(alpha: 0.22)),
            ),
            child: Text(
              data.eyebrow,
              style: theme.textTheme.labelSmall?.copyWith(
                color: data.accent,
                fontWeight: FontWeight.w800,
                letterSpacing: 1.35,
              ),
            ),
          ),
          SizedBox(height: compact ? 12 : 18),
          ShaderMask(
            blendMode: BlendMode.srcIn,
            shaderCallback: (bounds) => LinearGradient(
              colors: [colorScheme.onSurface, data.accent],
              stops: const [0.32, 1],
            ).createShader(bounds),
            child: Text(
              data.title,
              style: theme.textTheme.headlineLarge?.copyWith(
                fontSize: compact ? 29 : 34,
                height: 1.08,
                letterSpacing: -1.25,
                fontWeight: FontWeight.w800,
              ),
            ),
          ),
          SizedBox(height: compact ? 10 : 14),
          Text(
            data.subtitle,
            style: theme.textTheme.bodyLarge?.copyWith(
              color: colorScheme.onSurfaceVariant,
              height: 1.55,
              fontSize: compact ? 14 : 16,
            ),
          ),
          SizedBox(height: compact ? 14 : 20),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: data.highlights
                .map(
                  (label) => Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 11, vertical: 7),
                    decoration: BoxDecoration(
                      color: colorScheme.surface.withValues(alpha: 0.54),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color:
                            colorScheme.outlineVariant.withValues(alpha: 0.45),
                      ),
                    ),
                    child: Text(
                      label,
                      style: theme.textTheme.labelMedium?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }
}

class _BottomControls extends StatelessWidget {
  const _BottomControls({
    required this.currentPage,
    required this.pageCount,
    required this.accent,
    required this.isLoading,
    required this.pulseAnimation,
    required this.onNext,
  });

  final int currentPage;
  final int pageCount;
  final Color accent;
  final bool isLoading;
  final Animation<double> pulseAnimation;
  final VoidCallback onNext;

  bool get isLast => currentPage == pageCount - 1;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(22, 8, 22, 18),
      child: Row(
        children: [
          Semantics(
            label: 'Page ${currentPage + 1} of $pageCount',
            child: Row(
              children: List.generate(
                pageCount,
                (index) => AnimatedContainer(
                  duration: const Duration(milliseconds: 360),
                  curve: Curves.easeOutCubic,
                  width: index == currentPage ? 34 : 8,
                  height: 8,
                  margin: const EdgeInsets.only(right: 7),
                  decoration: BoxDecoration(
                    color: index == currentPage
                        ? accent
                        : Theme.of(context).colorScheme.outlineVariant,
                    borderRadius: BorderRadius.circular(99),
                    boxShadow: index == currentPage
                        ? [
                            BoxShadow(
                              color: accent.withValues(alpha: 0.35),
                              blurRadius: 12,
                            )
                          ]
                        : null,
                  ),
                ),
              ),
            ),
          ),
          const Spacer(),
          AnimatedBuilder(
            animation: pulseAnimation,
            builder: (context, child) {
              final scale = isLast ? 1 + (pulseAnimation.value * 0.025) : 1.0;
              return Transform.scale(scale: scale, child: child);
            },
            child: _GradientButton(
              key: Key(isLast ? 'onboarding_get_started' : 'onboarding_next'),
              label: isLast ? 'Get Started' : 'Next',
              icon: isLast
                  ? Icons.auto_awesome_rounded
                  : Icons.arrow_forward_rounded,
              accent: accent,
              expanded: isLast,
              isLoading: isLoading,
              onPressed: isLoading ? null : onNext,
            ),
          ),
        ],
      ),
    );
  }
}

class _GradientButton extends StatelessWidget {
  const _GradientButton({
    super.key,
    required this.label,
    required this.icon,
    required this.accent,
    required this.expanded,
    required this.isLoading,
    required this.onPressed,
  });

  final String label;
  final IconData icon;
  final Color accent;
  final bool expanded;
  final bool isLoading;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: label,
      child: Container(
        constraints: BoxConstraints(minWidth: expanded ? 160 : 116),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              accent,
              Color.lerp(accent, const Color(0xFF8A5CFF), 0.52)!
            ],
          ),
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: accent.withValues(alpha: 0.34),
              blurRadius: 24,
              offset: const Offset(0, 12),
            ),
          ],
        ),
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            onTap: onPressed,
            borderRadius: BorderRadius.circular(20),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  if (isLoading)
                    const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  else ...[
                    Text(
                      label,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w800,
                        letterSpacing: 0.1,
                      ),
                    ),
                    const SizedBox(width: 10),
                    Icon(icon, color: Colors.white, size: 20),
                  ],
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _GlassChip extends StatelessWidget {
  const _GlassChip({
    required this.icon,
    required this.label,
    required this.accent,
    this.compact = false,
  });

  final IconData icon;
  final String label;
  final Color accent;
  final bool compact;

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
        child: Container(
          padding: EdgeInsets.symmetric(
            horizontal: compact ? 10 : 12,
            vertical: compact ? 8 : 9,
          ),
          decoration: BoxDecoration(
            color: const Color(0xFF071225).withValues(alpha: 0.58),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white.withValues(alpha: 0.2)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: compact ? 15 : 17, color: accent),
              const SizedBox(width: 7),
              Text(
                label,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: compact ? 11 : 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _AmbientGlow extends StatelessWidget {
  const _AmbientGlow({
    required this.animation,
    required this.accent,
    required this.isDark,
  });

  final Animation<double> animation;
  final Color accent;
  final bool isDark;

  @override
  Widget build(BuildContext context) {
    return Positioned.fill(
      child: IgnorePointer(
        child: AnimatedBuilder(
          animation: animation,
          builder: (context, _) {
            final phase = animation.value * math.pi * 2;
            return Stack(
              children: [
                Positioned(
                  left: -90 + (math.sin(phase) * 24),
                  top: 100 + (math.cos(phase) * 32),
                  child: _GlowOrb(
                    size: 250,
                    color: accent.withValues(alpha: isDark ? 0.15 : 0.09),
                  ),
                ),
                Positioned(
                  right: -110 + (math.cos(phase) * 22),
                  bottom: 70 + (math.sin(phase) * 28),
                  child: _GlowOrb(
                    size: 290,
                    color: const Color(0xFF8A5CFF)
                        .withValues(alpha: isDark ? 0.12 : 0.07),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _GlowOrb extends StatelessWidget {
  const _GlowOrb({required this.size, required this.color});

  final double size;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return ImageFiltered(
      imageFilter: ImageFilter.blur(sigmaX: 48, sigmaY: 48),
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(color: color, shape: BoxShape.circle),
      ),
    );
  }
}

class _OnboardingPageData {
  const _OnboardingPageData({
    required this.eyebrow,
    required this.title,
    required this.subtitle,
    required this.imageAsset,
    required this.visualLabel,
    required this.icon,
    required this.accent,
    required this.secondaryAccent,
    required this.highlights,
    required this.floatingIcons,
    required this.floatingLabels,
  });

  final String eyebrow;
  final String title;
  final String subtitle;
  final String imageAsset;
  final String visualLabel;
  final IconData icon;
  final Color accent;
  final Color secondaryAccent;
  final List<String> highlights;
  final List<IconData> floatingIcons;
  final List<String> floatingLabels;
}

const _pages = [
  _OnboardingPageData(
    eyebrow: 'GENERATIVE INTERIORS',
    title: 'Design Your Dream Space with AI',
    subtitle:
        'Transform any room into a personalized masterpiece using artificial intelligence.',
    imageAsset: 'assets/images/onboarding/welcome.png',
    visualLabel: 'AI-designed in seconds',
    icon: Icons.auto_awesome_rounded,
    accent: Color(0xFF397DFF),
    secondaryAccent: Color(0xFF9A6CFF),
    highlights: [
      'Personalized styles',
      'Photorealistic results',
      'One-tap redesign'
    ],
    floatingIcons: [Icons.chair_alt_rounded, Icons.light_rounded],
    floatingLabels: ['Smart furniture', 'Mood lighting'],
  ),
  _OnboardingPageData(
    eyebrow: 'COMPUTER VISION',
    title: 'AI Understands Your Space',
    subtitle:
        'Our AI analyzes room layouts, furniture, lighting, and dimensions automatically.',
    imageAsset: 'assets/images/onboarding/ai-analysis.png',
    visualLabel: 'Live spatial analysis',
    icon: Icons.center_focus_strong_rounded,
    accent: Color(0xFF00B8E6),
    secondaryAccent: Color(0xFF6F64FF),
    highlights: [
      'Object detection',
      'Room segmentation',
      'Layout intelligence'
    ],
    floatingIcons: [Icons.grid_view_rounded, Icons.straighten_rounded],
    floatingLabels: ['Spatial map', 'Auto dimensions'],
  ),
  _OnboardingPageData(
    eyebrow: 'AUGMENTED REALITY',
    title: 'See Designs in Augmented Reality',
    subtitle:
        'Preview furniture and layouts directly in your room before making decisions.',
    imageAsset: 'assets/images/onboarding/ar-visualization.png',
    visualLabel: 'True-to-scale preview',
    icon: Icons.view_in_ar_rounded,
    accent: Color(0xFF1DA7FF),
    secondaryAccent: Color(0xFF28D7C0),
    highlights: [
      'Life-size placement',
      'Real-time preview',
      'Confident decisions'
    ],
    floatingIcons: [Icons.threed_rotation_rounded, Icons.touch_app_rounded],
    floatingLabels: ['Interactive 3D', 'Place & explore'],
  ),
  _OnboardingPageData(
    eyebrow: 'WHOLE-HOME INTELLIGENCE',
    title: 'Your Personal Interior Design Assistant',
    subtitle:
        'Get intelligent recommendations, cost estimates, shopping suggestions, and complete home design solutions.',
    imageAsset: 'assets/images/onboarding/smart-home.png',
    visualLabel: 'One intelligent workspace',
    icon: Icons.hub_rounded,
    accent: Color(0xFF7857FF),
    secondaryAccent: Color(0xFFFFB45C),
    highlights: ['Smart lighting', 'Cost planning', '3D walkthroughs'],
    floatingIcons: [Icons.pets_rounded, Icons.shopping_bag_rounded],
    floatingLabels: ['Pet-friendly', 'Shop the look'],
  ),
];
