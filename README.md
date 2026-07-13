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

Streaming platforms like Spotify and YouTube predict recommendations by blending the use of matching users to similar users' behavior with matching songs to a user's stated preferences based on the songs' own attributes, plus contextual signals. The data involved falls into user data (UserProfile: favorite genre/mood, target energy, acoustic preference), item data (Song: categorical fields like genre/mood/artist and continuous fields like energy/tempo/valence/danceability/acousticness), and derived data (scores, rankings, explanations). songs.csv shows that energy and acousticness are the most discriminative continuous features, while genre/mood are too sparse across only 10 songs to use as hard filters. For numeric features like energy, the right scoring approach is a closeness-based formula (1 - abs(song.value - user.target)) rather than "higher is better," since it rewards proximity to the user's target in both directions. Finally, the system needs two distinct pieces: a scoring rule (score_song) that judges one song against one user in isolation, and a ranking rule (recommend_songs/Recommender.recommend) that operates on the whole scored list to sort, cut to top-k, break ties, and apply any list-level policy — keeping these separate makes each independently testable and reusable.

### Planned data flow

```
INPUT                              PROCESS (loop once per song)                    OUTPUT
─────                              ─────────────────────────────                   ──────
user_prefs dict                    for song in songs:                              sorted list, sliced to top k
{genre, mood, energy}         ┌──▶     score, reasons = score_song(user_prefs, song)         │
                               │            │                                       recommend_songs()
songs: List[Dict]             │            ├─ genre == song["genre"]?  +2.0         returns
  ← load_songs(csv_path)      │            │     → reasons.append("genre match")   [(song, score, explanation), ...]
                               │            │
                               │            ├─ mood == song["mood"]?    +1.0
                               │            │     → reasons.append("mood match")
                               │            │
                               │            ├─ energy closeness:
                               │            │     (1 - abs(song["energy"] - user energy)) * weight
                               │            │     → reasons.append(f"energy close ({song['energy']})")
                               │            │
                               │            └─ score_song returns (score, reasons)
                               │
                               └──▶     scored.append((song, score, reasons))
                                    (repeat for all rows in songs.csv)

scored  →  sort by score, descending  →  take first k  →  build explanation string from reasons  →  return
```

`score_song` only ever looks at one song plus the user's preferences — it has no idea about rank, ties, or k, which keeps it testable on a single song. `recommend_songs` (or `Recommender.recommend`) owns the loop, the sort, the top-k cut, and turning `reasons` into a human-readable explanation.

### Planned scoring recipe

- **Genre match: +2.0** — genre is treated as a stable identity preference, so getting it right (or wrong) matters most.
- **Mood match: +1.0** — mood is more situational/mutable than genre, so it should tip close calls rather than dominate.
- **Energy closeness: `(1 - abs(song.energy - user.target_energy)) * 1.5`** — scaled up so a strong energy fit can meaningfully compete with a genre or mood match, since raw closeness on this catalog (energy 0.28–0.97) tends to cluster around 0.5–0.85 rather than the extremes.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18

Top Recommendations
========================================
1. Sunrise City (Neon Echo)
   Score:   4.47
   Because: genre matches (pop), mood matches (happy), energy close to target (0.82 vs 0.8)
----------------------------------------
2. Gym Hero (Max Pulse)
   Score:   3.30
   Because: genre matches (pop), energy close to target (0.93 vs 0.8)
----------------------------------------
3. Rooftop Lights (Indigo Parade)
   Score:   2.44
   Because: mood matches (happy), energy close to target (0.76 vs 0.8)
----------------------------------------
4. Night Drive Loop (Neon Echo)
   Score:   1.42
   Because: energy close to target (0.75 vs 0.8)
----------------------------------------
5. Neon Pulse Rave (Circuit Bloom)
   Score:   1.38
   Because: energy close to target (0.88 vs 0.8)
----------------------------------------
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



