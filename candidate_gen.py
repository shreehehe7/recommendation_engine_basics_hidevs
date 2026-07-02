from typing import List, Set, Dict, Any
from similarity import SimilarityCalculator
from sample_data import (
    user_vectors,
    user_history,
    item_tags,
    item_popularity,
    all_items
)

class CandidateGenerator:
    """
    A class to generate recommendation candidates using various strategies.
    """

    def __init__(self) -> None:
        self.similarity = SimilarityCalculator()

    def collaborative_candidates(self, user_id: str, limit: int = 20) -> List[str]:
        """
        Generate candidates based on user similarity (Collaborative Filtering).

        Args:
            user_id (str): The target user ID.
            limit (int): The maximum number of candidates to return.

        Returns:
            List[str]: A list of candidate item IDs.
        """
        try:
            if user_id not in user_history or user_id not in user_vectors:
                return self.popularity_candidates(limit=limit)

            similarities: Dict[str, float] = {}
            target_vector = user_vectors[user_id]

            for user in user_vectors:
                if user == user_id:
                    continue

                score = self.similarity.cosine_similarity(
                    target_vector,
                    user_vectors[user]
                )
                similarities[user] = score

            similar_users = sorted(
                similarities,
                key=similarities.get,  # type: ignore
                reverse=True
            )

            candidates: Set[str] = set()
            for user in similar_users:
                if user not in user_history:
                    continue
                for item in user_history[user]:
                    if item not in user_history.get(user_id, []):
                        candidates.add(item)
                        
            return list(candidates)[:limit]
        except Exception as e:
            # Fallback in case of unexpected errors
            print(f"Error in collaborative_candidates: {e}")
            return self.popularity_candidates(limit=limit)

    def content_based_candidates(self, user_id: str, limit: int = 20) -> List[str]:
        """
        Generate candidates based on item similarity (Content-Based Filtering).

        Args:
            user_id (str): The target user ID.
            limit (int): The maximum number of candidates to return.

        Returns:
            List[str]: A list of candidate item IDs.
        """
        try:
            if user_id not in user_history:
                return self.popularity_candidates(limit=limit)

            user_items = user_history[user_id]
            candidates: Set[str] = set()

            for watched_item in user_items:
                if watched_item not in item_tags:
                    continue
                watched_tags = item_tags[watched_item]

                for item in all_items:
                    if item in user_items or item not in item_tags:
                        continue

                    similarity = self.similarity.jaccard_similarity(
                        watched_tags,
                        item_tags[item]
                    )

                    if similarity > 0:
                        candidates.add(item)

            return list(candidates)[:limit]
        except Exception as e:
            print(f"Error in content_based_candidates: {e}")
            return self.popularity_candidates(limit=limit)

    def popularity_candidates(self, limit: int = 20) -> List[str]:
        """
        Generate candidates based on overall item popularity.

        Args:
            limit (int): The maximum number of candidates to return.

        Returns:
            List[str]: A list of candidate item IDs.
        """
        try:
            popular = sorted(
                item_popularity,
                key=item_popularity.get,  # type: ignore
                reverse=True
            )
            return popular[:limit]
        except Exception as e:
            print(f"Error in popularity_candidates: {e}")
            return []

    def hybrid_candidates(self, user_id: str, limit: int = 20) -> List[str]:
        """
        Generate candidates using a hybrid of collaborative, content-based, and popularity methods.

        Args:
            user_id (str): The target user ID.
            limit (int): The maximum number of candidates to return.

        Returns:
            List[str]: A list of candidate item IDs.
        """
        try:
            collaborative = self.collaborative_candidates(user_id, limit=limit)
            content = self.content_based_candidates(user_id, limit=limit)
            popular = self.popularity_candidates(limit=limit)

            combined = collaborative + content + popular
            unique: List[str] = []

            for item in combined:
                if item not in unique:
                    unique.append(item)

            return unique[:limit]
        except Exception as e:
            print(f"Error in hybrid_candidates: {e}")
            return self.popularity_candidates(limit=limit)