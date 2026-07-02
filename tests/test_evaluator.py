import pytest
from evaluator import RecommendationEvaluator

@pytest.fixture
def evaluator():
    return RecommendationEvaluator()

def test_precision_at_k(evaluator):
    recs = ["item1", "item2", "item3"]
    truth = ["item2", "item4"]
    assert evaluator.precision_at_k(recs, truth, 3) == 0.3333
    
    assert evaluator.precision_at_k([], truth, 3) == 0.0

def test_recall_at_k(evaluator):
    recs = ["item1", "item2", "item3"]
    truth = ["item2", "item4"]
    assert evaluator.recall_at_k(recs, truth, 3) == 0.5
    
    assert evaluator.recall_at_k(recs, [], 3) == 0.0

def test_ndcg_at_k(evaluator):
    recs = ["item1", "item2"]
    truth = ["item1"]
    assert evaluator.ndcg_at_k(recs, truth, 2) == 1.0

def test_evaluate_all(evaluator):
    recs_dict = {"user1": ["item1", "item2"]}
    truth_dict = {"user1": ["item1"]}
    
    result = evaluator.evaluate_all(recs_dict, truth_dict, 2)
    assert result["precision@k"] == 0.5
    assert result["recall@k"] == 1.0
    assert result["ndcg@k"] == 1.0

def test_evaluate_all_empty(evaluator):
    result = evaluator.evaluate_all({}, {}, 2)
    assert result["precision@k"] == 0.0
