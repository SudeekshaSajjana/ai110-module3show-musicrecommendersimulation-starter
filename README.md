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


'''
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

Adversarial / Edge Case Profiles
========================================

[Out-of-range energy (5.0)] prefs={'genre': 'pop', 'mood': 'happy', 'energy': 5.0}
----------------------------------------
1. Sunrise City (Neon Echo)
   Score:   -1.77
   Because: genre matches (pop), mood matches (happy), energy close to target (0.82 vs 5.0)
----------------------------------------
2. Gym Hero (Max Pulse)
   Score:   -2.61
   Because: genre matches (pop), energy close to target (0.93 vs 5.0)
----------------------------------------
3. Rooftop Lights (Indigo Parade)
   Score:   -3.86
   Because: mood matches (happy), energy close to target (0.76 vs 5.0)
----------------------------------------

[Negative energy (-2.0)] prefs={'genre': 'rock', 'mood': 'intense', 'energy': -2.0}
----------------------------------------
1. Storm Runner (Voltline)
   Score:   0.13
   Because: genre matches (rock), mood matches (intense), energy close to target (0.91 vs -2.0)
----------------------------------------
2. Gym Hero (Max Pulse)
   Score:   -1.90
   Because: mood matches (intense), energy close to target (0.93 vs -2.0)
----------------------------------------
3. Spacewalk Thoughts (Orbit Bloom)
   Score:   -1.92
   Because: energy close to target (0.28 vs -2.0)
----------------------------------------

[NaN energy] prefs={'genre': 'lofi', 'mood': 'chill', 'energy': nan}
----------------------------------------
1. Sunrise City (Neon Echo)
   Score:   nan
   Because: energy close to target (0.82 vs nan)
----------------------------------------
2. Midnight Coding (LoRoom)
   Score:   nan
   Because: genre matches (lofi), mood matches (chill), energy close to target (0.42 vs nan)
----------------------------------------
3. Storm Runner (Voltline)
   Score:   nan
   Because: energy close to target (0.91 vs nan)
----------------------------------------

[String energy ("0.8")] prefs={'genre': 'pop', 'mood': 'happy', 'energy': '0.8'}
----------------------------------------
   ERROR: TypeError: unsupported operand type(s) for -: 'float' and 'str'
----------------------------------------

[Case mismatch (Pop/Happy)] prefs={'genre': 'Pop', 'mood': 'Happy', 'energy': 0.8}
----------------------------------------
1. Sunrise City (Neon Echo)
   Score:   1.47
   Because: energy close to target (0.82 vs 0.8)
----------------------------------------
2. Rooftop Lights (Indigo Parade)
   Score:   1.44
   Because: energy close to target (0.76 vs 0.8)
----------------------------------------
3. Night Drive Loop (Neon Echo)
   Score:   1.42
   Because: energy close to target (0.75 vs 0.8)
----------------------------------------

[Empty profile] prefs={}
----------------------------------------
1. Sunrise City (Neon Echo)
   Score:   0.00
   Because: 
----------------------------------------
2. Midnight Coding (LoRoom)
   Score:   0.00
   Because: 
----------------------------------------
3. Storm Runner (Voltline)
   Score:   0.00
   Because: 
----------------------------------------

[Nonexistent genre/mood] prefs={'genre': 'opera', 'mood': 'furious', 'energy': 0.5}
----------------------------------------
1. Dust Road Ballad (Willow Creek)
   Score:   1.50
   Because: energy close to target (0.5 vs 0.5)
----------------------------------------
2. Golden Hour Bloom (Petal Radio)
   Score:   1.42
   Because: energy close to target (0.45 vs 0.5)
----------------------------------------
3. Velvet Whisper (Satin Groove)
   Score:   1.42
   Because: energy close to target (0.55 vs 0.5)
----------------------------------------

[Extra irrelevant keys] prefs={'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'artist': 'Neon Echo', 'min_danceability': 0.9}
----------------------------------------
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
'''
---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

**Lowering the genre weight (2.0 → 0.5):** I tried this on a "pop, happy, energy 0.8" listener. Normally Gym Hero (genre match only) beats Rooftop Lights (mood + energy match, no genre) for the #2 spot. Once genre was worth less, they swapped places — Rooftop Lights moved up to #2 and Gym Hero dropped to #3. So the genre weight isn't just changing the numbers, it's actually deciding which song wins when a listener's preferences pull in different directions.

**Adding valence (how "positive-sounding" a song is) to the score:** I added a bonus for songs whose valence was close to a target of 0.8 (asking for upbeat-sounding songs). This bumped Neon Pulse Rave up and pushed Night Drive Loop out of the top 5 entirely, since Night Drive Loop has a "moody" feel with fairly low valence even though its energy was a decent match. This shows the recommender currently can't tell the difference between a song that's high-energy-and-happy versus high-energy-and-moody — adding valence would let it capture that difference.

**Different types of users:** Listeners who ask for a genre/mood/energy combination that actually exists together in the catalog (like "lofi, chill, low energy") get a top pick that matches all three and feels correct. Listeners who ask for an unusual combination (like "folk, happy, high energy," which doesn't really exist in this catalog) still get a confident-looking top 3, but it's really just the least-bad partial match. And a listener who gives no preferences at all still gets a ranked list — it just falls back to whatever song happens to be listed first in the CSV file, which isn't a real recommendation at all.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

It only works on a tiny catalog of 18 songs, and most genres only have one song in them, so picking a favorite genre often just means "get that one song" no matter what mood or energy you also asked for. It does not understand lyrics, language, vocals, or instruments at all — it only looks at genre, mood, and energy, so two very different-sounding songs could get treated as a great match if those three labels line up. It can also unfairly favor genre matches over everything else, since genre is worth more points than mood or energy, so a so-so genre match can beat a really strong mood-and-energy match. If a listener doesn't give a genre or mood the system recognizes exactly (like a different capitalization or spelling), that match is silently missed with no warning. And if a listener gives very few preferences, or ones nothing in the catalog fits well, the system still confidently hands back a top 5 — it doesn't have a way to say "I don't have a good answer for you," it just returns whatever scored highest, even if that's barely better than anything else.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

The biggest learning moment during this project is how hard it is to create a scoring system that accurately recommends songs without having some sort of mistake. The AI helped me with creating the code for the functions. However, I needed to double check the code sometimes because it wouldn't be efficient or there would be errors in the code. I was surprised that only a few lines of codes can give some sort of recommendation, even if it's not completely accurate. If I extended this project, I would try to add more methods and algorithms to give more accurate recommendations. This would be done with more song descriptions and more songs in the csv file.

