from typing import Callable, Dict, Any, List, Optional
from sample_data import (
    item_popularity,
    item_recency,
    item_relevance
)

class RecommendationScorer:
    """
    A class to score and rank recommendation candidates based on weighted factors.
    """

    def __init__(self) -> None:
        # Dictionary storing scorer functions and their weights
        self.scorers: Dict[str, Dict[str, Any]] = {}

    def add_scorer(self, name: str, function: Callable[[str], float], weight: float) -> None:
        """
        Add a scoring function to the scorer.

        Args:
            name (str): The name of the scoring factor (e.g., 'relevance').
            function (Callable[[str], float]): A function that takes an item ID and returns a score.
            weight (float): The weight of this score in the final calculation.
        """
        self.scorers[name] = {
            "function": function,
            "weight": weight
        }

    def calculate_score(self, user_id: str, item_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculate the overall score for a given candidate item.

        Args:
            user_id (str): The user for whom the item is being scored.
            item_id (str): The item being scored.
            context (Optional[Dict[str, Any]]): Optional context for scoring.

        Returns:
            Dict[str, Any]: A dictionary containing the final score and a list of explanations.
        """
        total_score: float = 0.0
        total_weight: float = 0.0
        explanation: List[str] = []

        for name, scorer in self.scorers.items():
            try:
                score = scorer["function"](item_id)
            except Exception as e:
                # Handle potential errors inside custom scoring functions
                score = 0.0
                explanation.append(f"{name}:error({e})")
                continue

            weight = scorer["weight"]
            total_score += score * weight
            total_weight += weight
            explanation.append(f"{name}:{round(score, 2)}")

        if total_weight == 0:
            final_score = 0.0
        else:
            final_score = total_score / total_weight

        return {
            "score": round(final_score, 4),
            "explanation": explanation
        }

    def rank_candidates(self, user_id: str, candidates: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Rank a list of candidate items based on the configured scorers.

        Args:
            user_id (str): The target user ID.
            candidates (List[str]): A list of candidate item IDs.
            limit (int): The maximum number of ranked items to return.

        Returns:
            List[Dict[str, Any]]: A ranked list of dictionaries containing item, score, and explanation.
        """
        ranked: List[Dict[str, Any]] = []

        for item in candidates:
            result = self.calculate_score(user_id, item)

            ranked.append({
                "item": item,
                "score": result["score"],
                "explanation": result["explanation"]
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked[:limit]