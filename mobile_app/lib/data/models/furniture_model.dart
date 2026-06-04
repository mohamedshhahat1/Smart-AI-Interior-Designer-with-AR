class FurnitureModel {
  final String id;
  final String name;
  final String category;
  final String? style;
  final double price;
  final String currency;
  final String? imageUrl;
  final String? model3dUrl;
  final double? rating;

  FurnitureModel({
    required this.id,
    required this.name,
    required this.category,
    this.style,
    required this.price,
    this.currency = 'USD',
    this.imageUrl,
    this.model3dUrl,
    this.rating,
  });

  factory FurnitureModel.fromJson(Map<String, dynamic> json) {
    return FurnitureModel(
      id: json['id'] as String,
      name: json['name'] as String,
      category: json['category'] as String,
      style: json['style'] as String?,
      price: (json['price'] as num).toDouble(),
      currency: json['currency'] as String? ?? 'USD',
      imageUrl: json['image_url'] as String?,
      model3dUrl: json['model_3d_url'] as String?,
      rating: (json['rating'] as num?)?.toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'category': category,
      'style': style,
      'price': price,
      'currency': currency,
      'image_url': imageUrl,
      'model_3d_url': model3dUrl,
      'rating': rating,
    };
  }
}
