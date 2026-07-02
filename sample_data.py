# User -> Item ratings (1-5 scale)
user_ratings = {
    "user1": {
        "movie1": 5,
        "movie2": 4,
        "movie3": 2
    },

    "user2": {
        "movie1": 4,
        "movie2": 5,
        "movie4": 4
    },

    "user3": {
        "movie2": 3,
        "movie3": 5,
        "movie5": 4
    },

    "user4": {
        "movie1": 2,
        "movie4": 5,
        "movie5": 5
    }
}


# Item features/tags
item_tags = {
    "movie1": {"action", "adventure"},
    "movie2": {"action", "thriller"},
    "movie3": {"drama", "romance"},
    "movie4": {"action", "sci-fi"},
    "movie5": {"drama", "mystery"}
}


# Item popularity counts
item_popularity = {
    "movie1": 120,
    "movie2": 95,
    "movie3": 70,
    "movie4": 110,
    "movie5": 60
}


# Vector representations
user_vectors = {
    "user1": [5,4,2,0,0],
    "user2": [4,5,0,4,0],
    "user3": [0,3,5,0,4],
    "user4": [2,0,0,5,5]
}

# User watch history
user_history = {
    "user1": ["movie1", "movie2", "movie3"],
    "user2": ["movie1", "movie2", "movie4"],
    "user3": ["movie2", "movie3", "movie5"],
    "user4": ["movie1", "movie4", "movie5"]
}


# Complete item catalog
all_items = [
    "movie1",
    "movie2",
    "movie3",
    "movie4",
    "movie5"
]

# Recency scores (higher = newer)
item_recency = {
    "movie1": 0.4,
    "movie2": 0.7,
    "movie3": 0.3,
    "movie4": 0.9,
    "movie5": 0.8
}

# mock Relevance scores
item_relevance = {
    "movie1": 0.85,
    "movie2": 0.75,
    "movie3": 0.55,
    "movie4": 0.95,
    "movie5": 0.70
}

# Ground truth data
# represent items the user actually liked later

ground_truth = {
    "user1": ["movie4", "movie5"],
    "user2": ["movie3", "movie5"],
    "user3": ["movie1", "movie4"],
    "user4": ["movie2", "movie3"]
}