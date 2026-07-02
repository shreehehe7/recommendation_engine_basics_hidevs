import math
from typing import List, Set, Dict, Any

class SimilarityCalculator:
    """
    A class to calculate various similarity and correlation metrics between items or users.
    """

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate the Cosine Similarity between two vectors.

        Args:
            vec1 (List[float]): The first vector.
            vec2 (List[float]): The second vector.

        Returns:
            float: The cosine similarity score, rounded to 4 decimal places. Returns 0.0 if either vector has a magnitude of 0.

        Raises:
            ValueError: If the vectors do not have the same length.
            TypeError: If the vectors contain non-numeric types.
        """
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have same length")

        try:
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude1 = math.sqrt(sum(a * a for a in vec1))
            magnitude2 = math.sqrt(sum(b * b for b in vec2))
        except TypeError as e:
            raise TypeError(f"Vectors must contain numeric values: {e}")

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        similarity = dot_product / (magnitude1 * magnitude2)
        return round(similarity, 4)

    def jaccard_similarity(self, set1: Set[Any], set2: Set[Any]) -> float:
        """
        Calculate the Jaccard Similarity between two sets.

        Args:
            set1 (Set[Any]): The first set.
            set2 (Set[Any]): The second set.

        Returns:
            float: The jaccard similarity score, rounded to 4 decimal places. Returns 0.0 if both sets are empty.
        """
        if not isinstance(set1, set) or not isinstance(set2, set):
            try:
                set1 = set(set1)
                set2 = set(set2)
            except Exception:
                raise TypeError("Inputs must be sets or convertible to sets.")

        if not set1 and not set2:
            return 0.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        if union == 0:
            return 0.0
            
        similarity = intersection / union
        return round(similarity, 4)

    def pearson_correlation(self, ratings1: Dict[Any, float], ratings2: Dict[Any, float]) -> float:
        """
        Calculate the Pearson Correlation Coefficient between two sets of ratings.

        Args:
            ratings1 (Dict[Any, float]): The first dictionary of ratings.
            ratings2 (Dict[Any, float]): The second dictionary of ratings.

        Returns:
            float: The pearson correlation score, rounded to 4 decimal places. Returns 0.0 if there are no common items or if variance is zero.
        """
        if not isinstance(ratings1, dict) or not isinstance(ratings2, dict):
             raise TypeError("Inputs must be dictionaries.")

        common_items = set(ratings1.keys()).intersection(set(ratings2.keys()))
        
        if len(common_items) == 0:
            return 0.0

        try:
            values1 = [float(ratings1[item]) for item in common_items]
            values2 = [float(ratings2[item]) for item in common_items]
        except (TypeError, ValueError) as e:
            raise TypeError(f"Ratings must contain numeric values: {e}")

        mean1 = sum(values1) / len(values1)
        mean2 = sum(values2) / len(values2)

        numerator = sum((a - mean1) * (b - mean2) for a, b in zip(values1, values2))

        denominator1 = math.sqrt(sum((a - mean1) ** 2 for a in values1))
        denominator2 = math.sqrt(sum((b - mean2) ** 2 for b in values2))

        denominator = denominator1 * denominator2

        if denominator == 0:
            return 0.0

        correlation = numerator / denominator
        return round(correlation, 4)