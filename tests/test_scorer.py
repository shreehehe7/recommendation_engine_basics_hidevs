import pytest
from scorer import RecommendationScorer

@pytest.fixture
def scorer():
    return RecommendationScorer()

def test_add_scorer(scorer):
    scorer.add_scorer("test_score", lambda x: 1.0, 0.5)
    assert "test_score" in scorer.scorers

def test_calculate_score(scorer):
    scorer.add_scorer("test1", lambda x: 0.8, 0.5)
    scorer.add_scorer("test2", lambda x: 0.6, 0.5)
    
    result = scorer.calculate_score("user1", "item1")
    assert result["score"] == 0.7
    assert len(result["explanation"]) == 2

def test_calculate_score_with_exception(scorer):
    def bad_score(item):
        raise ValueError("Database error")
        
    scorer.add_scorer("bad", bad_score, 1.0)
    scorer.add_scorer("good", lambda x: 0.5, 1.0)
    
    result = scorer.calculate_score("user1", "item1")
    assert result["score"] == 0.5

def test_rank_candidates(scorer):
    scorer.add_scorer("test1", lambda item: 0.9 if item == "itemA" else 0.4, 1.0)
    ranked = scorer.rank_candidates("user1", ["itemB", "itemA"])
    
    assert ranked[0]["item"] == "itemA"
    assert ranked[1]["item"] == "itemB"
