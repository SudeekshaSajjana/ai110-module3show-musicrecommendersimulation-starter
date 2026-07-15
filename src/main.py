"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def print_recommendations(user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} ({song['artist']})")
        print(f"   Score:   {score:.2f}")
        print(f"   Because: {explanation}")
        print("-" * 40)


# Adversarial / edge-case profiles designed to probe weak spots in score_song:
# out-of-range or non-numeric energy, NaN propagation, case-sensitive string
# matching, empty/unknown preferences, and tie-breaking behavior.
ADVERSARIAL_PROFILES = [
    ("Out-of-range energy (5.0)", {"genre": "pop", "mood": "happy", "energy": 5.0}),
    ("Negative energy (-2.0)", {"genre": "rock", "mood": "intense", "energy": -2.0}),
    ("NaN energy", {"genre": "lofi", "mood": "chill", "energy": float("nan")}),
    ("String energy (\"0.8\")", {"genre": "pop", "mood": "happy", "energy": "0.8"}),
    ("Case mismatch (Pop/Happy)", {"genre": "Pop", "mood": "Happy", "energy": 0.8}),
    ("Empty profile", {}),
    ("Nonexistent genre/mood", {"genre": "opera", "mood": "furious", "energy": 0.5}),
    (
        "Extra irrelevant keys",
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "artist": "Neon Echo",
            "min_danceability": 0.9,
        },
    ),
]


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print("\nTop Recommendations")
    print("=" * 40)
    print_recommendations(user_prefs, songs, k=5)

    print("\nAdversarial / Edge Case Profiles")
    print("=" * 40)
    for name, prefs in ADVERSARIAL_PROFILES:
        print(f"\n[{name}] prefs={prefs}")
        print("-" * 40)
        try:
            print_recommendations(prefs, songs, k=3)
        except Exception as exc:
            print(f"   ERROR: {type(exc).__name__}: {exc}")
            print("-" * 40)


if __name__ == "__main__":
    main()
