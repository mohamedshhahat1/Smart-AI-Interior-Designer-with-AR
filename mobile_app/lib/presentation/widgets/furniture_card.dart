import 'package:flutter/material.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/data/models/furniture_model.dart';

class FurnitureCard extends StatelessWidget {
  final FurnitureModel furniture;
  final VoidCallback? onTap;
  final VoidCallback? onAddToAR;

  const FurnitureCard({
    super.key,
    required this.furniture,
    this.onTap,
    this.onAddToAR,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: 120,
              width: double.infinity,
              color: Colors.grey[200],
              child: furniture.imageUrl != null
                  ? Image.network(furniture.imageUrl!, fit: BoxFit.cover)
                  : Icon(Icons.chair, size: 48, color: Colors.grey[400]),
            ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    furniture.name,
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    furniture.category,
                    style: TextStyle(color: Colors.grey[600], fontSize: 12),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        '\$${furniture.price.toStringAsFixed(0)}',
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                          color: AppTheme.primaryColor,
                        ),
                      ),
                      if (furniture.rating != null)
                        Row(
                          children: [
                            const Icon(Icons.star, size: 14, color: AppTheme.warningColor),
                            const SizedBox(width: 2),
                            Text(
                              furniture.rating!.toStringAsFixed(1),
                              style: const TextStyle(fontSize: 12),
                            ),
                          ],
                        ),
                    ],
                  ),
                  if (onAddToAR != null) ...[
                    const SizedBox(height: 8),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        onPressed: onAddToAR,
                        icon: const Icon(Icons.view_in_ar, size: 16),
                        label: const Text('View in AR', style: TextStyle(fontSize: 12)),
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 6),
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
