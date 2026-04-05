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
    "pop_party": {"genre": "pop", "mood": "happy", "energy": 0.85, "likes_acoustic": False},
    "rock_workout": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    "lofi_focus": {"genre": "lofi", "mood": "focused", "energy": 0.40, "likes_acoustic": True},
    "ambient_unwind": {"genre": "ambient", "mood": "chill", "energy": 0.28, "likes_acoustic": True},
    "synthwave_night": {"genre": "synthwave", "mood": "moody", "energy": 0.75, "likes_acoustic": False},
    "genre_ghost": {"genre": "jazz", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "acoustic_trap": {"genre": "rock", "mood": "intense", "energy": 0.95, "likes_acoustic": True},
    "flatline": {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False},
    "misspelled_mood": {"genre": "lofi", "mood": "Focus", "energy": 0.4, "likes_acoustic": True},
    "extremist": {"genre": "electronic", "mood": "euphoric", "energy": 1.0, "likes_acoustic": False},
    "ghost_profile": {"genre": "jazz", "mood": "nostalgic", "energy": 0.5, "likes_acoustic": True},
}

def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from the dataset.\n")

    for name, prefs in PROFILES.items():
        prefs_str = ", ".join(f"{k}={v}" for k, v in prefs.items())
        print(f"\n[{name}]  {prefs_str}")

        recommendations = recommend_songs(prefs, songs, k=5)

        for rank, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print(f"  #{rank}  {song['title']} ({score:.2f})  —  {explanation}")


if __name__ == "__main__":
    main()
