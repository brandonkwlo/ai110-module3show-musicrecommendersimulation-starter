"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    "pop_party": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "rock_workout": {"genre": "rock", "mood": "intense", "energy": 0.92},
    "lofi_focus": {"genre": "lofi", "mood": "focused", "energy": 0.40},
    "ambient_unwind": {"genre": "ambient", "mood": "chill", "energy": 0.28},
    "synthwave_night": {"genre": "synthwave", "mood": "moody", "energy": 0.75},
}

def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Loaded {len(songs)} songs from the dataset.")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = explanation.split("; ")
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   :")
        for reason in reasons:
            print(f"               • {reason}")
        print()


if __name__ == "__main__":
    main()
