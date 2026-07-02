import pytest
from similarity import SimilarityCalculator

@pytest.fixture
def calc():
    return SimilarityCalculator()

def test_cosine_similarity(calc):
    vec1 = [1, 2, 3]
    vec2 = [1, 2, 3]
    assert calc.cosine_similarity(vec1, vec2) == 1.0

    vec3 = [1, 0, 0]
    vec4 = [0, 1, 0]
    assert calc.cosine_similarity(vec3, vec4) == 0.0

def test_cosine_similarity_zero_magnitude(calc):
    assert calc.cosine_similarity([0, 0], [1, 1]) == 0.0

def test_cosine_similarity_errors(calc):
    with pytest.raises(ValueError):
        calc.cosine_similarity([1, 2], [1, 2, 3])
    
    with pytest.raises(TypeError):
        calc.cosine_similarity(["a", "b"], ["c", "d"])

def test_jaccard_similarity(calc):
    set1 = {"a", "b"}
    set2 = {"b", "c"}
    assert calc.jaccard_similarity(set1, set2) == 0.3333
    
    assert calc.jaccard_similarity(set(), set()) == 0.0

def test_jaccard_similarity_type_conversion(calc):
    assert calc.jaccard_similarity(["a", "b"], ["b", "c"]) == 0.3333

def test_pearson_correlation(calc):
    r1 = {"item1": 4, "item2": 5, "item3": 2}
    r2 = {"item1": 5, "item2": 4, "item3": 3}
    assert calc.pearson_correlation(r1, r2) != 0.0
    
    assert calc.pearson_correlation({"a": 1}, {"b": 2}) == 0.0

def test_pearson_correlation_errors(calc):
    with pytest.raises(TypeError):
        calc.pearson_correlation({"a": "bad"}, {"a": "value"})
