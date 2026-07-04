# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

**Song features:** `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness` (plus `title`/`artist` for display).

**UserProfile fields:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

### Algorithm Recipe

Each song is scored against the user's profile with this formula:

```
score = 2 * (genre == favorite_genre)
      + 2 * (mood == favorite_mood)
      + (1 - abs(energy - target_energy))
      + (acousticness if likes_acoustic else 1 - acousticness)
```

- **Genre match (+2)** and **mood match (+2)** carry the heaviest weight because they're categorical, easy to reason about, and the strongest signal of taste in this dataset.
- **Energy closeness (0 to 1)** rewards songs whose energy is near the user's `target_energy`, scaled so a perfect match adds 1 point and a maximally-off match adds 0.
- **Acousticness (0 to 1)** rewards acoustic songs for users who `like_acoustic`, and rewards non-acoustic songs otherwise.

To recommend, every song in the catalog is scored this way and the top `k` by score are returned.

### Potential Biases

- **Genre/mood over-weighting:** because genre and mood matches are worth 2 points each versus a max of 1 point for energy and acousticness combined, a song that's a poor mood/energy fit but shares the favorite genre can outrank a song that's a much better overall vibe match. The system may over-prioritize genre and mood, ignoring great songs that match the user's mood on other dimensions (tempo, valence, danceability) but sit in a different genre bucket.
- **Cold-start / narrow-taste bias:** users whose favorite genre or mood is rare (or absent) in the catalog will get recommendations driven almost entirely by the energy/acousticness tiebreakers, which may feel arbitrary.
- **Unused signals:** `tempo_bpm`, `valence`, and `danceability` aren't part of the score at all, so two songs that differ a lot on those axes can tie if they match on genre, mood, energy, and acousticness.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the starter profile (`genre=pop, mood=happy, energy=0.8, danceability=0.7`):

```
Loaded songs: 20

Top Recommendations for genre=pop, mood=happy, energy=0.8, danceability=0.7
===========================================================================

1. Sunrise City by Neon Echo — Score: 5.89
     - genre match (+2.0)
     - mood match (+2.0)
     - energy closeness (+0.98)
     - danceability closeness (+0.91)

2. Rooftop Lights by Indigo Parade — Score: 3.84
     - mood match (+2.0)
     - energy closeness (+0.96)
     - danceability closeness (+0.88)

3. Gym Hero by Max Pulse — Score: 3.69
     - genre match (+2.0)
     - energy closeness (+0.87)
     - danceability closeness (+0.82)

4. Night Drive Loop by Neon Echo — Score: 1.92
     - energy closeness (+0.95)
     - danceability closeness (+0.97)

5. Storm Runner by Voltline — Score: 1.85
     - energy closeness (+0.89)
     - danceability closeness (+0.96)
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
