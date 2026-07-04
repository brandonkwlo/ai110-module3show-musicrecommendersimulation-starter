# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeCheck 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeCheck looks at a small list of songs and picks the ones that best match what a listener says they like. You tell it a favorite genre, a favorite mood, and how much energy and danceability you want. It scores every song and hands back the top 5, with plain reasons for each pick.

It assumes you know your own taste and can describe it in simple words like "pop" or "chill." It does not learn from listening history or feedback — every recommendation starts fresh from the preferences you type in.

**Intended use:** This is a classroom project, not a real product. It's meant to show how a simple scoring rule can feel like a recommendation.

**Not intended for:** Real music streaming decisions, judging someone's actual taste, targeting ads, or any use where the small 20-song catalog needs to represent real listening options.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

VibeCheck gives every song a score, then sorts songs from highest to lowest score.

Here's how a song earns points:

- **Genre match:** If the song's genre matches your favorite genre, it earns 2 points.
- **Mood match:** If the song's mood matches your favorite mood, it earns 2 more points.
- **Energy fit:** The closer the song's energy is to what you asked for, the more points it earns — up to 1 point for a perfect match.
- **Danceability fit:** Same idea as energy — the closer the match, the more points, up to 1 point.

All the points get added together into one score per song. The top 5 highest-scoring songs get recommended, along with a short list of reasons (like "genre match (+2.0)") explaining why each song scored the way it did.

Genre and mood matter the most because they're easy yes/no checks. Energy and danceability are more like tiebreakers that fine-tune the ranking.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 20 songs, stored in `data/songs.csv`. I added 10 songs to the original 10 that came with the starter project.

Each song has a genre, a mood, and five numbers: energy, tempo, valence, danceability, and acousticness.

There are 17 different genres and 15 different moods across the 20 songs. Most genres show up only once — pop and lofi are the only genres with more than one song. That means picking a genre often just points at one specific song, not a real style.

There's also a gap in the energy numbers: songs cluster between 0.22–0.58 (calmer) and 0.75–0.97 (high energy), with nothing in between. A listener who wants medium-high energy (around 0.6–0.7) won't find a great match.

The dataset is made up for this class project. It doesn't include lyrics, artist popularity, or real listening history, so it can't capture real musical taste — only genre, mood, and a few numeric vibes.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

It works best for users whose favorite genre and mood actually show up in the catalog. High-Energy Pop, Chill Lofi, and Deep Intense Rock all got a clear, sensible #1 pick that matched genre, mood, and energy at once.

The reasons list is a real strength. Seeing "genre match (+2.0), energy closeness (+0.97)" makes it obvious why a song was picked, instead of just trusting a mystery number.

It also held up under weird inputs. A made-up genre or a mood that doesn't exist in the catalog didn't crash the program — it just quietly used whatever preferences were actually valid.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness discovered during experiments: genre match creates a filter bubble around single-song genres, and the energy gap can't rescue a bad fit.** In `data/songs.csv`, 15 of the 17 genres (pop and lofi are the only exceptions) contain exactly one song, so a user's `favorite_genre` acts less like a taste signal and more like a lookup key for one specific track — everyone who shares that genre preference gets funneled toward the same recommendation regardless of their mood or energy target, which is a textbook filter bubble. This was confirmed by the "Contradictory Vibe" experiment (`genre=classical, mood=angry, energy=0.95`): *Still Water Suite*, a peaceful, low-energy classical piece (`energy=0.22`), still ranked #2 out of 20 songs purely on its +2.0 genre-match bonus, even though its energy and danceability were nearly the opposite of what was requested. Because each categorical match (`score_song` in [`src/recommender.py`](src/recommender.py)) is worth 2.0 points while the energy-gap term is capped at 1.0, no amount of numeric closeness can outweigh a genre or mood match, so the "energy gap" calculation can only ever fine-tune the ranking within a genre — it can never override a poor genre fit or rescue a good one. The energy-gap math also has a blind spot: catalog energy values cluster between 0.22–0.58 and 0.75–0.97 with no songs in between, so users who target moderate-high energy (around 0.60–0.70) are effectively ignored, since every song in the catalog is a mediocre numeric match for them.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles tested** (all defined in [`src/main.py`](src/main.py), full output in the README's [Experiments You Tried](README.md#experiments-you-tried) section):

| Profile | genre | mood | energy | danceability | Top pick |
|---|---|---|---|---|---|
| High-Energy Pop (P) | pop | happy | 0.85 | 0.85 | Sunrise City |
| Chill Lofi (L) | lofi | chill | 0.35 | 0.55 | Library Rain |
| Deep Intense Rock (R) | rock | intense | 0.90 | 0.60 | Storm Runner |
| Conflicting Mood-Energy (C) | pop | sad *(not in catalog)* | 0.90 | 0.60 | Sunrise City |
| Nonexistent Genre (N) | k-pop *(not in catalog)* | happy | 0.70 | 0.75 | Rooftop Lights |
| Contradictory Vibe (V) | classical | angry | 0.95 | 0.90 | Molten Sky |

For each run I checked whether the #1 result's genre/mood/energy actually matched the request, and whether the `reasons` list correctly explained the score.

**What surprised me:** I expected the "Conflicting Mood-Energy" profile (C) to visibly struggle or produce an oddly-ranked list, but its #1 result was identical to the "High-Energy Pop" profile's (P) — the system simply dropped the unmatched `mood="sad"` and let `genre="pop"` decide the winner, with no signal that the request was partially unsatisfiable. I also didn't expect "Contradictory Vibe" (V), which asked for `genre="classical"`, to return a metal song (Molten Sky) at #1 — it made sense once I traced it (mood="angry" matched, genre="classical" didn't, and Molten Sky's energy was a near-perfect fit), but it shows mood can override the genre the user explicitly typed.

**Pairwise comparisons** (why the differences make sense):

| Pair | What changed | Why it makes sense |
|---|---|---|
| P vs L | Pop/happy/high-energy picks (Sunrise City) → lofi/chill/low-energy picks (Library Rain), with zero song overlap | Genre, mood, and energy targets are all near-opposite, so the scoring correctly polarizes toward two different corners of the catalog |
| P vs R | Both want high energy, but P lands on pop/happy (Sunrise City) while R lands on rock/intense (Storm Runner) | Genre + mood together outweigh a shared energy target, showing categorical fields dominate when energy is similar |
| L vs R | Fully disjoint top-5 lists (chill lofi vs intense rock) | These are the two most extreme energy asks (0.35 vs 0.90) plus opposite genres/moods, so no crossover is expected |
| P vs C | Same #1 song (Sunrise City) even though C asked for mood="sad" instead of "happy" | "sad" doesn't exist in the catalog, so the mood term never fires for C and genre="pop" alone decides the winner — the mood request is silently ignored rather than changing the outcome |
| P vs N | Straight pop pick (Sunrise City) shifts to an indie-pop/happy pick (Rooftop Lights) once genre is swapped for a fictional "k-pop" | With genre unmatchable, mood="happy" becomes the strongest categorical signal, so the system reasonably falls back to the next best-matching field |
| P vs V | No overlap between top picks (Sunrise City vs Molten Sky) | The two profiles share no genre or mood, so a fully disjoint result set is correct |
| L vs C | Low-energy lofi pick vs C's high-energy pop pick, no overlap | Even though C's mood request was unsatisfiable, its energy target (0.90) is real and correctly separates it from L's low-energy request (0.35) |
| L vs N | Chill/lofi pick (Library Rain) vs happy/indie-pop pick (Rooftop Lights), no overlap | Both profiles have one broken or absent genre signal (L's genre is valid, N's isn't), but their moods differ (chill vs happy), which is enough to fully redirect the ranking |
| L vs V | Fully opposite energy asks (0.35 vs 0.95) with disjoint results | Confirms the energy-closeness term correctly pulls recommendations toward each extreme of the catalog |
| R vs C | Same energy target (0.90) but different #1 songs (Storm Runner vs Sunrise City) | With energy held constant, genre (rock vs pop) becomes the deciding factor — isolates genre as the tie-breaker when energy is equal |
| R vs N | Intense/high-energy rock pick vs moderate-energy indie-pop pick, no overlap | Genre, mood, and energy all differ enough that a shared result would be surprising |
| R vs V | Both land on aggressive, high-energy songs from *different* genres (rock's Storm Runner vs metal's Molten Sky) even though R asked for rock and V asked for classical | Mood ("intense"/"angry") plus a close energy match pulled both toward the catalog's aggressive-sounding tracks, showing mood + energy can matter more than the literal genre string |
| C vs N | C keeps its genre match (pop) but loses its mood match; N keeps its mood match (happy) but loses its genre match — different top songs result | Each profile has exactly one working categorical field, and that field ends up defining the recommendation's vibe, confirming the system falls back gracefully to whichever signal is actually valid |
| C vs V | C's valid genre (pop) but broken mood ("sad") skews the result toward upbeat pop; V's valid mood ("angry") but broken genre ("classical") skews toward aggressive metal | Shows that whichever single categorical field actually exists in the catalog effectively decides the genre bucket of the recommendation, regardless of which field the user intended to be the strong request |
| N vs V | N's broken genre + valid mood → upbeat indie pop; V's valid genre + unusual mood/energy combo → aggressive metal | Different "which field is broken" scenarios land in completely different genre buckets, reinforcing that genre and mood are not interchangeable fallbacks — whichever one is valid drives very different recommendations |

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. **Rebalance the weights.** Genre and mood match are worth 2 points each, but energy and danceability only add up to 1 point each. I'd lower the genre/mood weight (or raise the numeric weights) so a bad energy fit can actually change the ranking, instead of always losing to genre.
2. **Add more songs per genre.** Right now most genres only have one song. With more songs per genre, picking a genre would actually mean picking a style, not one specific track.
3. **Flag unmatched preferences.** If a user picks a mood or genre that doesn't exist in the catalog, the system should say so ("no songs match 'sad', showing next-best options") instead of silently dropping it.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment was the "Contradictory Vibe" test. I asked for a classical song and got a metal song back. At first that looked like a bug. It wasn't — mood matched, genre didn't, and the math just did what I told it to do. That's when it really clicked that bias in a recommender isn't some hidden mystery. It's just the weights I chose, showing up in the output.

Using an AI coding assistant helped me move fast — it wrote the scoring function, built out multiple test profiles, and formatted the terminal output so I could actually read it. But I had to double-check the numbers myself. I ran a small script to count genres and moods instead of guessing, and I actually ran every profile in the terminal before writing any output into this file, so nothing here is made up.

What surprised me most is how "smart" a really simple point-adding formula can feel. It's just addition and subtraction, but once you print out the reasons next to each song, it feels like the system understands your taste. That's a little unsettling — it means simple math can look convincing even when it's quietly biased, like it is here.

If I kept working on this, I'd try rebalancing the weights first, then add a bigger, more varied song catalog, and maybe let the system explain when it can't fully match what a user asked for instead of picking silently.
