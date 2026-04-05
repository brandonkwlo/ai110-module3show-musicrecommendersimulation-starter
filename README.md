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

My recommender uses content features from each song: energy, valence, danceability, acousticness, plus genre and mood tags. The user profile stores preferred genre, preferred mood, target energy, and whether the user likes acoustic songs. For numeric features, I compute similarity by distance from the user target (closer values get higher scores). I combine feature matches using a weighted score, then rank all songs by score and return the top recommendations. This approach is transparent and easy to explain, but it may miss complex factors like lyrics, context, and diversity.

## Terminal Outputs

### Pop Party

```
[pop_party]  genre=pop, mood=happy, energy=0.85, likes_acoustic=False
  #1  Sunrise City (10.70)  —  genre match (+3.00); mood match (+3.00); energy closeness (+3.88); less acoustic boost (+0.82)
  #2  Gym Hero (7.63)  —  genre match (+3.00); energy closeness (+3.68); less acoustic boost (+0.95)
  #3  Rooftop Lights (7.29)  —  mood match (+3.00); energy closeness (+3.64); less acoustic boost (+0.65)
  #4  Neon Cathedral (4.81)  —  energy closeness (+3.88); less acoustic boost (+0.93)
  #5  Static Hearts (4.78)  —  energy closeness (+3.84); less acoustic boost (+0.94)
```

### Rock Workout

```
[rock_workout] genre=rock, mood=intense, energy=0.92, likes_acoustic=False
#1 Storm Runner (10.86) — genre match (+3.00); mood match (+3.00); energy closeness (+3.96); less acoustic boost (+0.90)
#2 Gym Hero (7.91) — mood match (+3.00); energy closeness (+3.96); less acoustic boost (+0.95)
#3 Granite Sky (4.85) — energy closeness (+3.88); less acoustic boost (+0.97)
#4 Static Hearts (4.82) — energy closeness (+3.88); less acoustic boost (+0.94)
#5 Neon Cathedral (4.77) — energy closeness (+3.84); less acoustic boost (+0.93)
```

### Lofi Focus

```
[lofi_focus] genre=lofi, mood=focused, energy=0.4, likes_acoustic=True
#1 Focus Flow (11.17) — genre match (+3.00); mood match (+3.00); energy closeness (+4.00); acoustic preference (+1.17)
#2 Library Rain (8.09) — genre match (+3.00); energy closeness (+3.80); acoustic preference (+1.29)
#3 Midnight Coding (7.98) — genre match (+3.00); energy closeness (+3.92); acoustic preference (+1.06)
#4 Coffee Shop Stories (5.21) — energy closeness (+3.88); acoustic preference (+1.33)
#5 Pinecone Waltz (5.04) — energy closeness (+3.64); acoustic preference (+1.40)
```

### Ambient Unwind

```
[ambient_unwind] genre=ambient, mood=chill, energy=0.28, likes_acoustic=True
#1 Spacewalk Thoughts (11.38) — genre match (+3.00); mood match (+3.00); energy closeness (+4.00); acoustic preference (+1.38)
#2 Library Rain (8.01) — mood match (+3.00); energy closeness (+3.72); acoustic preference (+1.29)
#3 Midnight Coding (7.51) — mood match (+3.00); energy closeness (+3.44); acoustic preference (+1.06)
#4 Pinecone Waltz (5.28) — energy closeness (+3.88); acoustic preference (+1.40)
#5 Gilded Strings (5.23) — energy closeness (+3.76); acoustic preference (+1.47)
```

### Synthwave Night

```
[synthwave_night] genre=synthwave, mood=moody, energy=0.75, likes_acoustic=False
#1 Night Drive Loop (10.78) — genre match (+3.00); mood match (+3.00); energy closeness (+4.00); less acoustic boost (+0.78)
#2 Midday Parade (4.63) — energy closeness (+3.84); less acoustic boost (+0.79)
#3 Rooftop Lights (4.61) — energy closeness (+3.96); less acoustic boost (+0.65)
#4 Sunrise City (4.54) — energy closeness (+3.72); less acoustic boost (+0.82)
#5 Neon Cathedral (4.41) — energy closeness (+3.48); less acoustic boost (+0.93)
```

### Genre Ghost

```
[genre_ghost] genre=jazz, mood=happy, energy=0.8, likes_acoustic=False
#1 Sunrise City (7.74) — mood match (+3.00); energy closeness (+3.92); less acoustic boost (+0.82)
#2 Rooftop Lights (7.49) — mood match (+3.00); energy closeness (+3.84); less acoustic boost (+0.65)
#3 Coffee Shop Stories (5.39) — genre match (+3.00); energy closeness (+2.28); less acoustic boost (+0.11)
#4 Midday Parade (4.75) — energy closeness (+3.96); less acoustic boost (+0.79)
#5 Neon Cathedral (4.61) — energy closeness (+3.68); less acoustic boost (+0.93)
```

### Acoustic Trap

```
[acoustic_trap] genre=rock, mood=intense, energy=0.95, likes_acoustic=True
#1 Storm Runner (9.99) — genre match (+3.00); mood match (+3.00); energy closeness (+3.84); acoustic preference (+0.15)
#2 Gym Hero (7.00) — mood match (+3.00); energy closeness (+3.92); acoustic preference (+0.08)
#3 Granite Sky (4.04) — energy closeness (+4.00); acoustic preference (+0.04)
#4 Static Hearts (3.85) — energy closeness (+3.76); acoustic preference (+0.09)
#5 Neon Cathedral (3.83) — energy closeness (+3.72); acoustic preference (+0.11)
```

### Flatline

```
[flatline] genre=pop, mood=happy, energy=0.5, likes_acoustic=False
#1 Sunrise City (9.54) — genre match (+3.00); mood match (+3.00); energy closeness (+2.72); less acoustic boost (+0.82)
#2 Rooftop Lights (6.61) — mood match (+3.00); energy closeness (+2.96); less acoustic boost (+0.65)
#3 Gym Hero (6.23) — genre match (+3.00); energy closeness (+2.28); less acoustic boost (+0.95)
#4 Signal in the Fog (4.33) — energy closeness (+3.92); less acoustic boost (+0.41)
#5 Velvet Sunrise (4.24) — energy closeness (+3.68); less acoustic boost (+0.56)
```

### Misspelled Mood

```
[misspelled_mood] genre=lofi, mood=Focus, energy=0.4, likes_acoustic=True
#1 Focus Flow (8.17) — genre match (+3.00); energy closeness (+4.00); acoustic preference (+1.17)
#2 Library Rain (8.09) — genre match (+3.00); energy closeness (+3.80); acoustic preference (+1.29)
#3 Midnight Coding (7.98) — genre match (+3.00); energy closeness (+3.92); acoustic preference (+1.06)
#4 Coffee Shop Stories (5.21) — energy closeness (+3.88); acoustic preference (+1.33)
#5 Pinecone Waltz (5.04) — energy closeness (+3.64); acoustic preference (+1.40)
```

### Extremist

```
[extremist] genre=electronic, mood=euphoric, energy=1.0, likes_acoustic=False
#1 Neon Cathedral (10.45) — genre match (+3.00); mood match (+3.00); energy closeness (+3.52); less acoustic boost (+0.93)
#2 Granite Sky (4.77) — energy closeness (+3.80); less acoustic boost (+0.97)
#3 Gym Hero (4.67) — energy closeness (+3.72); less acoustic boost (+0.95)
#4 Storm Runner (4.54) — energy closeness (+3.64); less acoustic boost (+0.90)
#5 Static Hearts (4.50) — energy closeness (+3.56); less acoustic boost (+0.94)
```

### Ghost Profile

```
[ghost_profile] genre=jazz, mood=nostalgic, energy=0.5, likes_acoustic=True
#1 Coffee Shop Stories (7.82) — genre match (+3.00); energy closeness (+3.48); acoustic preference (+1.33)
#2 Signal in the Fog (4.80) — energy closeness (+3.92); acoustic preference (+0.89)
#3 Focus Flow (4.77) — energy closeness (+3.60); acoustic preference (+1.17)
#4 Midnight Coding (4.74) — energy closeness (+3.68); acoustic preference (+1.06)
#5 Library Rain (4.69) — energy closeness (+3.40); acoustic preference (+1.29)
```

###

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

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:

- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:

- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:

- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
```
