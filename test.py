
from similarity import SimilarityCalculator
from sample_data import user_vectors
from sample_data import item_tags
from sample_data import user_ratings


similarity = SimilarityCalculator()


print("\n===== COSINE SIMILARITY =====")

cosine = similarity.cosine_similarity(
    user_vectors["user1"],
    user_vectors["user2"]
)

print("User1 vs User2:", cosine)


print("\n===== JACCARD SIMILARITY =====")

jaccard = similarity.jaccard_similarity(
    item_tags["movie1"],
    item_tags["movie2"]
)

print("Movie1 vs Movie2:", jaccard)


print("\n===== PEARSON CORRELATION =====")

pearson = similarity.pearson_correlation(
    user_ratings["user1"],
    user_ratings["user2"]
)

print("User1 vs User2:", pearson)


print("\n===== EDGE CASES =====")

print(
    "Empty sets:",
    similarity.jaccard_similarity(set(), set())
)

print(
    "Zero vectors:",
    similarity.cosine_similarity(
        [0,0,0],
        [0,0,0]
    )
)

print(
    "No common ratings:",
    similarity.pearson_correlation(
        {"a":1},
        {"b":5}
    )
)

from candidate_gen import CandidateGenerator

generator = CandidateGenerator()

print("\n===== COLLABORATIVE =====")

print(
    generator.collaborative_candidates(
        "user1"
    )
)

print("\n===== CONTENT BASED =====")

print(
    generator.content_based_candidates(
        "user1"
    )
)

print("\n===== POPULARITY =====")

print(
    generator.popularity_candidates()
)

print("\n===== HYBRID =====")

print(
    generator.hybrid_candidates(
        "user1"
    )
)

print("\n===== COLD START =====")

print(
    generator.hybrid_candidates(
        "new_user"
    )
)

from scorer import RecommendationScorer
from sample_data import (
    item_popularity,
    item_recency,
    item_relevance
)

def relevance_score(item):

    return item_relevance.get(
        item,
        0
    )


def recency_score(item):

    return item_recency.get(
        item,
        0
    )


def popularity_score(item):

    maximum = max(
        item_popularity.values()
    )

    return (
        item_popularity.get(item, 0)
        / maximum
    )

scorer = RecommendationScorer()

scorer.add_scorer(
    "relevance",
    relevance_score,
    0.5
)

scorer.add_scorer(
    "recency",
    recency_score,
    0.2
)

scorer.add_scorer(
    "popularity",
    popularity_score,
    0.3
)

print("\n===== RANKING =====")

candidates = generator.hybrid_candidates(
    "user1"
)

results = scorer.rank_candidates(
    "user1",
    candidates
)

for item in results:

    print(
        item["item"],
        item["score"],
        item["explanation"]
    )

from evaluator import RecommendationEvaluator
from sample_data import ground_truth

evaluator = RecommendationEvaluator()

recommendations = {}

for user in ground_truth:

    candidates = (
        generator.hybrid_candidates(
            user
        )
    )

    ranked = scorer.rank_candidates(
        user,
        candidates
    )

    recommendations[user] = [
        item["item"]
        for item in ranked
    ]

recommendations = {}

for user in ground_truth:

    candidates = (
        generator.hybrid_candidates(
            user
        )
    )

    ranked = scorer.rank_candidates(
        user,
        candidates
    )

    recommendations[user] = [
        item["item"]
        for item in ranked
    ]

print("\n===== EVALUATION =====")

metrics = evaluator.evaluate_all(
    recommendations,
    ground_truth,
    3
)

print(metrics)