import math
from typing import List, Dict, Any

class RecommendationEvaluator:
    """
    A class to evaluate the quality of recommendations against ground truth data.
    """

    def precision_at_k(self, recommendations: List[str], relevant_items: List[str], k: int) -> float:
        """
        Calculate Precision at K.

        Args:
            recommendations (List[str]): The list of recommended items.
            relevant_items (List[str]): The ground truth list of relevant items.
            k (int): The number of top recommendations to consider.

        Returns:
            float: Precision@k score rounded to 4 decimal places.
        """
        try:
            recommendations = recommendations[:k]
            if len(recommendations) == 0:
                return 0.0

            relevant = sum(1 for item in recommendations if item in relevant_items)
            return round(relevant / len(recommendations), 4)
        except Exception:
            return 0.0

    def recall_at_k(self, recommendations: List[str], relevant_items: List[str], k: int) -> float:
        """
        Calculate Recall at K.

        Args:
            recommendations (List[str]): The list of recommended items.
            relevant_items (List[str]): The ground truth list of relevant items.
            k (int): The number of top recommendations to consider.

        Returns:
            float: Recall@k score rounded to 4 decimal places.
        """
        try:
            recommendations = recommendations[:k]
            if len(relevant_items) == 0:
                return 0.0

            relevant = sum(1 for item in recommendations if item in relevant_items)
            return round(relevant / len(relevant_items), 4)
        except Exception:
            return 0.0

    def ndcg_at_k(self, recommendations: List[str], relevant_items: List[str], k: int) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG) at K.

        Args:
            recommendations (List[str]): The list of recommended items.
            relevant_items (List[str]): The ground truth list of relevant items.
            k (int): The number of top recommendations to consider.

        Returns:
            float: NDCG@k score rounded to 4 decimal places.
        """
        try:
            recommendations = recommendations[:k]
            dcg = 0.0

            for i, item in enumerate(recommendations):
                if item in relevant_items:
                    dcg += 1.0 / math.log2(i + 2)

            ideal_dcg = 0.0
            for i in range(min(k, len(relevant_items))):
                ideal_dcg += 1.0 / math.log2(i + 2)

            if ideal_dcg == 0:
                return 0.0

            return round(dcg / ideal_dcg, 4)
        except Exception:
            return 0.0

    def evaluate_all(self, recommendations_dict: Dict[str, List[str]], ground_truth_dict: Dict[str, List[str]], k: int) -> Dict[str, float]:
        """
        Evaluate Precision, Recall, and NDCG at K for all users in the dataset.

        Args:
            recommendations_dict (Dict[str, List[str]]): A dictionary mapping user_id to a list of recommended items.
            ground_truth_dict (Dict[str, List[str]]): A dictionary mapping user_id to a list of relevant items.
            k (int): The number of top recommendations to consider.

        Returns:
            Dict[str, float]: A dictionary containing the average precision, recall, and ndcg across all valid users.
        """
        precision_scores: List[float] = []
        recall_scores: List[float] = []
        ndcg_scores: List[float] = []

        for user in recommendations_dict:
            if user not in ground_truth_dict:
                continue

            recommendations = recommendations_dict[user]
            truth = ground_truth_dict[user]

            precision_scores.append(self.precision_at_k(recommendations, truth, k))
            recall_scores.append(self.recall_at_k(recommendations, truth, k))
            ndcg_scores.append(self.ndcg_at_k(recommendations, truth, k))

        try:
            if len(precision_scores) == 0:
                return {"precision@k": 0.0, "recall@k": 0.0, "ndcg@k": 0.0}

            return {
                "precision@k": round(sum(precision_scores) / len(precision_scores), 4),
                "recall@k": round(sum(recall_scores) / len(recall_scores), 4),
                "ndcg@k": round(sum(ndcg_scores) / len(ndcg_scores), 4)
            }
        except ZeroDivisionError:
            return {"precision@k": 0.0, "recall@k": 0.0, "ndcg@k": 0.0}