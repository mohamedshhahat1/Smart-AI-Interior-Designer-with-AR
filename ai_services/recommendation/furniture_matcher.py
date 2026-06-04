from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class FurnitureMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self._catalog_vectors = None
        self._catalog_items = None

    def build_index(self, catalog_items: list[dict]):
        self._catalog_items = catalog_items
        descriptions = [
            f"{item.get('name', '')} {item.get('category', '')} "
            f"{item.get('style', '')} {item.get('material', '')} "
            f"{item.get('color', '')} {' '.join(item.get('tags', []))}"
            for item in catalog_items
        ]
        self._catalog_vectors = self.vectorizer.fit_transform(descriptions)

    def match(
        self,
        query: str,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        top_k: int = 5,
    ) -> list[dict]:
        if self._catalog_vectors is None or self._catalog_items is None:
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self._catalog_vectors)[0]

        scored_items = []
        for idx, score in enumerate(similarities):
            item = self._catalog_items[idx]
            if category and item.get("category") != category:
                continue
            if max_price and item.get("price", 0) > max_price:
                continue
            scored_items.append((score, item))

        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored_items[:top_k]]

    def match_detected_objects(
        self,
        detected_objects: list[dict],
        style: str,
        budget: Optional[float] = None,
    ) -> list[dict]:
        results = []
        budget_per_item = None
        if budget and detected_objects:
            budget_per_item = budget / len(detected_objects)

        for obj in detected_objects:
            label = obj.get("label", "") if isinstance(obj, dict) else str(obj)
            query = f"{style} {label}"
            matches = self.match(
                query=query,
                category=label,
                max_price=budget_per_item,
                top_k=3,
            )
            results.extend(matches)

        return results


furniture_matcher = FurnitureMatcher()
