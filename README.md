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

I ran three distinct, realistic taste profiles plus three adversarial/edge-case profiles designed to try to trick the scoring logic (defined in [`src/main.py`](src/main.py)), and observed the top 5 for each.

### High-Energy Pop, Chill Lofi, Deep Intense Rock

These behaved as expected: for each, the song that matches on both genre and mood shoots to the top, with the rest of the ranking settled by energy/danceability closeness.

```
High-Energy Pop — genre=pop, mood=happy, energy=0.85, danceability=0.85
=======================================================================

1. Sunrise City by Neon Echo — Score: 5.91
     - genre match (+2.0)
     - mood match (+2.0)
     - energy closeness (+0.97)
     - danceability closeness (+0.94)

2. Gym Hero by Max Pulse — Score: 3.89
     - genre match (+2.0)
     - energy closeness (+0.92)
     - danceability closeness (+0.97)

3. Rooftop Lights by Indigo Parade — Score: 3.88
     - mood match (+2.0)
     - energy closeness (+0.91)
     - danceability closeness (+0.97)

4. Concrete Bloom by Kicker Lane — Score: 1.95
     - energy closeness (+0.95)
     - danceability closeness (+1.00)

5. Neon Pulse Rush by Kilowatt — Score: 1.85
     - energy closeness (+0.90)
     - danceability closeness (+0.95)

Chill Lofi — genre=lofi, mood=chill, energy=0.35, danceability=0.55
===================================================================

1. Library Rain by Paper Lanterns — Score: 5.97
     - genre match (+2.0)
     - mood match (+2.0)
     - energy closeness (+1.00)
     - danceability closeness (+0.97)

2. Midnight Coding by LoRoom — Score: 5.86
     - genre match (+2.0)
     - mood match (+2.0)
     - energy closeness (+0.93)
     - danceability closeness (+0.93)

3. Focus Flow by LoRoom — Score: 3.90
     - genre match (+2.0)
     - energy closeness (+0.95)
     - danceability closeness (+0.95)

4. Spacewalk Thoughts by Orbit Bloom — Score: 3.79
     - mood match (+2.0)
     - energy closeness (+0.93)
     - danceability closeness (+0.86)

5. Coffee Shop Stories by Slow Stereo — Score: 1.97
     - energy closeness (+0.98)
     - danceability closeness (+0.99)

Deep Intense Rock — genre=rock, mood=intense, energy=0.9, danceability=0.6
==========================================================================

1. Storm Runner by Voltline — Score: 5.93
     - genre match (+2.0)
     - mood match (+2.0)
     - energy closeness (+0.99)
     - danceability closeness (+0.94)

2. Gym Hero by Max Pulse — Score: 3.69
     - mood match (+2.0)
     - energy closeness (+0.97)
     - danceability closeness (+0.72)

3. Broken Static by The Riot Act — Score: 1.96
     - energy closeness (+0.98)
     - danceability closeness (+0.98)

4. Molten Sky by Ironclad Vow — Score: 1.88
     - energy closeness (+0.93)
     - danceability closeness (+0.95)

5. Sunrise City by Neon Echo — Score: 1.73
     - energy closeness (+0.92)
     - danceability closeness (+0.81)
```

### Adversarial / edge-case profiles

These profiles were designed to try to break or expose weaknesses in the scoring logic: a mood that contradicts the requested energy, a genre that doesn't exist in the catalog at all, and a genre/mood/energy combination that doesn't naturally co-occur.

```
Conflicting Mood-Energy — genre=pop, mood=sad, energy=0.9, danceability=0.6
===========================================================================

1. Sunrise City by Neon Echo — Score: 3.73
     - genre match (+2.0)
     - energy closeness (+0.92)
     - danceability closeness (+0.81)

2. Gym Hero by Max Pulse — Score: 3.69
     - genre match (+2.0)
     - energy closeness (+0.97)
     - danceability closeness (+0.72)

3. Broken Static by The Riot Act — Score: 1.96
     - energy closeness (+0.98)
     - danceability closeness (+0.98)

4. Storm Runner by Voltline — Score: 1.93
     - energy closeness (+0.99)
     - danceability closeness (+0.94)

5. Molten Sky by Ironclad Vow — Score: 1.88
     - energy closeness (+0.93)
     - danceability closeness (+0.95)

Nonexistent Genre — genre=k-pop, mood=happy, energy=0.7, danceability=0.75
==========================================================================

1. Rooftop Lights by Indigo Parade — Score: 3.87
     - mood match (+2.0)
     - energy closeness (+0.94)
     - danceability closeness (+0.93)

2. Sunrise City by Neon Echo — Score: 3.84
     - mood match (+2.0)
     - energy closeness (+0.88)
     - danceability closeness (+0.96)

3. Night Drive Loop by Neon Echo — Score: 1.93
     - energy closeness (+0.95)
     - danceability closeness (+0.98)

4. Slow Burn Velvet by Nadia Cross — Score: 1.80
     - energy closeness (+0.85)
     - danceability closeness (+0.95)

5. Concrete Bloom by Kicker Lane — Score: 1.80
     - energy closeness (+0.90)
     - danceability closeness (+0.90)

Contradictory Vibe — genre=classical, mood=angry, energy=0.95, danceability=0.9
===============================================================================

1. Molten Sky by Ironclad Vow — Score: 3.63
     - mood match (+2.0)
     - energy closeness (+0.98)
     - danceability closeness (+0.65)

2. Still Water Suite by Marion Vale — Score: 2.62
     - genre match (+2.0)
     - energy closeness (+0.27)
     - danceability closeness (+0.35)

3. Neon Pulse Rush by Kilowatt — Score: 2.00
     - energy closeness (+1.00)
     - danceability closeness (+1.00)

4. Gym Hero by Max Pulse — Score: 1.96
     - energy closeness (+0.98)
     - danceability closeness (+0.98)

5. Concrete Bloom by Kicker Lane — Score: 1.80
     - energy closeness (+0.85)
     - danceability closeness (+0.95)
```

**Observations:**

- **No crash on unknown values.** `mood="sad"` and `genre="k-pop"` don't exist anywhere in the catalog, but the system doesn't error — it just never awards that +2.0 bonus and falls back to whatever other signals are available. That's a robustness win, but it also means the system can't tell the difference between "no preference" and "preference nobody makes."
- **Genre match can drag in a bad overall fit.** In "Contradictory Vibe," *Still Water Suite* (a peaceful, low-energy classical piece: `energy=0.22`, `danceability=0.25`) still lands at #2 out of 20 songs purely because it matches `genre=classical`, despite being close to the opposite of the requested angry/high-energy/danceable vibe. This confirms the genre/mood-overweighting bias called out below — the +2.0 categorical bonus can outweigh a genuinely poor numeric fit.
- **A contradictory mood can accidentally get "fixed" by genre.** In "Conflicting Mood-Energy," the nonexistent `mood="sad"` never matches, so the ranking is effectively decided by `genre="pop"` + energy/danceability closeness — the system silently drops the mood signal instead of flagging that the request was contradictory or unsatisfiable.

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
