from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        scored_songs = sorted(
            self.songs,
            key=lambda song: _score_song_object(user, song),
            reverse=True,
        )
        return scored_songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        score, details = _score_song_object(user, song, return_details=True)
        detail_text = ", ".join(details)
        return f"{detail_text}. Total score: {score:.2f}."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        songs: List[Dict[str, Any]] = []
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_results: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, details = _score_song_dict(user_prefs, song, return_details=True)
        explanation = "; ".join(details)
        scored_results.append((song, score, explanation))

    scored_results.sort(key=lambda item: item[1], reverse=True)
    return scored_results[:k]


def _closeness_score(target: float, actual: float, max_points: float) -> float:
    """Return points scaled by how close actual is to target, up to max_points."""
    distance = abs(target - actual)
    similarity = max(0.0, 1.0 - distance)
    return similarity * max_points


def _song_value(song: Any, key: str) -> Any:
    """Read a field from a song whether it is a dict or a dataclass instance."""
    if isinstance(song, dict):
        return song[key]
    return getattr(song, key)


def _score_song_core(
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    likes_acoustic: bool,
    song: Any,
    return_details: bool = False,
) -> Tuple[float, List[str]]:
    """Compute a numeric score and reason list for a song against raw preference values."""
    details: List[str] = []
    score = 0.0

    genre = _song_value(song, "genre")
    mood = _song_value(song, "mood")
    energy = float(_song_value(song, "energy"))
    acousticness = float(_song_value(song, "acousticness"))

    if genre == favorite_genre:
        score += 3.0
        details.append("genre match (+3.00)")

    if mood == favorite_mood:
        score += 3.0
        details.append("mood match (+3.00)")

    energy_points = _closeness_score(target_energy, energy, 4.0)
    score += energy_points
    details.append(f"energy closeness (+{energy_points:.2f})")

    if likes_acoustic:
        acoustic_points = acousticness * 1.5
        score += acoustic_points
        details.append(f"acoustic preference (+{acoustic_points:.2f})")
    else:
        electric_points = (1.0 - acousticness) * 1.0
        score += electric_points
        details.append(f"less acoustic boost (+{electric_points:.2f})")

    return score, details if return_details else []


def _score_song_object(
    user: UserProfile,
    song: Song,
    return_details: bool = False,
) -> Any:
    """Score a Song dataclass against a UserProfile."""
    score, details = _score_song_core(
        user.favorite_genre,
        user.favorite_mood,
        user.target_energy,
        user.likes_acoustic,
        song,
        return_details=True,
    )
    if return_details:
        return score, details
    return score


def _score_song_dict(
    user_prefs: Dict,
    song: Dict,
    return_details: bool = False,
) -> Any:
    """Score a song dict against a user preferences dict."""
    score, details = _score_song_core(
        user_prefs["genre"],
        user_prefs["mood"],
        float(user_prefs["energy"]),
        bool(user_prefs.get("likes_acoustic", False)),
        song,
        return_details=True,
    )
    if return_details:
        return score, details
    return score
