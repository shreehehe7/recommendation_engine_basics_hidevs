import pytest
from candidate_gen import CandidateGenerator

@pytest.fixture
def generator():
    return CandidateGenerator()

def test_collaborative_candidates(generator):
    candidates = generator.collaborative_candidates("user1", limit=5)
    assert isinstance(candidates, list)

def test_collaborative_candidates_invalid_user(generator):
    candidates = generator.collaborative_candidates("unknown_user", limit=5)
    assert isinstance(candidates, list)

def test_content_based_candidates(generator):
    candidates = generator.content_based_candidates("user1", limit=5)
    assert isinstance(candidates, list)

def test_content_based_candidates_invalid_user(generator):
    candidates = generator.content_based_candidates("unknown_user", limit=5)
    assert isinstance(candidates, list)

def test_popularity_candidates(generator):
    candidates = generator.popularity_candidates(limit=2)
    assert isinstance(candidates, list)
    assert len(candidates) <= 2

def test_hybrid_candidates(generator):
    candidates = generator.hybrid_candidates("user1", limit=10)
    assert isinstance(candidates, list)
