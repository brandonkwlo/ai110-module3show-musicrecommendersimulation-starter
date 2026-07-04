"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Three distinct, realistic taste profiles.
USER_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85, "danceability": 0.85},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "danceability": 0.55},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "danceability": 0.6},
}

# Edge case profiles designed to probe or "trick" the scoring logic.
ADVERSARIAL_PROFILES = {
    # Mood ("sad") doesn't exist anywhere in the catalog, and it directly
    # contradicts the requested high energy.
    "Conflicting Mood-Energy": {"genre": "pop", "mood": "sad", "energy": 0.9, "danceability": 0.6},
    # Genre isn't present in the catalog at all -- can the system still
    # fall back gracefully on mood + numeric closeness?
    "Nonexistent Genre": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "danceability": 0.75},
    # Pairs a mellow/acoustic genre with an aggressive mood and high
    # energy/danceability that don't naturally co-occur -- probes whether
    # the +2 genre weight drags a mismatched-vibe song to the top.
    "Contradictory Vibe": {"genre": "classical", "mood": "angry", "energy": 0.95, "danceability": 0.9},
}


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    prefs_summary = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    header = f"{name} — {prefs_summary}"
    print(f"\n{header}")
    print("=" * len(header))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']} — Score: {score:.2f}")
        for reason in explanation.split(", "):
            print(f"     - {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in {**USER_PROFILES, **ADVERSARIAL_PROFILES}.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
