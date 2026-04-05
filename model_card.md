# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

TuneFinder 1.0

---

## 2. Intended Use

TuneFinder 1.0 is a classroom simulation built to demonstrate the core mechanics of a content-based music recommender. Given a user's preferred genre, mood, energy level, and acoustic preference, it scores every song in a small catalog and returns the top matches. It is designed for educational exploration — specifically to show how explicit user preferences can be turned into a ranked list, and where that approach breaks down.

This system assumes the user can clearly articulate their own preferences in advance (genre, mood, energy level). It is not designed for real-world deployment. It should not be used to make recommendations for actual users in a production setting, nor should it be applied to large catalogs where the limitations of binary genre/mood matching and unused features would cause significant degradation in result quality.

---

## 3. How the Model Works

Every song in the catalog has a set of labels and numbers attached to it: a genre, a mood, an energy level (0 = very calm, 1 = very intense), and an acousticness value (0 = fully produced/electric, 1 = fully acoustic). The user provides their own preferences using the same four dimensions.

When a recommendation is requested, the system goes through every song one by one and gives it a score based on how closely it matches the user. A genre match adds 3 points. A mood match adds another 3 points. The energy difference between the user's target and the song's actual energy is converted into up to 4 points — the closer they are, the more points the song earns. Finally, if the user likes acoustic music, songs with higher acousticness earn up to 1.5 bonus points; if the user prefers electric/produced music, songs with lower acousticness earn up to 1 bonus point. After all songs are scored, they are sorted highest to lowest and the top results are returned with a plain-language explanation of why each song ranked where it did.

The main change from the starter code was implementing all of this logic from scratch — the original file had placeholder functions that returned empty lists.

---

## 4. Data

The catalog contains 20 songs. Each song has 10 fields: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. The dataset was expanded from the original 10-song starter to 20 by adding songs across new genres (r&b, metal, world, blues, electronic, folk, punk, classical, funk, trip hop) and moods (romantic, aggressive, adventurous, melancholy, euphoric, calm, rebellious, serene, playful, mysterious).

Despite the expansion, the catalog has one song per genre for most genres, which means a genre match is either a perfect hit or a complete miss. Features like valence, danceability, and tempo_bpm are stored but not used in scoring. The dataset also has no representation of hybrid or emerging genres (e.g. indie folk, hyperpop, afrobeats), and all songs are assumed to have a single fixed mood — real songs are context-dependent and can feel different to different listeners.

---

## 5. Strengths

The system works best for users whose preferred genre and mood both have a clear match in the catalog. When all four scoring signals fire together — genre match, mood match, close energy, and acoustic alignment — the #1 result wins by a wide margin and the explanation is transparent and easy to verify. lofi_focus returning Focus Flow at 11.17 and rock_workout returning Storm Runner at 10.86 are examples where the output immediately makes intuitive sense.

The scoring is also fully explainable. Every recommendation comes with a breakdown of exactly which factors contributed and how many points each added, which is valuable in an educational context where understanding why a result appeared matters as much as the result itself. Unlike black-box models, a user can look at the output and trace exactly why one song ranked above another.

---

## 6. Limitations and Bias

The most significant weakness is that genre and mood matching is binary — a user who prefers "indie pop" receives zero credit when a "pop" song appears, even though the two are closely related. This creates a filter bubble where users with niche or hyphenated tastes are permanently locked out of the largest scoring bonuses (+3.00 each), leaving their rankings driven almost entirely by energy proximity. The energy scoring itself compounds this problem: because the formula measures raw distance on a 0–1 scale, users who prefer low-energy music have fewer high-scoring songs available in the dataset, compressing their results into a narrower band than high-energy users experience. Additionally, three song features — valence, danceability, and tempo — are stored in the dataset but never used in scoring, meaning two users with opposite feelings about rhythm or positivity can receive identical recommendations. Taken together, these gaps mean the system works best for mainstream, high-energy users whose genre exists in the catalog, and systematically underserves everyone else.

---

## 7. Evaluation

I tested eleven user profiles in total — five standard profiles (pop_party, rock_workout, lofi_focus, ambient_unwind, synthwave_night) and six adversarial profiles designed to stress-test the scoring logic (genre_ghost, acoustic_trap, flatline, misspelled_mood, extremist, ghost_profile).

For each profile I looked at whether the top result felt intuitive, how large the score gap was between #1 and #2, and whether any unexpected songs broke into the top 5. The standard profiles all performed as expected: lofi_focus returned Focus Flow at 11.17 with a perfect energy match, and rock_workout surfaced Storm Runner at 10.86 with both genre and mood bonuses applied. In both cases the #1 result was a clear winner by a wide margin.

The adversarial profiles revealed more interesting behavior. The misspelled_mood profile ("Focus" instead of "focused") silently lost the +3.00 mood bonus with no warning, yet still returned the same top 3 songs as lofi_focus — just with lower scores. This confirmed the case-sensitivity bug but also showed that energy and genre were strong enough to compensate. The acoustic_trap profile (high energy + likes acoustic) exposed a real tension: high-energy songs score well on energy closeness but earn almost nothing from the acoustic bonus, since they tend to have low acousticness values. Storm Runner still won, but its score dropped from 10.86 to 9.99 compared to the standard rock_workout run. The ghost_profile (genre "jazz", mood "nostalgic" — neither present in the dataset as a match) was the most surprising: Coffee Shop Stories ranked #1 not because of any semantic match, but purely because its energy and acousticness happened to align numerically.

The clearest takeaway from testing was that when genre and mood both miss, the top results feel arbitrary rather than recommended — the system surfaces mathematically close songs with no explanation of why they are relevant to the user.

---

## 8. Future Work

1. **Fuzzy genre and mood matching.** Replace the binary exact-match check with a similarity lookup — for example, treating "indie pop" as a partial match for "pop", or "intense" as adjacent to "aggressive". This would eliminate the hard filter bubble that currently locks niche-genre users out of the top scoring tier.

2. **Use the unused features.** Valence, danceability, and tempo_bpm are loaded from the CSV but contribute nothing to the score. Adding even one of these — such as a valence closeness score weighted at +2.00 — would make the recommendations more sensitive to emotional tone and give users a meaningful way to distinguish between, say, a happy high-energy song and an aggressive high-energy one.

3. **Warn when preferences go unmet.** When no song in the catalog matches the user's genre or mood, the system should surface a notice rather than silently returning a math-driven fallback. A simple check after scoring — "no genre match found" — would make the output honest about what it was and wasn't able to do.

---

## 9. Personal Reflection

The biggest learning moment was writing the model card itself. It forced me to explain the scoring logic in plain language and confront the gaps — like the three unused features and the binary genre matching — that were easy to ignore while coding. I had not worked with model cards before, but seeing how they structure the "why" behind a model (intended use, limitations, evaluation) made it clear why they matter in real projects: a model that no one can explain is a model no one should trust.

AI tools helped most with the repetitive structural work — generating adversarial test profiles, drafting boilerplate output formatting, and catching edge cases in the scoring logic. The moments I needed to double-check were when the AI suggested code changes that looked correct but silently changed behavior, like modifying an import path. Running the program after each change and comparing output was the check, not reading the code alone.

What surprised me about the algorithm was how convincing the output felt for well-matched profiles even though the logic is just arithmetic. When lofi_focus returned Focus Flow as #1 with a perfect score and a clean explanation, it genuinely felt like a good recommendation — not because anything intelligent happened, but because the right features were aligned. That gap between "feels smart" and "is smart" is something I'll think about differently now when I use real recommendation apps.

For extending this project, the change I'd prioritize first is fuzzy genre matching — specifically because the binary miss is the most visible failure. A user who prefers "indie pop" getting zero genre credit is the kind of thing a real user would notice immediately and lose trust over.
